"""
测试模块导入问题。
"""
import sys

# 确保使用 Python 3
print(f"Python 版本: {sys.version}")
print(f"执行文件: {__file__}")
print()

# 测试 1: 直接导入 types
print("测试 1: 直接导入 types...")
try:
    from pipeline.llm.types import LLMBackend, LLMStage
    print("✅ LLMBackend, LLMStage 导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 测试 2: 导入 llm_client
print("测试 2: 导入 llm_client...")
try:
    from pipeline.llm_client import LLMClient
    print("✅ LLMClient 导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 测试 3: 完整导入
print("测试 3: 完整导入...")
try:
    from pipeline.run_mvp import build_client
    print("✅ build_client 导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
