# 布局契约（layout_contract v1）

你必须在输出 JSON 顶层提供 `layout_contract` 字段，用于把“布局描述”升级为“可执行约束”。

## 目标

1) 防止文本/公式重叠  
2) 防止对象越界  
3) 明确每一步对象的出现与消失（生命周期）  
4) 为 LLM4 提供可直接落地的布局规则

## 必须输出的结构

```json
{
  "layout_contract": {
    "version": "v1",
    "language": "zh-CN",
    "safe_margin": 0.4,
    "zones": [
      {"id": "title_zone", "x0": 0.05, "y0": 0.88, "x1": 0.95, "y1": 0.98},
      {"id": "main_zone", "x0": 0.05, "y0": 0.15, "x1": 0.62, "y1": 0.86},
      {"id": "formula_zone", "x0": 0.65, "y0": 0.20, "x1": 0.95, "y1": 0.86},
      {"id": "summary_zone", "x0": 0.05, "y0": 0.03, "x1": 0.95, "y1": 0.13}
    ],
    "global_rules": {
      "avoid_overlap": true,
      "min_gap": 0.18,
      "formula_stack": "arrange_down",
      "max_formula_width_ratio": 0.30,
      "overflow_policy": ["shrink", "move_down", "split_next_step"],
      "text_language": "chinese_only_except_symbols"
    },
    "objects": [
      {
        "id": "title_1",
        "kind": "text",
        "zone": "title_zone",
        "priority": 100,
        "max_width_ratio": 0.85
      },
      {
        "id": "eq_main",
        "kind": "math",
        "zone": "formula_zone",
        "priority": 80,
        "max_width_ratio": 0.30
      }
    ],
    "step_visibility": [
      {"step": 1, "show": ["title_1"], "hide": []},
      {"step": 2, "show": ["eq_main"], "hide": []}
    ]
  }
}
```

## 约束说明

1) `zones` 使用归一化坐标（0~1）描述画面分区。  
2) `objects` 中每个对象都要绑定 `zone`。  
3) 公式对象必须有 `max_width_ratio`，防止长公式越界。  
4) `step_visibility` 必须覆盖关键对象，避免旧元素残留堆叠。  
5) 文案默认中文；符号标签可保留 `L1/L2/L3/L4/P/Q/E/B_1/B_2/v_0`。

## 与 motion_constraints 的关系

- `layout_contract` 负责”放哪里、何时显示”。
- `motion_constraints` 负责”怎么动、到哪里结束”。
- 两者都必须输出，且不冲突。

---

## 【数学解题专用 - 3x3 九宫格布局模式】

### 布局说明

当进行数学解题讲解时，使用”左文右图”的 3x3 九宫格布局：

```
┌─────────────────────────────────┐
│  题目区 (Question Zone)     │  [2x1, 左上]
│  x0: 0.05, y0: 0.15        │  占宽 66%, 占高 33%
│  x1: 0.66, y1: 0.48        │
├─────────────┬───────────────┤
│  推导讲解区 │  几何作图区    │
│(Explanation) │   (Graph)       │
│  [2x2, 左下] │  [1x3, 右列]  │
│  x0: 0.05,  │  x0: 0.67,   │
│  y0: 0.50,  │  y0: 0.00,   │
│  x1: 0.66,  │  x1: 1.00,   │
│  y1: 0.83   │  y1: 1.00   │
└─────────────┴───────────────┘
```

### 各区域规则

#### 1. 题目区（Question Zone）
- **位置**：左上角 2x1 区域
- **坐标**：`x0: 0.05, y0: 0.15, x1: 0.66, y1: 0.48`
- **占用**：宽度 66%，高度 33%
- **定位方法**：使用 `.to_corner(UL)` 定位到左上角
- **内容**：题目文本，分行显示
- **宽度限制**：每个元素必须限制宽度（使用 `max_width_ratio`）

#### 2. 推导讲解区（Explanation Zone）
- **位置**：左下角 2x2 区域
- **坐标**：`x0: 0.05, y0: 0.50, x1: 0.66, y1: 0.83`
- **占用**：宽度 66%，高度 66%
- **定位方法**：
  - 使用 `.next_to(..., DOWN)` 紧接题目区下方
  - 使用 `.to_edge(LEFT)` 靠左对齐
- **内容**：
  - 推导步骤（公式 + 文字）
  - 结论性文字
