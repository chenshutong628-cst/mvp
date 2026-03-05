"""
HTTP 请求重试工具 - 处理 429 Too Many Requests 错误
"""

from __future__ import annotations

import time
from functools import wraps
from typing import Callable, Any, TypeVar

T = TypeVar("T")


def retry_on_429(
    max_retries: int = 3,
    base_backoff: float = 2.0,
    max_backoff: float = 60.0,
    exceptions: tuple = (Exception,),
):
    """
    针对 429 Too Many Requests 错误的重试装饰器。

    策略：
    - 遇到 429 错误后，等待 2 秒开始重试
    - 每次重试的等待时间指数级递增（2^n）
    - 最大等待时间不超过 60 秒
    - 最多重试 3 次

    Args:
        max_retries: 最大重试次数（包括首次请求）
        base_backoff: 初始等待时间（秒）
        max_backoff: 最大等待时间（秒）
        exceptions: 需要重试的异常类型

    Usage:
        @retry_on_429(max_retries=3)
        def some_function():
            # 函数体，如果遇到 429 错误会自动重试
            pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # 检查是否是 429 错误
                    error_msg = str(e).lower()
                    is_429 = any(code in error_msg for code in ["429", "too many requests", "rate limit"])

                    if not is_429 or attempt == max_retries - 1:
                        # 不是 429 错误，或者是最后一次尝试，直接抛出
                        raise

                    # 计算等待时间（指数退避）
                    backoff = min(base_backoff * (2 ** attempt), max_backoff)
                    time.sleep(backoff)
                    print(f"[Retry] 遇到 429 错误，{attempt + 1}/{max_retries} 次重试，等待 {backoff:.1f}s...")

            # 所有重试都失败
            raise RuntimeError(f"请求失败，重试 {max_retries} 次后仍无法完成") from last_exception

        return wrapper


class RetryStats:
    """重试统计器"""
    def __init__(self):
        self.total_requests = 0
        self.success_count = 0
        self.retry_count = 0
        self._429_errors = 0

    def record_success(self):
        self.total_requests += 1
        self.success_count += 1

    def record_retry(self):
        self.total_requests += 1
        self.retry_count += 1

    def record_429_error(self):
        self.total_requests += 1
        self.retry_count += 1
        self._429_errors += 1

    def reset(self):
        self.total_requests = 0
        self.success_count = 0
        self.retry_count = 0
        self._429_errors = 0

    def summary(self) -> str:
        success_rate = self.success_count / self.total_requests if self.total_requests > 0 else 0
        return (
            f"请求统计:\n"
            f"  - 总请求数: {self.total_requests}\n"
            f"  - 成功数: {self.success_count}\n"
            f"  - 重试数: {self.retry_count}\n"
            f"  - 429 错误数: {self._429_errors}\n"
            f"  - 成功率: {success_rate:.1%}\n"
        )


# 全局统计（用于调试）
_stats = RetryStats()
