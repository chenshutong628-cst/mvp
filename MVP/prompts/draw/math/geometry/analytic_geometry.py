"""
解析几何图形组件。

本模块提供常见解析几何曲线的标准 Manim 实现。
所有组件都支持与 DynamicPointOnCurve 配合使用。
"""

from __future__ import annotations

from typing import Callable
from manim import *


class Ellipse(VGroup):
    """
    椭圆组件。

    标准椭圆：x²/a² + y²/b² = 1

    典型用法：
        # 创建椭圆
        ellipse = Ellipse(
            a=4.0,           # 半长轴
            b=3.0,           # 半短轴
            center=ORIGIN,
            color=BLUE,
            stroke_width=3
        )

        self.add(ellipse)

        # 可以在椭圆上放置动态点
        moving_point = EllipsePoint(a=4.0, b=3.0, label="P")

    参数说明：
        a: 半长轴长度（x 方向半轴）
        b: 半短轴长度（y 方向半轴）
        center: 椭圆中心坐标
        color: 轮廓颜色
        stroke_width: 轮廓线宽
        fill_color: 填充颜色（可选）
        fill_opacity: 填充透明度（0-1）
    """

    def __init__(
        self,
        a: float = 3.0,
        b: float = 2.0,
        center: np.ndarray = ORIGIN,
        color: str = BLUE,
        stroke_width: float = 3.0,
        fill_color: str = BLACK,
        fill_opacity: float = 0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.a = a
        self.b = b
        self.center = center

        # 使用 Manim 内置的 Ellipse
        # 注意：Manim 的 Ellipse 参数是 width 和 height
        self.ellipse = manim_Ellipse(
            width=2 * a,
            height=2 * b,
            color=color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity
        ).move_to(center)

        self.add(self.ellipse)

        # 可选：绘制焦点
        self.foci: list[Dot] = []
        self.show_foci = False

    def get_foci(self) -> list[np.ndarray]:
        """
        计算椭圆焦点位置。

        对于标准椭圆 x²/a² + y²/b² = 1：
        - 若 a ≥ b（长轴在 x 方向）：
          焦点在 (±c, 0)，其中 c² = a² - b²
        - 若 b > a（长轴在 y 方向）：
          焦点在 (0, ±c)，其中 c² = b² - a²
        """
        a, b, center = self.a, self.b, self.center

        if a >= b:
            # 长轴在 x 方向
            c = np.sqrt(a**2 - b**2)
            return [
                np.array([center[0] + c, center[1], 0.0]),
                np.array([center[0] - c, center[1], 0.0])
            ]
        else:
            # 长轴在 y 方向
            c = np.sqrt(b**2 - a**2)
            return [
                np.array([center[0], center[1] + c, 0.0]),
                np.array([center[0], center[1] - c, 0.0])
            ]

    def show_foci_points(self, color: str = YELLOW, radius: float = 0.05) -> None:
        """显示椭圆焦点。"""
        if self.show_foci:
            return  # 已经显示

        foci_positions = self.get_foci()

        for pos in foci_positions:
            focus_dot = Dot(point=pos, radius=radius, color=color)
            self.foci.append(focus_dot)
            self.add(focus_dot)

        self.show_foci = True


class Hyperbola(VGroup):
    """
    双曲线组件。

    标准双曲线：x²/a² - y²/b² = 1（横向开口）

    典型用法：
        # 创建双曲线
        hyperbola = Hyperbola(
            a=2.0,
            b=1.5,
            center=ORIGIN,
            branches="both",  # "left", "right", "both"
            color=GREEN,
            stroke_width=3
        )

        self.add(hyperbola)

    参数说明：
        a: 实半轴长度
        b: 虚半轴长度
        center: 双曲线中心
        branches: 显示哪些分支（"left", "right", "both"）
        color: 轮廓颜色
        stroke_width: 轮廓线宽
        t_range: 参数 t 的范围（用于绘制曲线）
    """

    def __init__(
        self,
        a: float = 2.0,
        b: float = 1.5,
        center: np.ndarray = ORIGIN,
        branches: str = "both",
        color: str = GREEN,
        stroke_width: float = 3.0,
        t_range: tuple[float, float] = (-2.5, 2.5),
        **kwargs
    ):
        super().__init__(**kwargs)

        self.a = a
        self.b = b
        self.center = center

        # 双曲线参数方程：x = a*sec(t), y = b*tan(t)
        # 使用参数方程绘制
        t_min, t_max = t_range

        def hyperbola_point(t: float, branch_sign: float = 1.0) -> np.ndarray:
            """计算双曲线上的点。"""
            x = a * np.cosh(t) * branch_sign
            y = b * np.sinh(t)
            return np.array([center[0] + x, center[1] + y, 0.0])

        # 绘制分支
        if branches in ("right", "both"):
            right_branch = ParametricFunction(
                lambda t: hyperbola_point(t, 1.0),
                t_range=[t_min, t_max],
                color=color,
                stroke_width=stroke_width
            )
            self.add(right_branch)

        if branches in ("left", "both"):
            left_branch = ParametricFunction(
                lambda t: hyperbola_point(t, -1.0),
                t_range=[t_min, t_max],
                color=color,
                stroke_width=stroke_width
            )
            self.add(left_branch)

    def get_foci(self) -> list[np.ndarray]:
        """
        计算双曲线焦点位置。

        对于 x²/a² - y²/b² = 1：
        焦点在 (±c, 0)，其中 c² = a² + b²
        """
        c = np.sqrt(self.a**2 + self.b**2)
        return [
            np.array([self.center[0] + c, self.center[1], 0.0]),
            np.array([self.center[0] - c, self.center[1], 0.0])
        ]


class Parabola(VGroup):
    """
    抛物线组件。

    标准抛物线：y² = 4px（开口方向取决于 p 的符号）

    典型用法：
        # 创建开口向右的抛物线
        parabola = Parabola(
            p=1.0,           # 焦准距
            vertex=ORIGIN,
            direction="right",  # "up", "down", "left", "right"
            color=YELLOW,
            stroke_width=3
        )

        self.add(parabola)

    参数说明：
        p: 焦准距（焦点到顶点的距离）
        vertex: 抛物线顶点
        direction: 开口方向
        color: 轮廓颜色
        stroke_width: 轮廓线宽
        t_range: 参数 t 的范围
    """

    def __init__(
        self,
        p: float = 1.0,
        vertex: np.ndarray = ORIGIN,
        direction: str = "right",
        color: str = YELLOW,
        stroke_width: float = 3.0,
        t_range: tuple[float, float] = (-3.0, 3.0),
        **kwargs
    ):
        super().__init__(**kwargs)

        self.p = p
        self.vertex = vertex
        self.direction = direction

        t_min, t_max = t_range

        # 根据开口方向选择参数方程
        if direction == "right":
            # y² = 4px → 参数方程：x = pt², y = 2pt
            func = lambda t: np.array([
                vertex[0] + p * t**2,
                vertex[1] + 2 * p * t,
                0.0
            ])
        elif direction == "left":
            # y² = -4px
            func = lambda t: np.array([
                vertex[0] - p * t**2,
                vertex[1] + 2 * p * t,
                0.0
            ])
        elif direction == "up":
            # x² = 4py
            func = lambda t: np.array([
                vertex[0] + 2 * p * t,
                vertex[1] + p * t**2,
                0.0
            ])
        elif direction == "down":
            # x² = -4py
            func = lambda t: np.array([
                vertex[0] + 2 * p * t,
                vertex[1] - p * t**2,
                0.0
            ])
        else:
            raise ValueError(f"Unknown direction: {direction}")

        parabola_curve = ParametricFunction(
            func,
            t_range=[t_min, t_max],
            color=color,
            stroke_width=stroke_width
        )
        self.add(parabola_curve)

    def get_focus(self) -> np.ndarray:
        """获取抛物线焦点位置。"""
        p, vertex, direction = self.p, self.vertex, self.direction

        if direction == "right":
            return np.array([vertex[0] + p, vertex[1], 0.0])
        elif direction == "left":
            return np.array([vertex[0] - p, vertex[1], 0.0])
        elif direction == "up":
            return np.array([vertex[0], vertex[1] + p, 0.0])
        elif direction == "down":
            return np.array([vertex[0], vertex[1] - p, 0.0])
        else:
            return vertex


class Circle(VGroup):
    """
    圆组件（椭圆的特例）。

    典型用法：
        circle = Circle(
            radius=2.0,
            center=ORIGIN,
            color=WHITE,
            stroke_width=2
        )

        self.add(circle)
    """

    def __init__(
        self,
        radius: float = 1.0,
        center: np.ndarray = ORIGIN,
        color: str = WHITE,
        stroke_width: float = 2.0,
        fill_color: str = BLACK,
        fill_opacity: float = 0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.radius = radius
        self.center = center

        self.circle = manim_Circle(
            radius=radius,
            color=color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity
        ).move_to(center)

        self.add(self.circle)
