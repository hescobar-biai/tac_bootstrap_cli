"""Tool sequencer module for ensuring sequential tool execution per thread.

Claude requires this pattern for tool execution:
1. Model requests ONE tool (`tool_use`)
2. Backend executes THAT tool
3. Backend responds with `tool_result`
4. Model continues and (if needed) requests the next tool

Tools must NEVER execute concurrently for the same thread_id.

Common causes of concurrent execution:
- Using asyncio.gather() for tool execution
- Fire-and-forget tasks without awaiting
- Automatic retries that fire while a previous attempt is still running
- Multiple agents sharing the same thread_id

Usage:
    from adw_modules.tool_sequencer import run_tool_sequential

    async def my_tool_handler(thread_id: str, tool_input: dict) -> dict:
        async def execute():
            # Your actual tool execution logic here
            return await some_async_tool_call(tool_input)

        # This ensures only one tool runs at a time per thread_id
        return await run_tool_sequential(thread_id, execute)
"""

import asyncio
from collections import defaultdict
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

# Lock storage: one lock per thread_id
# Using defaultdict ensures a lock is created on first access
_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)


async def run_tool_sequential(thread_id: str, fn: Callable[[], Awaitable[T]]) -> T:
    """Execute a tool function sequentially for the given thread.

    Ensures that tool calls for the same thread_id never run concurrently.
    If a tool is already running for this thread_id, the caller will wait
    until it completes before executing.

    Args:
        thread_id: The unique identifier for the conversation thread.
                   All tool calls with the same thread_id will be serialized.
        fn: An async function (no arguments) that executes the tool.
            Typically a closure or lambda wrapping the actual tool call.

    Returns:
        The result of the tool function.

    Raises:
        Any exception raised by the tool function is re-raised.

    Example:
        async def call_my_tool():
            return await external_api.execute(params)

        result = await run_tool_sequential("thread-123", call_my_tool)
    """
    async with _locks[thread_id]:
        return await fn()


def get_active_thread_count() -> int:
    """Get the number of threads that currently have locks.

    Useful for debugging and monitoring. Note that this counts all threads
    that have ever acquired a lock, not just those currently holding one.

    Returns:
        Number of thread_ids with associated locks.
    """
    return len(_locks)


def clear_thread_locks() -> None:
    """Clear all thread locks.

    WARNING: Only use this for testing or shutdown scenarios.
    Clearing locks while tools are executing will cause undefined behavior.
    """
    _locks.clear()


async def run_tools_parallel_across_threads(
    tool_calls: list[tuple[str, Callable[[], Awaitable[T]]]]
) -> list[T]:
    """Execute multiple tool calls in parallel, but sequential within each thread.

    This function allows parallel execution across DIFFERENT thread_ids while
    maintaining sequential execution within the SAME thread_id.

    Args:
        tool_calls: List of (thread_id, tool_function) tuples.
                    Tools with different thread_ids run in parallel.
                    Tools with the same thread_id run sequentially.

    Returns:
        List of results in the same order as the input tool_calls.

    Example:
        results = await run_tools_parallel_across_threads([
            ("thread-1", lambda: tool_a()),  # These two run sequentially
            ("thread-1", lambda: tool_b()),
            ("thread-2", lambda: tool_c()),  # This runs in parallel with thread-1
        ])
    """
    async def wrapped_call(thread_id: str, fn: Callable[[], Awaitable[T]]) -> T:
        return await run_tool_sequential(thread_id, fn)

    tasks = [wrapped_call(thread_id, fn) for thread_id, fn in tool_calls]
    return await asyncio.gather(*tasks)


class ToolSequencer:
    """Class-based tool sequencer for more control over lock lifecycle.

    Use this when you need explicit control over lock cleanup, or when you
    want to isolate locks to a specific scope (e.g., per-request).

    Example:
        sequencer = ToolSequencer()
        try:
            result = await sequencer.run(thread_id, my_tool_fn)
        finally:
            sequencer.cleanup()
    """

    def __init__(self) -> None:
        """Initialize a new ToolSequencer with its own lock storage."""
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def run(self, thread_id: str, fn: Callable[[], Awaitable[T]]) -> T:
        """Execute a tool function sequentially for the given thread.

        Args:
            thread_id: The unique identifier for the conversation thread.
            fn: An async function (no arguments) that executes the tool.

        Returns:
            The result of the tool function.
        """
        async with self._locks[thread_id]:
            return await fn()

    def cleanup(self) -> None:
        """Clear all locks in this sequencer.

        Call this when the sequencer is no longer needed.
        """
        self._locks.clear()

    @property
    def active_threads(self) -> int:
        """Get the number of threads with associated locks."""
        return len(self._locks)
