from dataclasses import dataclass
from logging import Logger
from typing import (
    AsyncGenerator,
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
)

import anyio
from typing_extensions import TypedDict
from vmc_client import AsyncVMC


class State(TypedDict, total=False):
    pass


StateType = TypeVar("StateType", bound=State)


@dataclass
class SharedResource:
    llm: AsyncVMC
    callback: "CallbackGroup"


class Callback(Generic[StateType]):
    async def on_module_enter(self, module: "Module", state: StateType):
        pass

    async def on_module_exit(self, module: "Module", state: StateType):
        pass

    async def on_module_fail(self, module: "Module", state: StateType, exc: Exception):
        pass


class CallbackGroup:
    def __init__(self, callbacks: list[Callback], run_in_background: bool = False):
        if callbacks is None:
            callbacks = []
        self.callbacks = callbacks
        self.run_in_background = run_in_background

    def _on_event_construct(self, event: str):
        async def _on_event(*args):
            if not self.callbacks:
                return
            try:
                if self.run_in_background:
                    async with anyio.create_task_group() as tg:
                        for callback in self.callbacks:
                            tg.start_soon(callback.__getattribute__(event), *args)
                else:
                    for callback in self.callbacks:
                        await callback.__getattribute__(event)(*args)
            except Exception as e:
                Logger.warning(f"Error in callback {event}: {e}")

        return _on_event

    def __getattribute__(self, name: str):
        if name.startswith("on_"):
            return self._on_event_construct(name)
        return super().__getattribute__(name)

    def add_callback(self, callback: Callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback: Callback):
        self.callbacks.remove(callback)

    def clear(self):
        self.callbacks = []


class Module(Generic[StateType]):
    def __init__(
        self,
        modules: Optional[List["Module"]] = None,
        exec_in_parallel: bool = False,
        exec_order: Literal["before", "after", "ignore"] = "ignore",
        input_key: Optional[Union[List[str], str]] = None,
        output_key: Optional[Union[List[str], str]] = None,
        callbacks: list[Callback] | None = None,
        shared: Optional[SharedResource] = None,
        event_name: str = "module",
        description: str = "",
        module_name: str | None = None,
        *args,
        **kwargs,
    ):
        self.name = module_name or self.__class__.__name__
        self.input_key = input_key
        self.output_key = output_key
        self.shared = shared
        self.description = description

        self._modules = modules
        self._exec_in_parallel = exec_in_parallel
        self._exec_order = exec_order
        if self._exec_order == "ignore" and self._modules is None:
            self._exec_order = "after"
        self._inited = False
        self._callback_name = event_name
        self._enter_callback = f"on_{self._callback_name}_enter"
        self._exit_callback = f"on_{self._callback_name}_exit"
        self._fail_callback = f"on_{self._callback_name}_fail"
        self._callbacks = callbacks

    async def _init_sub_modules(self):
        _to_init = [v for v in self.__dict__.values() if isinstance(v, Module)]
        if self._modules is not None:
            _to_init = _to_init + self._modules
        async with anyio.create_task_group() as tg:
            for t in _to_init:
                t.name = f"{self.name}::{t.name}"
                tg.start_soon(t._init, self.shared)

    def _default_sharedresource(self):
        return SharedResource(llm=AsyncVMC(), callback=CallbackGroup(self._callbacks or []))

    async def _init(self, shared: SharedResource | None = None):
        if self._inited:
            return
        if self.shared is None and shared is None:
            shared = self._default_sharedresource()
        self.shared = shared or self.shared
        await self._init_sub_modules()
        self._inited = True

    def _get_input(self, state: StateType):
        if isinstance(self.input_key, list):
            return {k: state.get(k) for k in self.input_key}
        else:
            return {self.input_key: state.get(self.input_key)}

    async def _exec_sub_modules(self, state: StateType, *args) -> StateType:
        if self._modules is None:
            return state
        if self._exec_in_parallel:
            async with anyio.create_task_group() as tg:
                for t in self._modules:
                    tg.start_soon(t.__call__, state, *args)
        else:
            for t in self._modules:
                state = await t.__call__(state, *args)
        return state

    async def _streaming_sub_modules(
        self, state: StateType, *args
    ) -> AsyncGenerator[StateType, None]:
        if self._modules is None:
            return
        if self._exec_in_parallel:
            async with anyio.create_task_group() as tg:
                for t in self._modules:
                    tg.start_soon(t.__call__, state, *args)
            yield state
            return
        else:
            for t in self._modules:
                async for s in t.stream(state, *args):
                    yield s

    async def __call__(
        self, state: StateType, callbacks: list[Callback] | None = None, **kwargs
    ) -> StateType:
        await self._init()
        if callbacks:
            callback = CallbackGroup(callbacks)
        else:
            callback = self.shared.callback

        await getattr(callback, self._enter_callback)(self, state)
        if self._exec_order == "before":
            state = await self._exec(state, **kwargs)
        state = await self._exec_sub_modules(state, callbacks)
        if self._exec_order == "after":
            state = await self._exec(state, **kwargs)
        await getattr(callback, self._exit_callback)(self, state)
        return state

    async def _exec(self, state: StateType, **kwargs) -> StateType:
        try:
            return await self.forward(state, **kwargs)
        except Exception as e:
            await getattr(self.shared.callback, self._fail_callback)(self, state, e)
            raise e from None

    async def stream(
        self, state: StateType, callbacks: list[Callback] | None = None, **kwargs
    ) -> AsyncGenerator[StateType, None]:
        await self._init()
        if callbacks:
            callback = CallbackGroup(callbacks)
        else:
            callback = self.shared.callback

        await getattr(callback, self._enter_callback)(self, state)
        if self._exec_order == "before":
            async for s in self._exec_streaming(state, **kwargs):
                yield s
        async for s in self._streaming_sub_modules(state, callbacks):
            yield s
        if self._exec_order == "after":
            async for s in self._exec_streaming(state, **kwargs):
                yield s
        await getattr(callback, self._exit_callback)(self, state)
        return

    async def _exec_streaming(self, state: StateType, **kwargs) -> AsyncGenerator[StateType, None]:
        try:
            async for s in self.streaming(state, **kwargs):
                yield s
        except Exception as e:
            await getattr(self.shared.callback, self._fail_callback)(self, state, e)
            raise e from None

    async def forward(self, state: StateType, **kwargs) -> StateType:
        return state

    async def streaming(self, state: StateType, **kwargs) -> AsyncGenerator[StateType, None]:
        yield await self.forward(state)

    def __or__(self, module: "Module") -> "Pipeline[StateType]":
        assert isinstance(module, Module), "Only Module can be piped"
        return Pipeline[StateType](modules=[self, module])


class Pipeline(Module[StateType]):
    def __or__(self, module: "Module") -> "Pipeline[StateType]":
        assert isinstance(module, Module), "Only Module can be piped"
        self._modules.append(module)
        return self
