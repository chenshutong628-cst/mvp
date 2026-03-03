"""
动态几何点组件。

本模块展示如何在 Manim 中使用 ValueTracker 和 always_redraw
创建动态更新的几何对象。这是实现动画效果的核心模式。

核心概念：
- ValueTracker: 追踪数值变化，用于驱动动画参数
- always_redraw: 每帧重新创建 Mobject，实现实时更新
- updater 函数: 通过 add_updater 添加的更新函数
"""

from __future__ import annotations

from typing import Callable, Any
from manim import *


class DynamicPointOnCurve(VGroup):
    """
    曲线上的动态点组件。

    这是实现几何动画的核心组件。使用 ValueTracker 追踪点的位置参数，
    并通过 always_redraw 在每一帧重新计算点的位置。

    典型用法：
        # 创建椭圆参数方程
        ellipse_curve = lambda t: np.array([
            3 * np.cos(t),
            2 * np.sin(t),
            0
        ])

        # 创建动态点
        moving_point = DynamicPointOnCurve(
            curve_func=ellipse_curve,
            parameter_range=(0, 2 * PI),
            initial_t=0,
            point_color=RED,
            point_radius=0.08,
            show_trail=True,
            trail_length=50
        )

        # 添加到场景
        self.add(moving_point)

        # 动画：移动点
        self.play(
            moving_point.animate_parameter(0.5 * PI),
            run_time=3,
            rate_func=linear
        )

    参数说明：
        curve_func: 曲线参数方程，接受参数 t 返回 np.array([x, y, 0])
        parameter_range: 参数的取值范围 (min, max)
        initial_t: 初始参数值
        point_color: 点的颜色
        point_radius: 点的半径
        show_trail: 是否显示轨迹
        trail_length: 轨迹保留的点数
        label: 点的标签文字（如 "N", "P"）
    """

    def __init__(
        self,
        curve_func: Callable[[float], np.ndarray],
        parameter_range: tuple[float, float] = (0.0, TAU),
        initial_t: float = 0.0,
        point_color: str = RED,
        point_radius: float = 0.08,
        show_trail: bool = False,
        trail_length: int = 50,
        trail_color: str = YELLOW,
        label: str = "",
        label_color: str = WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)

        # 保存曲线函数和参数范围
        self.curve_func = curve_func
        self.t_min, self.t_max = parameter_range

        # 创建 ValueTracker 用于追踪参数 t 的值
        # 这是实现动态更新的核心
        self.t_tracker = ValueTracker(initial_t)

        # 创建点（通过 always_redraw 动态更新）
        self.point = always_redraw(lambda: Dot(
            point=self.curve_func(self.t_tracker.get_value()),
            radius=point_radius,
            color=point_color
        ))
        self.add(self.point)

        # 可选：创建轨迹
        self.trail: VMobject | None = None
        if show_trail:
            self.trail = self._create_trail(
                trail_length=trail_length,
                trail_color=trail_color
            )
            if self.trail:
                self.add(self.trail)

        # 可选：创建标签
        self.label_mobject: Text | None = None
        if label:
            self.label_mobject = always_redraw(lambda: Text(
                label,
                font_size=24,
                color=label_color
            ).next_to(
                self.curve_func(self.t_tracker.get_value()),
                UP + RIGHT,
                buff=0.1
            ))
            self.add(self.label_mobject)

        # 保存配置以便后续使用
        self.point_radius = point_radius
        self.point_color = point_color
        self.show_trail = show_trail
        self.trail_length = trail_length

    def _create_trail(self, trail_length: int, trail_color: str) -> VMobject | None:
        """
        创建轨迹线。

        轨迹是点经过的路径，通过维护一个历史位置列表来实现。
        """
        # 轨迹历史位置列表
        self.trail_points: list[np.ndarray] = []
        self.max_trail_length = trail_length

        # 使用 always_redraw 创建动态轨迹
        trail = always_redraw(lambda: self._update_trail(trail_color))
        return trail

    def _update_trail(self, trail_color: str) -> VMobject:
        """
        更新轨迹。

        每帧调用时，将当前位置添加到历史列表，
        然后绘制连接历史点的虚线。
        """
        current_t = self.t_tracker.get_value()
        current_pos = self.curve_func(current_t)

        # 添加当前位置到历史
        self.trail_points.append(current_pos)

        # 限制轨迹长度
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)

        # 绘制轨迹（虚线）
        if len(self.trail_points) < 2:
            return DashedLine(current_pos, current_pos, color=trail_color)

        trail_line = DashedLine(
            self.trail_points[0],
            self.trail_points[1],
            color=trail_color
        )

        # 逐段连接所有历史点
        for i in range(2, len(self.trail_points)):
            segment = DashedLine(
                self.trail_points[i-1],
                self.trail_points[i],
                color=trail_color
            )
            trail_line = VGroup(trail_line, segment)

        return trail_line

    def animate_parameter(
        self,
        target_t: float,
        run_time: float = 2.0,
        rate_func: Callable[[float], float] = smooth
    ) -> Animation:
        """
        创建参数动画。

        这是一个便捷方法，用于创建将参数 t 从当前值动画到目标值的动画。

        用法：
            self.play(
                moving_point.animate_parameter(PI),
                run_time=3
            )
        """
        current_t = self.t_tracker.get_value()
        return Animati Group(
            self.t_tracker.animate.set_value(target_t),
            run_time=run_time,
            rate_func=rate_func
        )

    def set_parameter(self, t: float) -> None:
        """
        直接设置参数值（无动画）。

        用法：
            moving_point.set_parameter(PI)
        """
        self.t_tracker.set_value(t)

    def get_parameter(self) -> float:
        """获取当前参数值。"""
        return self.t_tracker.get_value()

    def get_position(self) -> np.ndarray:
        """获取当前位置。"""
        return self.curve_func(self.t_tracker.get_value())


