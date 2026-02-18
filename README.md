# Manim 立体几何组件库

一个基于 Manim 的立体几何可视化组件库，符合中国高中数学教材标准。

## ✨ 特性

- 🎯 **绝对中心构建法** - 所有组件基于绝对数学中心，确保 100% 几何精确
- 📐 **斜二测画法** - 符合中国高中教材标准
- 🎨 **视觉优化** - 虚实分明，立体感强
- 🔧 **易于使用** - 统一的 API 设计
- 📚 **完整文档** - 每个组件都有详细的使用说明

## 📦 组件列表

### 多面体 (Polyhedra)

| 组件 | 类名 | 说明 |
|------|------|------|
| 正方体 | `CubeOblique` | 斜二测正方体 |
| 长方体 | `CuboidOblique` | 斜二测长方体 |
| 四棱锥 | `PyramidOblique` | 斜二测正四棱锥 |
| 三棱锥 | `TetrahedronOblique` | 斜二测正三棱锥 |
| 三棱柱 | `PrismOblique` | 斜二测直三棱柱 |

### 旋转体 (Solids of Revolution)

| 组件 | 类名 | 说明 |
|------|------|------|
| 圆柱 | `CylinderOblique` | 斜二测圆柱 |
| 圆锥 | `ConeOblique` | 斜二测圆锥（精确切点） |
| 圆台 | `FrustumOblique` | 斜二测圆台 |
| 球体 | `SphereOblique` | 斜二测球体（美术增强版） |

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd mvp

# 安装依赖
pip install manim
```

### 使用示例

```python
from manim import *
from components.solid_geometry import CylinderOblique, SphereOblique

class MyScene(Scene):
    def construct(self):
        # 创建圆柱
        cylinder = CylinderOblique(
            radius=2.0,
            height=3.5,
            skew_factor=0.4,
            show_axes=True,
            show_labels=True
        )
        self.add(cylinder)

        # 创建球体（增强版）
        sphere = SphereOblique(
            radius=2.0,
            show_meridian=True,              # 显示本初子午线
            show_intersection_dots=True      # 显示穿刺点
        ).shift(RIGHT * 5)
        self.add(sphere)
```

### 渲染

```bash
# 渲染场景
manim -pql my_scene.py MyScene
```

## 📖 详细文档

每个组件的详细文档请查看 `components/solid_geometry/` 目录下的对应文件。

### 组件参数

所有组件都支持以下通用参数：

- `show_axes`: 是否显示坐标轴（默认 True）
- `show_labels`: 是否显示标签（默认 True）
- `center`: 绝对中心位置（默认 ORIGIN）

### 特殊参数

**球体组件增强功能：**

```python
sphere = SphereOblique(
    radius=2.0,
    skew_factor=0.3,
    show_meridian=True,              # 新增：显示本初子午线
    show_intersection_dots=True      # 新增：显示穿刺点
)
```

## 🏗️ 项目结构

```
mvp/
├── components/
│   └── solid_geometry/
│       ├── __init__.py              # 模块导出
│       ├── cube.py                  # 正方体
│       ├── cuboid.py                # 长方体
│       ├── pyramid.py               # 棱锥
│       ├── prism.py                 # 三棱柱
│       ├── cylinder.py              # 圆柱
│       ├── cone.py                  # 圆锥
│       ├── frustum.py               # 圆台
│       ├── sphere.py                # 球体
│       └── *.md                     # 文档
├── tests/
│   └── test_cube.py                 # 测试场景
└── README.md
```

## 🎓 核心技术

### 绝对中心构建法

所有组件采用"绝对中心构建法"，定义绝对的数学中心，所有组件基于此点生成。

```python
# 示例：圆柱组件
self.p_center = center                  # 🔑 底面圆心（定海神针）
self.p_left = self.p_center + LEFT * radius
self.p_right = self.p_center + RIGHT * radius
self.p_top_center = self.p_center + UP * height
```

### about_point 缩放修复

为避免椭圆裂缝，所有缩放操作都指定 `about_point` 参数：

```python
arc.stretch(skew_factor, dim=1, about_point=p_center)
```

### 解析几何求交点

球体组件的坐标轴交点通过解析几何精确计算：

```python
# X 轴与椭圆交点
x_intersect = - (a * b) / np.sqrt(b**2 + a**2 * k**2)
y_intersect = k * x_intersect
```

## 📝 开发日志

- **2026-02-19**: 初始版本发布
  - 完成所有基础组件
  - 球体组件美术增强
  - 统一代码风格和架构

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Manim 数学组件库

---

**享受使用！** 🎉
