from dataclasses import dataclass
from typing import Awaitable, Callable

from vmc_client.types.generation.message_params import GenerationMessageParam

from ragkit.document import BaseReranker, BaseRetriever, Chunk

from .pipeline import Module


@dataclass
class LLMCost:
    currency: str = "Unknown"
    multiplier: int = 1
    total_tokens: int = 0
    total_cost: float = 0.0
    input_tokens: int = 0
    input_cost: float = 0.0
    output_tokens: int = 0
    output_cost: float = 0.0


class TextProcessor(Module):
    def __init__(self, fn_process: Callable[[str], Awaitable[str]], key: str):
        super().__init__(input_key=key, output_key=key)
        self.fn_process = fn_process
        self.key = key

    async def forward(self, state, **kwargs):
        state[self.key] = await self.fn_process(state[self.key])
        return state


class HistoryProcessor(Module):
    def __init__(
        self,
        fn_process: Callable[[list[GenerationMessageParam]], Awaitable[str]],
        input_key: str = "history",
        output_key: str = "history",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def forward(self, state, **kwargs):
        state[self.output_key] = await self.fn_process(state.get(self.input_key))
        return state


class ContextComposer(Module):
    def __init__(
        self,
        fn_process: Callable[[list[Chunk]], Awaitable[str]],
        input_key: str = "chunks",
        output_key: str = "context",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def forward(self, state, **kwargs):
        state[self.output_key] = await self.fn_process(state.get(self.input_key))
        return state


class PromptComposer(Module):
    def __init__(
        self,
        fn_process: Callable[[str, str, str], Awaitable[str]],
        input_key: list[str] = ["query", "context", "history"],
        output_key: str = "final_prompt",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.fn_process = fn_process

    async def forward(self, state, **kwargs):
        state[self.output_key] = await self.fn_process(**self._get_input(state))
        return state


class Retriever(Module):
    def __init__(
        self,
        retriever: BaseRetriever,
        input_key: list[str] = ["query", "doc_ids"],
        output_key: str = "chunks",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.retriever = retriever

    async def forward(self, state, **kwargs):
        state[self.output_key] = await self.retriever.retrieve(**self._get_input(state))
        return state


class Reranker(Module):
    def __init__(
        self,
        reranker: BaseReranker,
        input_key: list[str] = ["query", "chunks"],
        output_key: str = "chunks",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.reranker = reranker

    async def forward(self, state, **kwargs):
        state[self.output_key] = await self.reranker.rerank(**self._get_input(state))
        return state


class Generation(Module):
    def __init__(
        self,
        llm_model: str,
        temperature: float = 0.01,
        top_p: float = 0.01,
        max_tokens: int | None = None,
        seed: int | None = None,
        generation_kwargs: dict = {},
        input_key: str = "final_prompt",
        output_key: str = "response",
        cost_key: str = "cost",
    ):
        super().__init__(input_key=input_key, output_key=output_key)
        self.llm_model = llm_model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.input_key = input_key
        self.cost_key = cost_key
        self.seed = seed
        self._generation_kwargs = generation_kwargs

    def _prepare_generate_kwargs(self, state):
        generate_kwargs = {
            "content": state[self.input_key],
            "model": self.llm_model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "seed": self.seed,
            **self._generation_kwargs,
        }
        return {k: v for k, v in generate_kwargs.items() if v is not None}

    async def forward(self, state, **kwargs):
        resp = await self.shared.llm.generate(**self._prepare_generate_kwargs(state))
        state[self.output_key] = resp.text
        cost: LLMCost = state.get(self.cost_key, LLMCost())
        cost.input_tokens += resp.cost.prompt_tokens
        cost.output_tokens += resp.cost.generated_tokens
        cost.total_tokens += resp.cost.total_tokens
        cost.input_cost += resp.cost.prompt_cost
        cost.output_cost += resp.cost.generated_cost
        cost.total_cost += resp.cost.total_cost
        cost.currency = resp.cost.currency
        cost.multiplier = resp.cost.multiplier
        state[self.cost_key] = cost
        return state

    async def streaming(self, state, **kwargs):
        state[self.output_key] = ""
        async for token in self.shared.llm.stream(**self._prepare_generate_kwargs(state)):
            state[self.output_key] += token.token
            if token.cost:
                cost = state.get(self.cost_key, LLMCost())
                cost.input_tokens += token.cost.prompt_tokens
                cost.output_tokens += token.cost.generated_tokens
                cost.total_tokens += token.cost.total_tokens
                cost.input_cost += token.cost.prompt_cost
                cost.output_cost += token.cost.generated_cost
                cost.total_cost += token.cost.total_cost
                cost.currency = token.cost.currency
                cost.multiplier = token.cost.multiplier
                state[self.cost_key] = cost
            yield state