class EllipsePoint(DynamicPointOnCurve):
    """
    椭圆上的动态点（专用组件）。

    这是 DynamicPointOnCurve 的特化版本，专门用于椭圆场景。
    提供更直观的接口，直接设置椭圆的半长轴和半短轴。

    典型用法：
        # 创建椭圆上的动点 N
        point_n = EllipsePoint(
            a=4.0,           # 半长轴
            b=3.0,           # 半短轴
            center=ORIGIN,   # 椭圆中心
            initial_t=0,     # 初始参数（弧度）
            label="N",       # 点的标签
            point_color=RED,
            show_trail=True  # 显示轨迹
        )

        # 添加到场景
        self.add(point_n)

        # 动画：点沿椭圆运动
        self.play(
            point_n.animate_parameter(PI / 2),
            run_time=2,
            rate_func=linear
        )

        # 也可以持续运动一整圈
        self.play(
            point_n.animate_parameter(TAU),
            run_time=8,
            rate_func=linear
        )

    参数说明：
        a: 椭圆半长轴长度（x 方向）
        b: 椭圆半短轴长度（y 方向）
        center: 椭圆中心点
        initial_t: 初始参数值（弧度，0 到 2π）
        point_color: 点的颜色
        point_radius: 点的半径
        show_trail: 是否显示运动轨迹
        trail_length: 轨迹保留的点数
        label: 点的标签（如 "N", "P", "M"）
        label_color: 标签文字颜色
    """

    def __init__(
        self,
        a: float = 3.0,
        b: float = 2.0,
        center: np.ndarray = ORIGIN,
        initial_t: float = 0.0,
        point_color: str = RED,
        point_radius: float = 0.08,
        show_trail: bool = False,
        trail_length: int = 50,
        trail_color: str = YELLOW,
        label: str = "",
        label_color: str = WHITE,
        **kwargs
    ):
        # 定义椭圆参数方程
        def ellipse_func(t: float) -> np.ndarray:
            x = center[0] + a * np.cos(t)
            y = center[1] + b * np.sin(t)
            return np.array([x, y, 0.0])

        # 保存椭圆参数供后续使用
        self.a = a
        self.b = b
        self.center = center

        # 调用父类初始化
        super().__init__(
            curve_func=ellipse_func,
            parameter_range=(0.0, TAU),
            initial_t=initial_t,
            point_color=point_color,
            point_radius=point_radius,
            show_trail=show_trail,
            trail_length=trail_length,
            trail_color=trail_color,
            label=label,
            label_color=label_color,
            **kwargs
        )


class DynamicRelation(VGroup):
    """
    动态几何关系组件。

    用于表示两个动态点之间的关系，如连线、距离标注等。
    会在点移动时自动更新。

    典型用法：
        # 创建两个动态点
        point_a = EllipsePoint(a=3, b=2, label="A")
        point_b = EllipsePoint(a=3, b=2, label="B", initial_t=PI)

        # 创建动态连线
        line_ab = DynamicRelation(
            point_a=point_a,
            point_b=point_b,
            relation_type="line",
            color=WHITE,
            stroke_width=2
        )

        self.add(point_a, point_b, line_ab)

        # 动画时连线会自动跟随
        self.play(point_a.animate_parameter(PI))
    """

    def __init__(
        self,
        point_a: DynamicPointOnCurve,
        point_b: DynamicPointOnCurve,
        relation_type: str = "line",
        color: str = WHITE,
        stroke_width: float = 2.0,
        show_distance: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.point_a = point_a
        self.point_b = point_b
        self.relation_type = relation_type
        self.show_distance = show_distance

        # 创建动态连线
        if relation_type == "line":
            self.relation_mobject = always_redraw(
                lambda: Line(
                    start=point_a.get_position(),
                    end=point_b.get_position(),
                    color=color,
                    stroke_width=stroke_width
                )
            )
            self.add(self.relation_mobject)

        # 可选：显示距离标注
        self.distance_text: Text | None = None
        if show_distance:
            self.distance_text = always_redraw(
                lambda: Text(
                    f"{np.linalg.norm(point_a.get_position() - point_b.get_position()):.2f}",
                    font_size=20,
                    color=color
                ).move_to(
                    (point_a.get_position() + point_b.get_position()) / 2
                )
            )
            self.add(self.distance_text)
