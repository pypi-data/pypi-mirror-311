from typing import Awaitable, Callable, List, Union

from vmc_client import AsyncVMC
from vmc_client.types.generation.message_params import GenerationMessageParam

from ragkit.document import BaseReranker, BaseRetriever, Chunk

from ._consts import DEFAULT_FINAL_PROMPT
from .modules import (
    ContextComposer,
    Generation,
    HistoryProcessor,
    LLMCost,
    PromptComposer,
    Reranker,
    Retriever,
    TextProcessor,
)
from .pipeline import Callback, Module, State


class VanillaState(State):
    query: str
    doc_ids: List[str]
    rewritten_queries: List[str]
    history: Union[List[GenerationMessageParam], str]
    chunks: List[Chunk]
    context: str
    final_prompt: str
    response: str
    cost: LLMCost


async def default_fn_preprocess(text: str) -> str:
    return text.strip()


async def default_fn_postprocess(text: str) -> str:
    return text.strip()


async def default_fn_history(messages: list[GenerationMessageParam]) -> str:
    if not messages:
        return ""
    msg = "\n".join([f"{m['role']}: {m['content'].strip()}" for m in messages]).strip()
    msg = f"<history>\n{msg}\n</history>"
    return msg


async def default_fn_context(chunks: list[Chunk]) -> str:
    if not chunks:
        return ""
    context = "\n".join([chunk.content for chunk in chunks]).strip()
    context = f"<context>\n{context}\n</context>"
    return context


async def default_fn_final_prompt(query: str, context: str, history: str) -> str:
    return DEFAULT_FINAL_PROMPT.format(question=query, context=context, history=history)


def _build_vanilla_modules(
    llm_model: str,
    retriever: BaseRetriever | None = None,
    reranker: BaseReranker | None = None,
    fn_preprocess: Callable[[str], Awaitable[str]] | None = None,
    fn_postprocess: Callable[[str], Awaitable[str]] | None = None,
    fn_history: Callable[[list[GenerationMessageParam]], Awaitable[str]] | None = None,
    fn_context: Callable[[list[Chunk]], Awaitable[str]] | None = None,
    fn_final_prompt: Callable[[str, str, str], Awaitable[str]] | None = None,
    temperature: float = 0.01,
    top_p: float = 0.01,
):
    transforms = [
        TextProcessor(fn_preprocess or default_fn_preprocess, key="query"),
        HistoryProcessor(fn_history or default_fn_history),
        Retriever(retriever or BaseRetriever()),
        Reranker(reranker or BaseReranker()),
        ContextComposer(fn_process=fn_context or default_fn_context),
        PromptComposer(fn_process=fn_final_prompt or default_fn_final_prompt),
        Generation(llm_model=llm_model, temperature=temperature, top_p=top_p),
        TextProcessor(fn_postprocess or default_fn_postprocess, key="response"),
    ]
    return transforms


def build_vanilla_pipeline(
    llm_model: str,
    llm: AsyncVMC | None = None,
    retriever: BaseRetriever | None = None,
    reranker: BaseReranker | None = None,
    fn_preprocess: Callable[[str], Awaitable[str]] | None = None,
    fn_postprocess: Callable[[str], Awaitable[str]] | None = None,
    fn_history: Callable[[list[GenerationMessageParam]], Awaitable[str]] | None = None,
    fn_context: Callable[[list[Chunk]], Awaitable[str]] | None = None,
    fn_final_prompt: Callable[[str, str, str], Awaitable[str]] | None = None,
    callbacks: list[Callback] = [],
    temperature: float = 0.01,
    top_p: float = 0.01,
):
    modules = _build_vanilla_modules(
        llm_model=llm_model,
        retriever=retriever,
        reranker=reranker,
        fn_preprocess=fn_preprocess,
        fn_postprocess=fn_postprocess,
        fn_history=fn_history,
        fn_context=fn_context,
        fn_final_prompt=fn_final_prompt,
        temperature=temperature,
        top_p=top_p,
    )
    return Module[VanillaState](
        modules=modules, callbacks=callbacks, llm=llm, module_name="VanillaPipeline"
    )
