# 椭圆概念讲解模板

## 概念信息

**概念名称**: 椭圆
**所属领域**: 解析几何
**预计时长**: 3-5 分钟
**目标受众**: 高中生

## 概念描述

```
[在此处描述要讲解的椭圆概念]

示例：讲解椭圆的定义、标准方程、几何性质
```

## 讲解要点

### 1. 引入（10-15秒）
- 生活实例：行星轨道、水杯倾斜时的水面
- 为什么需要研究椭圆

### 2. 定义（20-30秒）
- 第一定义：平面内与两个定点 F1、F2 的距离之和等于常数（大于 |F1F2|）的点的轨迹
- 第二定义（焦半径定义）：平面内与一个定点的距离和一条定直线的距离之比是常数 e (0<e<1) 的点的轨迹

### 3. 标准方程（30-40秒）
- 焦点在 x 轴：x²/a² + y²/b² = 1
- 焦点在 y 轴：y²/a² + x²/b² = 1
- 参数 a、b、c 的几何意义和关系：c² = a² - b²

### 4. 直观演示（60-90秒）
- **动态展示 1**：使用绳子画椭圆（第一定义的可视化）
- **动态展示 2**：参数 t 的几何意义（点 P = (a cos t, b sin t) 的运动）
- **动态展示 3**：离心率 e 对椭圆形状的影响

### 5. 重要性质（30-40秒）
- 对称性：关于 x 轴、y 轴、原点对称
- 顶点、焦点、准线
- 焦半径公式
- 焦点三角形面积

### 6. 应用示例（20-30秒）
- 简单应用：求椭圆方程
- 实际应用：天体运行轨道

### 7. 总结（10-15秒）
- 关键要点回顾
- 记忆技巧：长轴、短轴、焦距的关系

## 动态组件使用建议

```python
# 展示椭圆参数化
from prompts.draw.math.geometry import EllipsePoint, Ellipse, DynamicTriangle

# 创建椭圆
ellipse = Ellipse(a=4, b=3, color=BLUE)

# 创建动态点展示参数 t
point_p = EllipsePoint(a=4, b=3, label="P", show_trail=True)

# 动画：点沿椭圆运动
self.play(point_p.animate_parameter(TAU), run_time=8, rate_func=linear)

# 展示焦点三角形
f1 = Dot(point=[-c, 0, 0], color=YELLOW)
f2 = Dot(point=[c, 0, 0], color=YELLOW)
triangle_f1pf2 = DynamicTriangle(
    point_a=f1,
    point_b=point_p,
    point_c=f2,
    fill_color=BLUE,
    fill_opacity=0.3
)
```

## 运行命令

```bash
python MVP/run_mvp.py --requirement-file workflows/concept_explanation/concepts/ellipse/concept.md
```
