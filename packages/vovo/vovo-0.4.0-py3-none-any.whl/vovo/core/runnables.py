from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, TypeVar, Union

from vovo.custom_logger import logger

Input = TypeVar("Input")
Output = TypeVar("Output")


class Runnable(Generic[Input, Output], ABC):
    """一个基础可运行单元（Runnable），支持管道式操作、批处理和重试等特性。"""

    def __or__(self, other: Union["Runnable", Callable]) -> "RunnableSequence":
        """支持管道操作符 `|`，并自动将普通函数转换为 `LambdaRunnable`。"""
        if not isinstance(other, Runnable):
            other = LambdaRunnable(other)  # 自动封装为 Runnable
        return RunnableSequence([self, other])

    def map(self, inputs: List[Input]) -> List[Output]:
        """批量处理多个输入，返回对应的多个输出。"""
        return [self.invoke(i) for i in inputs]

    def with_retry(self, attempts: int = 3) -> "RetryRunnable":
        """为当前 Runnable 添加重试机制。"""
        return RetryRunnable(self, attempts)

    @abstractmethod
    def invoke(self, input: Input) -> Output:
        """实现单次调用的逻辑。"""
        pass


class RunnableSequence(Runnable):
    """将多个 Runnable 顺序组合为一个运行链。"""

    def __init__(self, runnable_list: List[Runnable]):
        self.runnable_list = runnable_list

    def invoke(self, input: Any) -> Any:
        """依次执行每个 Runnable，将输出作为下一个的输入。"""
        output = input
        for runnable in self.runnable_list:
            output = runnable.invoke(output)
        return output


class RetryRunnable(Runnable):
    """包装一个 Runnable，为其添加重试机制。"""

    def __init__(self, runnable: Runnable, attempts: int):
        self.runnable = runnable
        self.attempts = attempts

    def invoke(self, input: Input) -> Output:
        """尝试多次执行 Runnable，直到成功或达到最大重试次数。"""
        last_exception = None
        for attempt in range(self.attempts):
            try:
                return self.runnable.invoke(input)
            except Exception as e:
                last_exception = e
                logger.error(f"Retry {attempt + 1} failed: {e}")
        raise last_exception


class LambdaRunnable(Runnable):
    """一个简单的 Runnable，用于包装任意的函数。"""

    def __init__(self, func: Callable[[Input], Output]):
        self.func = func

    def invoke(self, input: Input) -> Output:
        return self.func(input)
