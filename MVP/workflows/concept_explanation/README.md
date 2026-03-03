# 讲解概念工作流（Concept Explanation Workflow）

本目录用于存放数学概念讲解相关的配置、Prompt 和案例。

## 工作流说明

讲解概念工作流针对抽象的数学概念（如函数、极限、向量等），通过 LLM 生成的可视化视频帮助理解。

### LLM 阶段划分

与解题工作流相同，但各阶段的侧重点不同：

1. **LLM1 - Analyst（分析阶段）**
   - 输入：概念描述
   - 输出：概念分析（定义、关键属性、直观类比、可视化要点）
   - Prompt: `../../prompts/llm1_analyst/`（可能需要概念特定的覆盖）

2. **LLM2 - Scene Planner（场景规划）**
   - 输入：概念分析
   - 输出：讲解场景规划（引入→定义→性质→应用→总结）
   - Prompt: `../../prompts/llm2_scene_planner/`

3. **LLM3 - Scene Designer（场景设计）**
   - 输入：场景规划
   - 输出：分镜设计（强调动画效果和视觉化）
   - Prompt: `../../prompts/llm3_scene_designer/`

4. **LLM4 - CodeGen（代码生成）**
   - 输入：场景设计
   - 输出：scene.py（Manim 代码，大量使用动态组件）
   - Prompt: `../../prompts/llm4_codegen/`
   - 组件库: `../../prompts/draw/math/geometry/`（动态几何组件）

5. **LLM5 - Fixer（渲染修复）**
   - 输入：渲染错误日志
   - 输出：修复后的代码
   - Prompt: `../../prompts/llm5_fixer/`

## 目录结构

```
concept_explanation/
├── README.md                  # 本文件
├── config.yaml                # 工作流配置（可选）
├── templates/                 # 概念模板
│   ├── function_concept.md    # 函数概念模板
│   ├── limit.md               # 极限概念模板
│   ├── derivative.md          # 导数概念模板
│   ├── vector.md              # 向量概念模板
│   └── solid_geometry.md      # 立体几何概念模板
├── prompts/                   # 工作流特定的 Prompt 覆盖
│   └── overrides/
│       ├── llm1_concept_analyst.md
│       └── llm2_concept_planner.md
└── concepts/                  # 概念案例目录
    └── ellipse_definition/
        ├── concept.md         # 概念描述
        └── output/            # 生成结果
```

## 使用方法

```bash
# 运行概念讲解工作流
cd /path/to/mvp/MVP
python run_mvp.py --requirement-file workflows/concept_explanation/concepts/ellipse_definition/concept.md

# 或者指定运行目录
python run_mvp.py --run-dir workflows/concept_explanation/concepts/ellipse_definition/output
```

## 讲解概念的视频结构建议

典型的概念讲解视频应包含以下场景：

1. **引入场景（10-15秒）**
   - 生活实例或问题引入
   - 为什么需要这个概念

2. **定义场景（20-30秒）**
   - 严格的数学定义
   - 关键术语解释

3. **直观演示（40-60秒）**
   - 动态可视化（使用 DynamicPointOnCurve 等组件）
   - 参数变化对图形的影响
   - 特殊情况展示

4. **性质说明（30-40秒）**
   - 重要性质列表
   - 性质的几何意义

5. **应用示例（30-40秒）**
   - 简单应用场景
   - 与其他概念的联系

6. **总结（10-15秒）**
   - 关键要点回顾
   - 记忆技巧

## 动态组件使用指南

讲解概念时，应大量使用以下动态组件：

- **DynamicPointOnCurve**: 展示点的轨迹运动
- **EllipsePoint**: 椭圆上的参数化运动
- **DynamicTriangle**: 展示三角形的形变
- **DynamicAngle**: 角度的动态变化

示例：
```python
# 展示椭圆参数 t 的几何意义
point = EllipsePoint(a=3, b=2, show_trail=True, label="P")
self.add(point)

# 持续运动一整圈
self.play(
    point.animate_parameter(TAU),
    run_time=8,
    rate_func=linear
)
```
