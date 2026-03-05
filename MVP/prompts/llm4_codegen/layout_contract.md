# 布局契约执行规范（LLM4）

输入中的 `scene_designs.scenes[*].layout_contract` 是硬约束。  
你必须按契约生成代码，而不是仅参考自然语言布局描述。

## 必须执行

1) 解析 `layout_contract.zones`：建立标题区/主图区/公式区/总结区。
2) 解析 `layout_contract.objects`：每个对象按 `zone` 放置，并遵守 `max_width_ratio`。
3) 解析 `layout_contract.step_visibility`：按步显示/隐藏对象，避免叠屏。
4) 执行 `global_rules.avoid_overlap=true`：使用包围盒检测避免重叠。
5) 执行 `global_rules.formula_stack=arrange_down`：多条公式必须分组竖排。
6) 执行 `global_rules.text_language`：自然语言文本默认中文（符号标签除外）。

## V5 视觉终极打磨强制要求

### 空间拉宽（充分利用 16:9 画布）

**左侧文本组（Title Zone + Explanation Zone）：**
- 必须强制使用 `.to_edge(LEFT, buff=0.5)` 定位
- 绝对禁止居中堆叠，文本内容必须紧贴左边缘

**右侧坐标系与图形组（Graph Zone）：**
- 必须强制使用 `.to_edge(RIGHT, buff=0.5)` 定位
- 绝对禁止居中堆叠，图形内容必须紧贴右边缘

### 消除畸变（确保几何图形比例正确）

**构建 Axes 时的强制要求：**
1. 必须锁定 x 轴和 y 轴的单位长度为 1:1
2. 通过精确控制 x_length 和 y_length 实现比例锁定
3. 计算公式：x_length / y_length = (x_range[1] - x_range[0]) / (y_range[1] - y_range[0])
4. 绝对禁止随意设置 x_length 和 y_length 导致图形畸变

## 推荐实现模式

```python
# 1) 分区锚点（V5：空间拉宽，使用 buff=0.5）
title_anchor = LEFT * 0.5 + UP * 2.5
formula_anchor = LEFT * 0.5 + DOWN * 1.0
graph_anchor = RIGHT * 0.5

# 2) 公式组统一排版，避免硬编码堆叠
formula_group = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
formula_group.to_edge(LEFT, buff=0.5)  # V5：空间拉宽

# 3) 超宽对象自动缩放
if formula_group.width > config.frame_width * 0.30:
    formula_group.scale_to_fit_width(config.frame_width * 0.30)

# 4) V5：消除畸变，构建 Axes 时锁定 x 轴和 y 轴单位长度为 1:1
x_range = [-5, 5]
y_range = [-4, 4]
x_range_length = x_range[1] - x_range[0]  # 10
y_range_length = y_range[1] - y_range[0]  # 8
# 设置 x_length 和 y_length 保持 1:1 单位长度比例
x_length = 6.0
y_length = 6.0 * (y_range_length / x_range_length)  # 4.8

axes = Axes(
    x_range=x_range,
    y_range=y_range,
    x_length=x_length,
    y_length=y_length
).to_edge(RIGHT, buff=0.5)  # V5：空间拉宽
```

## 防重叠最低要求

1) 不允许出现“同一帧中两条公式互相覆盖”。  
2) 不允许标题与公式覆盖。  
3) 不允许总结文字覆盖主图关键对象。  
4) 若对象过多：优先拆到下一步，不要同帧硬塞。

## 与 motion_constraints 协同

- 布局契约只管“放置与显隐”；  
- 运动约束只管“轨迹与锚点命中”；  
- 代码中必须同时满足两者。
