import os
import string
from typing import AsyncGenerator, TypeVar

from ragkit.pipeline import Module, State
from ragkit.pipeline.vanilla import Generation


class AgentState(State):
    pass


class PromptAgentState(AgentState):
    final_prompt: str
    response: str


AgentStateType = TypeVar("AgentStateType", bound=AgentState)
PromptAgentStateType = TypeVar("PromptAgentStateType", bound=PromptAgentState)


class Agent(Module[AgentStateType]):
    pass


class PromptAgent(Agent[PromptAgentStateType]):
    def __init__(
        self,
        llm_model: str,
        output_key: list[str] | str = "response",
        input_key: list[str] | None = None,
        generation_key: str = "generation",
        temperature: float = 0.01,
        top_p: float = 0.01,
        max_tokens: int | None = None,
        seed: int | None = None,
        *args,
        **kwargs,
    ):
        self.prompt = "\n".join([x.strip() for x in self.__doc__.split("\n")])
        if input_key is None:
            input_key = [i[1] for i in string.Formatter().parse(self.prompt) if i[1] is not None]
        super().__init__(input_key=input_key, output_key=output_key, *args, **kwargs)
        self.generation_key = generation_key
        seed = seed or os.getenv("LLM_SEED", None)
        if seed is not None:
            seed = int(seed)
        self.generate = Generation(
            llm_model=llm_model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            output_key=generation_key,
            seed=seed,
        )

    async def form_prompt(self, inputs: dict):
        format_dict = {key: inputs.get(key) for key in self.input_key}
        try:
            return self.prompt.format(**format_dict)
        except KeyError as e:
            raise ValueError(f"Missing input: {e}") from None

    async def _parse_response(self, response: str):
        try:
            return await self.parse_response(response)
        except Exception as e:
            raise ValueError(f"Invalid Response: {response}, Error: {e}") from None

    async def parse_response(self, response: str):
        return {self.output_key: response}

    async def forward(self, state: PromptAgentStateType, **kwargs) -> PromptAgentStateType:
        final_prompt = await self.form_prompt(state)
        state["final_prompt"] = final_prompt
        state = await self.generate(state)
        output = await self._parse_response(state[self.generation_key])
        state.update(output)
        return state

    async def streaming(
        self, state: PromptAgentStateType, **kwargs
    ) -> AsyncGenerator[AgentStateType, None]:
        final_prompt = await self.form_prompt(state)
        state["final_prompt"] = final_prompt
        async for state in self.generate.stream(state):
            yield state
        output = await self._parse_response(state[self.generation_key])
        state.update(output)
        yield state