- **排列**：使用 `VGroup(...).arrange(DOWN, buff=...)` 垂直排列
- **清理**：切换到图形场景时，必须清空此区域

#### 3. 几何作图区（Graph Zone）
- **位置**：右侧 1x3 整列区域
- **坐标**：`x0: 0.67, y0: 0.00, x1: 1.00, y1: 1.00`
- **占用**：宽度 33%，高度 100%
- **定位方法**：使用 `.to_edge(RIGHT)` 靠右对齐
- **坐标系要求**：
  - `Axes` 对象必须被缩放并限制在右半边
  - 通常使用 `x_range=[-a-1, a], y_range=[-b, b]` 的范围
  - 坐标系中心点应在 `(x0 + x1) / 2` 位置附近
- **内容**：
  - 坐标系（Axes）
  - 几何图形（椭圆、直线、点、三角形等）
  - 标注（点标签、线段标注）
- **动态更新**：动点、动态线段使用 `always_redraw`

### 输出格式要求

当选择 3x3 Grid 模式时，必须在 `layout_contract` 中指定：

```json
{
  “layout_contract”: {
    “version”: “grid_3x3”,
    “language”: “zh-CN”,
    “mode”: “math_problem_solving”,
    “zones”: [
      {“id”: “question_zone”, “x0”: 0.05, “y0”: 0.15, “x1”: 0.66, “y1”: 0.48},
      {“id”: “explanation_zone”, “x0”: 0.05, “y0”: 0.50, “x1”: 0.66, “y1”: 0.83},
      {“id”: “graph_zone”, “x0”: 0.67, “y0”: 0.00, “x1”: 1.00, “y1”: 1.00}
    ],
    “global_rules”: {
      “avoid_overlap”: true,
      “min_gap”: 0.18,
      “formula_stack”: “arrange_down”,
      “max_formula_width_ratio”: 0.28,  // 题目区文字
      “explanation_max_width_ratio”: 0.60,  // 推导区文字
      “graph_padding”: 0.10,
      “text_language”: “chinese_only_except_symbols”
    },
    “objects”: [
      // 题目区对象
      {
        “id”: “question_text”,
        “kind”: “text”,
        “zone”: “question_zone”,
        “priority”: 100,
        “max_width_ratio”: 0.28
      },

      // 推导区对象
      {
        “id”: “explanation_formula”,
        “kind”: “math”,
        “zone”: “explanation_zone”,
        “priority”: 80,
        “max_width_ratio”: 0.60
      },

      // 几何区对象
      {
        “id”: “axes_graph”,
        “kind”: “axes”,
        “zone”: “graph_zone”,
        “priority”: 90,
        “scale”: 0.85
      }
    ]
  }
}
```

### 区域切换规则

- **场景 1-2**（题目展示）：使用 question_zone + graph_zone
  - explanation_zone 保持为空
- **场景 3-N**（推导过程）：使用 question_zone（保留题目）+ explanation_zone
  - graph_zone 显示辅助图形
- **最后场景**（总结）：清空 explanation_zone，只保留题目区和图形区关键元素

### Manim 实现要点

1. **题目区实现**：
   ```python
   question_text = Text(“题目内容”, font_size=20, color=WHITE)
   question_text.to_corner(UL).shift(RIGHT * 0.05 + DOWN * 0.15)
   # 限制宽度
   if question_text.width > config.frame_width * 0.28:
       question_text.scale_to_width(config.frame_width * 0.28)
   ```

2. **推导区实现**：
   ```python
   explanation = VGroup(
       MathTex(r”\frac{AB}{AC} = ...”),
       Text(“根据相似三角形”)
   ).arrange(DOWN, buff=0.2)
   explanation.next_to(question_text, DOWN).to_edge(LEFT)
   # 限制宽度
   if explanation.width > config.frame_width * 0.60:
       explanation.scale_to_width(config.frame_width * 0.60)
   ```

3. **几何区实现**：
   ```python
   axes = Axes(
       x_range=[-5, 5],
       y_range=[-4, 4],
       x_length=6,  # 限制宽度
       y_length=8
   ).to_edge(RIGHT).shift(LEFT * 0.15)

   # 动点使用 always_redraw
   point_p = always_redraw(lambda: Dot(...))
   self.add(axes, point_p)
   ```
