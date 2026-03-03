"""
LLM 类型定义模块。

本模块定义了用于 LLM 调用的核心数据结构：
- Role: 聊天消息的角色类型
- ChatMessage: 通用聊天消息格式
- ZhipuMessage: 智谱 API 消息格式
- LLMBackend: LLM 后端类型标识
- LLMStage: 业务角色到 LLM 后端的映射

注意：
1. 所有类型都使用 dataclass 或 TypedDict，确保类型安全
2. 使用 Literal 类型约束角色只能是 system/user/assistant
3. LLMBackend 和 LLMStage 是 pipeline 配置的核心结构
"""

from __future__ import annotations

import dataclasses
from typing import Literal, TypedDict


# ==================== 聊天消息类型 ====================

Role = Literal["system", "user", "assistant"]


@dataclasses.dataclass(frozen=True)
class ChatMessage:
    """通用聊天消息格式，兼容智谱和 Anthropic。"""
    role: Role
    content: str


class ZhipuMessage(TypedDict):
    """智谱 API 的消息格式。"""
    role: Role
    content: str


# ==================== LLM 后端配置类型 ====================

@dataclasses.dataclass(frozen=True)
class LLMBackend:
    """
    LLM 后端类型标识。

    Attributes:
        name: 后端名称，可选值 "zhipu" 或 "anthropic"
        stage_config: 对应的配置 stage 名称
    """
    name: str  # "zhipu" 或 "anthropic"
    stage_config: str  # 对应的配置 stage 名称


@dataclasses.dataclass(frozen=True)
class LLMStage:
    """
    把"业务角色"映射到 LLM 后端配置。

    支持的后端：
    - zhipu: 使用智谱 AI
    - anthropic: 使用 Anthropic/Claude

    Attributes:
        name: 业务角色名称（如 "analyst", "scene_designer", "codegen" 等）
        backend: LLM 后端配置
        prompt_bundle: prompt bundle 目录名（可选，默认使用 name）
    """
    name: str
    backend: LLMBackend
    prompt_bundle: str | None = None
