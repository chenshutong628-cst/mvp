"""
Anthropic/Claude API 适配模块。

使用 Anthropic 官方 Python SDK，支持自定义网关和 SSL 证书绕过。
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Literal

import httpx
from anthropic import Anthropic

from ..config import load_llm_yaml
from ..env import load_dotenv

from .types import ChatMessage


@dataclass(frozen=True)
class AnthropicConfig:
    """Anthropic/Claude API 配置。"""

    model: str
    temperature: float
    max_tokens: int
    timeout_s: int
    retries: int
    retry_backoff_s: float
    base_url: str


def _load_anthropic_raw() -> dict[str, Any]:
    raw = load_llm_yaml() or {}
    return raw.get("anthropic", {}) or {}


def _to_bool(value: str | bool | None, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def load_anthropic_config() -> AnthropicConfig:
    """
    优先级：
    1) 环境变量（包含 .env，强制覆盖）
    2) MVP/configs/llm.yaml
    3) 内置默认值
    """

    # 注意：使用 override=True 确保 .env 中的配置优先
    load_dotenv(override=True)
    anthropic = _load_anthropic_raw()

    model = os.environ.get("CLAUDE_MODEL") or str(
        anthropic.get("model", "claude-sonnet-4-6")
    )
    temperature = float(
        os.environ.get("ANTHROPIC_TEMPERATURE")
        or anthropic.get("temperature", 0.2)
    )
    max_tokens = int(
        os.environ.get("ANTHROPIC_MAX_TOKENS")
        or anthropic.get("max_tokens", 8192)
    )
    timeout_s = int(
        os.environ.get("ANTHROPIC_TIMEOUT_S")
        or anthropic.get("timeout_s", 240)
    )
    retries = int(
        os.environ.get("ANTHROPIC_RETRIES")
        or anthropic.get("retries", 2)
    )
    retry_backoff_s = float(
        os.environ.get("ANTHROPIC_RETRY_BACKOFF_S")
        or anthropic.get("retry_backoff_s", 1.5)
    )

    # 注意：Anthropic 官方 API 使用的是 https://api.anthropic.com
    # 但我们需要通过自定义网关 https://ai.jiexi6.cn 访问
    base_url = (
        os.environ.get("ANTHROPIC_BASE_URL")
        or anthropic.get("base_url", "https://api.anthropic.com")
    )

    return AnthropicConfig(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout_s=timeout_s,
        retries=max(0, retries),
        retry_backoff_s=max(0.1, retry_backoff_s),
        base_url=base_url,
    )


def _build_anthropic_config(
    base_cfg: AnthropicConfig, overrides: dict[str, Any]
) -> AnthropicConfig:
    model = str(overrides.get("model", base_cfg.model))
    temperature = float(overrides.get("temperature", base_cfg.temperature))
    max_tokens = int(overrides.get("max_tokens", base_cfg.max_tokens))
    timeout_s = int(overrides.get("timeout_s", base_cfg.timeout_s))
    retries = int(overrides.get("retries", base_cfg.retries))
    retry_backoff_s = float(overrides.get("retry_backoff_s", base_cfg.retry_backoff_s))
    base_url = str(overrides.get("base_url", base_cfg.base_url))

    return AnthropicConfig(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout_s=timeout_s,
        retries=max(0, retries),
        retry_backoff_s=max(0.1, retry_backoff_s),
        base_url=base_url,
    )


def load_anthropic_stage_config(
    stage: str,
    mode: Literal["generate", "continue", "repair"],
    *,
    base_cfg: AnthropicConfig | None = None,
) -> AnthropicConfig:
    """
    读取 stage/mode 特定采样配置：
    anthropic.stages.<stage>.<mode> = {temperature, ...}
    """

    base = base_cfg or load_anthropic_config()
    anthropic = _load_anthropic_raw()

    stages = anthropic.get("stages", {}) or {}
    if not isinstance(stages, dict):
        return base

    stage_cfg = stages.get(stage, {}) or {}
    if not isinstance(stage_cfg, dict):
        return base

    mode_cfg = stage_cfg.get(mode, {}) or {}
    if not isinstance(mode_cfg, dict):
        return base

    return _build_anthropic_config(base, mode_cfg)


def _get_api_key() -> str:
    """获取并清洗 API Key，去除隐形字符和引号。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "缺少 Anthropic API key：请在 MVP/.env 中设置 ANTHROPIC_API_KEY=..."
        )

    # 严格清洗：去除首尾空白、去除引号
    api_key = api_key.strip().strip('"').strip("'")

    if not api_key:
        raise RuntimeError(
            "Anthropic API key 清洗后为空，请检查 .env 配置"
        )

    return api_key


