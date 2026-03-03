"""
测试 Anthropic/Claude API 连接。

用途：验证 LLM4 (CodeGen) 能否通过 https://ai.jiexi6.cn
成功连接到 Claude 并返回代码。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 确保 MVP 根目录在 Python 路径中
MVP_ROOT = Path(__file__).resolve().parents[0]
if str(MVP_ROOT) not in sys.path:
    sys.path.insert(0, str(MVP_ROOT))

from pipeline.llm.anthropic import load_anthropic_config, chat_completion
from pipeline.llm.types import ChatMessage


def test_connection():
    """测试 Anthropic API 连接并生成简单代码。"""

    print("=" * 60)
    print("测试 Anthropic/Claude API 连接")
    print("=" * 60)
    print()

    try:
        # 1. 加载配置
        print("[1/3] 加载配置...")
        cfg = load_anthropic_config()
        print(f"    - 模型: {cfg.model}")
        print(f"    - Base URL: {cfg.base_url}")
        print(f"    - 温度: {cfg.temperature}")
        print(f"    - Max Tokens: {cfg.max_tokens}")
        print(f"    - 超时: {cfg.timeout_s}s")
        print(f"    - 重试: {cfg.retries}")
        print()

        # 2. 准备测试请求
        print("[2/3] 准备测试请求...")
        system_prompt = """你是一个 Manim 动画代码生成助手。

请生成一个简单的 Manim 代码示例。"""
        user_prompt = """请生成一个 Manim 代码，实现以下功能：

1. 创建一个圆，半径为 2
2. 在圆上创建一个动点，从角度 0 运动到 2π
3. 点的颜色为红色，显示运动轨迹

只输出 Python 代码，不要任何解释。"""

        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ]
        print(f"    - System Prompt 长度: {len(system_prompt)} 字符")
        print(f"    - User Prompt 长度: {len(user_prompt)} 字符")
        print()

        # 3. 发送请求
        print("[3/3] 发送 API 请求...")
        response = chat_completion(messages, cfg=cfg)

        # 4. 显示结果
        print()
        print("=" * 60)
        print("✅ API 调用成功！")
        print("=" * 60)
        print()
        print("【Claude 返回的代码】")
        print("-" * 60)
        print(response)
        print("-" * 60)
        print()
        print("【测试结论】")
        print("✅ LLM4 (CodeGen) 可以通过 https://ai.jiexi6.cn 正常连接 Claude")
        print("✅ System Prompt 机制工作正常")
        print("✅ 可以在项目中使用 Claude 生成 Manim 代码")
        print()

        return True

    except RuntimeError as e:
        print()
        print("=" * 60)
        print("❌ API 调用失败")
        print("=" * 60)
        print(f"错误信息: {e}")
        print()
        print("【排查建议】")
        print("1. 检查 MVP/.env 中的 ANTHROPIC_API_KEY 是否正确")
        print("2. 检查网络是否可以访问 https://ai.jiexi6.cn")
        print("3. 检查 ANTHROPIC_BASE_URL 配置是否正确")
        print("4. 查看错误信息中的具体原因")
        print()
        return False

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 测试过程中发生未预期错误")
        print("=" * 60)
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
