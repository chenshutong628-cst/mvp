# 解题工作流（Problem Solving Workflow）

本目录用于存放数学题目解题相关的配置、Prompt 和案例。

## 工作流说明

解题工作流针对具体的数学题目（如高考题、竞赛题），通过 LLM 分工协作生成完整的解题视频。

### LLM 阶段划分

1. **LLM1 - Analyst（分析阶段）**
   - 输入：题目需求（problem.md）
   - 输出：explanation.txt（已知条件、目标、解题步骤）
   - Prompt: `../../prompts/llm1_analyst/`

2. **LLM2 - Scene Planner（场景规划）**
   - 输入：题目需求 + explanation.txt
   - 输出：scene_plan.json（场景拆分、时长分配）
   - Prompt: `../../prompts/llm2_scene_planner/`

3. **LLM3 - Scene Designer（场景设计）**
   - 输入：场景规划
   - 输出：scene_designs.json（分镜级设计）
   - Prompt: `../../prompts/llm3_scene_designer/`

4. **LLM4 - CodeGen（代码生成）**
   - 输入：场景设计
   - 输出：scene.py（Manim 代码）
   - Prompt: `../../prompts/llm4_codegen/`
   - 组件库: `../../prompts/draw/math/geometry/`

5. **LLM5 - Fixer（渲染修复）**
   - 输入：渲染错误日志
   - 输出：修复后的代码
   - Prompt: `../../prompts/llm5_fixer/`

## 目录结构

```
problem_solving/
├── README.md                  # 本文件
├── config.yaml                # 工作流配置（可选）
├── templates/                 # 题目模板
│   ├── analytic_geometry.md   # 解析几何题模板
│   ├── solid_geometry.md      # 立体几何题模板
│   └── function.md            # 函数题模板
├── prompts/                   # 工作流特定的 Prompt 覆盖（可选）
│   └── overrides/
└── cases/                     # 案例目录
    └── example_001/
        ├── problem.md         # 题目描述
        └── output/            # 生成结果
```

## 使用方法

```bash
# 运行解题工作流
cd /path/to/mvp/MVP
python run_mvp.py --requirement-file workflows/problem_solving/cases/example_001/problem.md

# 或者指定运行目录
python run_mvp.py --run-dir workflows/problem_solving/cases/example_001/output
```

## 与讲解概念工作流的区别

| 特性 | 解题工作流 | 讲解概念工作流 |
|------|-----------|---------------|
| 输入 | 具体数学题目 | 数学概念/定义 |
| 输出 | 解题过程视频 | 概念讲解视频 |
| LLM1 侧重点 | 分析题目条件 | 概念拆解与类比 |
| 场景风格 | 逻辑推导、步骤展示 | 直观演示、动画说明 |
| 典型时长 | 3-8 分钟 | 2-5 分钟 |