def _create_client(cfg: AnthropicConfig, api_key: str) -> Anthropic:
    """
    创建 Anthropic 客户端，支持自定义网关和 SSL 绕过。

    使用 httpx.Client(verify=False) 绕过 macOS SSL 证书验证问题。
    """
    # 创建不验证 SSL 的 httpx 客户端
    http_client = httpx.Client(
        verify=False,
        timeout=httpx.Timeout(cfg.timeout_s),
    )

    client = Anthropic(
        api_key=api_key,
        base_url=cfg.base_url,
        http_client=http_client,
    )

    # 调试：打印客户端配置
    print(f"[调试] Anthropic 客户端初始化:")
    print(f"[调试]   - Base URL: {cfg.base_url}")
    print(f"[调试]   - API Key (前 10 字符): {api_key[:10]}...")
    print(f"[调试]   - SSL Verify: False")
    print(f"[调试]   - Timeout: {cfg.timeout_s}s")

    return client


def chat_completion(
    messages: list[ChatMessage],
    *,
    cfg: AnthropicConfig | None = None,
) -> str:
    """
    调用 Anthropic/Claude API（原生格式）。

    使用直接 httpx 请求，支持自定义网关。
    自动处理：
    - /v1/messages 端点
    - x-api-key header
    - anthropic-version header
    - system 作为顶级参数
    """

    load_dotenv()
    cfg = cfg or load_anthropic_config()
    api_key = _get_api_key()

    # 构建完整 URL：确保包含 /v1/messages
    base_url_clean = cfg.base_url.rstrip("/")
    url = f"{base_url_clean}/v1/messages"

    # 分离 system 消息和其他消息
    system_content = ""
    api_messages = []
    for msg in messages:
        if msg.role == "system":
            system_content = msg.content
        else:
            api_messages.append({"role": msg.role, "content": msg.content})

    # 构建 payload
    payload = {
        "model": cfg.model,
        "max_tokens": cfg.max_tokens,
        "temperature": cfg.temperature,
        "system": system_content,
        "messages": api_messages,
    }

    # 设置请求头
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    raw: str | None = None
    last_exc: Exception | None = None
    total_attempts = cfg.retries + 1

    for attempt in range(total_attempts):
        try:
            # 使用直接 httpx 请求（绕过 SSL 验证以支持自定义网关）
            with httpx.Client(verify=False, timeout=cfg.timeout_s) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

            # 提取文本内容
            content = data.get("content", [])
            for block in content:
                if block.get("type") == "text":
                    raw = block.get("text", "")
                    break

            if raw:
                return raw

            raise RuntimeError("Anthropic 返回空内容")

        except Exception as e:
            last_exc = e

            # 检查是否是可重试的错误（5xx 错误或网络错误）
            is_retryable = (
                hasattr(e, "status_code") and 500 <= e.status_code <= 599
            ) or isinstance(
                e,
                (
                    httpx.TimeoutException,
                    httpx.NetworkError,
                    httpx.ConnectError,
                ),
            )

            if not is_retryable or attempt >= total_attempts - 1:
                raise RuntimeError(f"Anthropic API 调用失败: {e}") from e

            # 退避重试
            sleep_s = cfg.retry_backoff_s * (2**attempt)
            time.sleep(sleep_s)

    if last_exc is not None:
        raise RuntimeError(f"Anthropic 请求失败（重试 {total_attempts} 次后仍失败）") from last_exc

    raise RuntimeError("Anthropic 请求失败（未知错误）")
