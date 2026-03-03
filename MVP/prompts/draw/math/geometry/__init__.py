"""
Manim 数学几何组件库。

本模块提供标准的几何图形组件，支持静态和动态渲染。

核心组件：
- DynamicPointOnCurve: 曲线上的动态点（使用 ValueTracker 和 always_redraw）
- EllipsePoint: 椭圆上的动态点（专用组件）
- DynamicLine: 连接两个动态点的线段
- DynamicSegment: 带长度标注的动态线段
- DynamicAngle: 动态角度标注
- DynamicTriangle: 动态三角形
- Ellipse, Hyperbola, Parabola: 解析几何曲线
"""

from .dynamic_point_on_curve import (
    DynamicPointOnCurve,
    EllipsePoint,
    DynamicRelation,
)
from .dynamic_geometric_relations import (
    DynamicLine,
    DynamicSegment,
    DynamicAngle,
    DynamicTriangle,
)
from .analytic_geometry import (
    Ellipse,
    Hyperbola,
    Parabola,
    Circle as ManimCircle,
)

__all__ = [
    # 动态点组件
    "DynamicPointOnCurve",
    "EllipsePoint",
    "DynamicRelation",
    # 动态关系组件
    "DynamicLine",
    "DynamicSegment",
    "DynamicAngle",
    "DynamicTriangle",
    # 解析几何组件
    "Ellipse",
    "Hyperbola",
    "Parabola",
    "ManimCircle",
]
