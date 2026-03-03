# LLM 引擎分工调整 - 完成总结

## 已完成的修改

### 1. 环境变量配置 (`MVP/.env`)

已新增 Claude 相关环境变量：

```bash
# Anthropic/Claude API Key（用于 LLM4 CodeGen 和 LLM5 Fixer）
ANTHROPIC_API_KEY=sk-be8543debae25769bd75cf3c5abebdd1829fdb967de0a213dba7868ef7323490

# Claude 模型（默认：claude-sonnet-4-6）
CLAUDE_MODEL=claude-sonnet-4-6

# Anthropic API Base URL（自定义网关）
ANTHROPIC_BASE_URL=https://ai.jiexi6.cn
```

### 2. 新增 Anthropic API 适配 (`pipeline/llm/anthropic.py`)

- 完整的 Anthropic/Claude API 调用实现
- 支持 OpenAI 兼容格式和 Anthropic 原生格式
- 自动根据 URL 判断使用哪种格式
- 包含完整的配置加载、重试机制

### 3. 更新类型定义 (`pipeline/llm/types.py`)

- 新增 `LLMBackend` 数据类，用于标识 LLM 后端
- 支持 `zhipu` 和 `anthropic` 两种后端

### 4. 更新 LLMClient (`pipeline/llm_client.py`)

- 修改 `LLLMStage` 数据类，从 `zhipu_stage` 改为 `backend` 字段
- 更新 `_cfg` 方法，根据 backend 加载对应配置
- 更新 `chat` 方法，根据 backend 调用不同的 API

### 5. 更新 Pipeline 模型路由 (`pipeline/run_mvp.py`)

修改 `build_client()` 函数，实现以下分工：

| LLM 阶段 | 角色 | 后端 | API |
|-----------|------|--------|-----|
| LLM1 | Analyst | zhipu | 智谱 AI |
| LLM2 | Scene Planner | zhipu | 智谱 AI |
| LLM3 | Scene Designer | zhipu | 智谱 AI |
| LLM4 | CodeGen | **anthropic** | **Claude** |
| LLM5 | Fixer | **anthropic** | **Claude** |

### 6. 创建测试脚本 (`MVP/test_anthropic_connection.py`)

独立的连接测试脚本，用于验证：
- 配置是否正确加载
- API 网关是否可访问
- Claude API 调用是否成功
- System Prompt 机制是否工作

## 核心文件修改列表

| 文件 | 修改内容 |
|------|---------|
| `MVP/.env` | 新增 ANTHROPIC_API_KEY、CLAUDE_MODEL、ANTHROPIC_BASE_URL |
| `MVP/pipeline/llm/anthropic.py` | 新增文件，完整 Anthropic API 实现 |
| `MVP/pipeline/llm/types.py` | 新增 LLMBackend 类 |
| `MVP/pipeline/llm_client.py` | 修改 LLMStage 结构，支持多 backend |
| `MVP/pipeline/run_mvp.py` | 修改 build_client()，切换 LLM4/5 到 Claude |
| `MVP/test_anthropic_connection.py` | 新增测试脚本 |
| `MVP/pipeline/llm/zhipu.py` | 修改 load_zhipu_config() 使用 override=True |

## ⚠️ 需要确认的问题

### 网关 API 端点问题

当前测试中发现，`https://ai.jiexi6.cn` 网关需要确认正确的 API 端点路径。

**已测试的端点：**

1. `/v1/chat/completions` (OpenAI 格式) → 返回 HTML，不是 API 响应
2. `/v1/responses` (Anthropic 格式) → HTTP 400 错误，提示不支持的路径
3. `/v1/messages` (Anthropic 格式) → HTTP 404 错误

**需要师兄确认：**

1. `https://ai.jiexi6.cn` 的正确 API 端点是什么？
2. 是否需要特殊的请求格式（如特定的 Header 或认证方式）？
3. 网关是否同时支持 OpenAI 和 Anthropic 格式？

**临时解决方案：**

如果网关确实使用 OpenAI 兼容格式，可以尝试：
- `/chat/completions`
- 或者要求在 `.env` 中配置完整的 API URL（包含端点）

## 使用方法

### 1. 确认网关配置

请师兄确认正确的 API 端点，然后更新 `MVP/.env` 中的 `ANTHROPIC_BASE_URL`。

例如，如果正确端点是 `/chat/completions`：

```bash
ANTHROPIC_BASE_URL=https://ai.jiexi6.cn/chat/completions
```

### 2. 运行测试

```bash
cd /Users/chenshutong/Desktop/mvp/mvp/MVP
python test_anthropic_connection.py
```

### 3. 运行完整 Pipeline

测试通过后，可以正常使用 MVP 生成视频：

```bash
cd /Users/chenshutong/Desktop/mvp/mvp/MVP
python run_mvp.py --requirement "你的需求"
```

## 技术说明

### Anthropic vs OpenAI 格式

**Anthropic 原生格式：**
```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 8192,
  "temperature": 0.2,
  "system": "系统提示词",  // 顶级参数
  "messages": [
    {"role": "user", "content": "用户消息"}
  ]
}
```

**OpenAI 兼容格式：**
```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 8192,
  "temperature": 0.2,
  "messages": [
    {"role": "system", "content": "系统提示词"},  // 在 messages 数组中
    {"role": "user", "content": "用户消息"}
  ]
}
```

当前实现会根据 URL 自动判断使用哪种格式，并设置对应的 Header：
- Anthropic 格式：`x-api-key`
- OpenAI 格式：`Authorization: Bearer ...`

### System Prompt 注入

通过 `MVP/prompts/llm4_codegen/bundle.md` 注入的 System Prompt 会在：
- Anthropic 格式：作为 `system` 顶级参数传入
- OpenAI 格式：作为 `messages[0]` 传入（role="system"）

两种方式都能正确工作，确保 bundle.md 机制继续有效。
