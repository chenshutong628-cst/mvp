"""
动态几何关系组件。

本模块提供动态更新的几何关系，如线段、角度、三角形等。
这些组件会自动跟随关联的动态点更新。
"""

from __future__ import annotations

from manim import *


class DynamicLine(VGroup):
    """
    动态线段组件。

    连接两个动态点，并在点移动时自动更新。

    典型用法：
        # 创建两个动态点
        point_m = EllipsePoint(a=3, b=2, label="M")
        point_n = EllipsePoint(a=3, b=2, initial_t=PI/2, label="N")

        # 创建动态连线
        line_mn = DynamicLine(
            point_a=point_m,
            point_b=point_n,
            color=WHITE,
            stroke_width=2,
            add_arrow=False
        )

        self.add(point_m, point_n, line_mn)

        # 动画：线段会自动跟随点移动
        self.play(point_n.animate_parameter(PI))

    参数说明：
        point_a: 第一个动态点
        point_b: 第二个动态点
        color: 线段颜色
        stroke_width: 线段宽度
        add_arrow: 是否添加箭头
        arrow_size: 箭头大小
    """

    def __init__(
        self,
        point_a: "DynamicPointOnCurve",
        point_b: "DynamicPointOnCurve",
        color: str = WHITE,
        stroke_width: float = 2.0,
        add_arrow: bool = False,
        arrow_size: float = 0.2,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.point_a = point_a
        self.point_b = point_b
        self.add_arrow = add_arrow

        # 使用 always_redraw 创建动态线段
        if add_arrow:
            self.line = always_redraw(lambda: Arrow(
                start=point_a.get_position(),
                end=point_b.get_position(),
                color=color,
                stroke_width=stroke_width,
                buff=0,
                max_tip_length_to_length_ratio=arrow_size
            ))
        else:
            self.line = always_redraw(lambda: Line(
                start=point_a.get_position(),
                end=point_b.get_position(),
                color=color,
                stroke_width=stroke_width
            ))

        self.add(self.line)

    def get_length(self) -> float:
        """获取当前线段长度。"""
        return float(np.linalg.norm(
            self.point_a.get_position() - self.point_b.get_position()
        ))


class DynamicSegment(DynamicLine):
    """
    动态线段（带长度标注）。

    与 DynamicLine 类似，但可以显示线段长度。

    典型用法：
        segment_ab = DynamicSegment(
            point_a=point_a,
            point_b=point_b,
            color=WHITE,
            stroke_width=2,
            show_length=True,
            length_color=YELLOW
        )

        self.add(segment_ab)
    """

    def __init__(
        self,
        point_a: "DynamicPointOnCurve",
        point_b: "DynamicPointOnCurve",
        color: str = WHITE,
        stroke_width: float = 2.0,
        show_length: bool = True,
        length_color: str = YELLOW,
        length_decimal_places: int = 2,
        length_font_size: int = 20,
        **kwargs
    ):
        super().__init__(
            point_a=point_a,
            point_b=point_b,
            color=color,
            stroke_width=stroke_width,
            **kwargs
        )

        # 可选：长度标注
        self.length_label: Text | None = None
        if show_length:
            self.length_label = always_redraw(
                lambda: Text(
                    f"{self.get_length():.{length_decimal_places}f}",
                    font_size=length_font_size,
                    color=length_color
                ).next_to(
                    (point_a.get_position() + point_b.get_position()) / 2,
                    UP,
                    buff=0.1
                )
            )
            self.add(self.length_label)


class DynamicAngle(VGroup):
    """
    动态角度标注组件。

    标注三个点形成的角度，并在点移动时自动更新。

    典型用法：
        # 创建三个点
        point_a = EllipsePoint(a=3, b=2, label="A")
        point_o = EllipsePoint(a=3, b=2, label="O", initial_t=PI/3)
        point_b = EllipsePoint(a=3, b=2, label="B", initial_t=PI*2/3)

        # 标注 ∠AOB
        angle_aob = DynamicAngle(
            vertex_point=point_o,
            ray1_point=point_a,
            ray2_point=point_b,
            angle_radius=0.5,
            color=YELLOW,
            show_label=True,
            label_text="θ"
        )

        self.add(point_a, point_o, point_b, angle_aob)

    参数说明：
        vertex_point: 角的顶点
        ray1_point: 角的第一条边上的点
        ray2_point: 角的第二条边上的点
        angle_radius: 角度标注弧线的半径
        color: 标注颜色
        stroke_width: 线宽
        show_label: 是否显示角度标签
        label_text: 标签文字
        label_color: 标签颜色
        label_font_size: 标签字号
    """

    def __init__(
        self,
        vertex_point: "DynamicPointOnCurve",
        ray1_point: "DynamicPointOnCurve",
        ray2_point: "DynamicPointOnCurve",
        angle_radius: float = 0.5,
        color: str = YELLOW,
        stroke_width: float = 2.0,
        show_label: bool = True,
        label_text: str = "",
        label_color: str = WHITE,
        label_font_size: int = 24,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.vertex_point = vertex_point
        self.ray1_point = ray1_point
        self.ray2_point = ray2_point
        self.angle_radius = angle_radius

        # 创建动态角度弧线
        self.arc = always_redraw(lambda: self._create_angle_arc(
            color=color,
            stroke_width=stroke_width
        ))
        self.add(self.arc)

        # 可选：创建标签
        self.label: Text | None = None
        if show_label:
            label_str = label_text
            if not label_str:
                # 如果没有指定标签，使用角度值
                label_str = always_redraw(lambda: Text(
                    f"{self.get_angle_degrees():.1f}°",
                    font_size=label_font_size,
                    color=label_color
                ))
            else:
                self.label = always_redraw(lambda: Text(
                    label_text,
                    font_size=label_font_size,
                    color=label_color
                ).move_to(self._get_label_position()))

            if isinstance(self.label, Text):
                pass  # 已经是 always_redraw 包装的
            else:
                self.add(self.label)

    def _create_angle_arc(self, color: str, stroke_width: float) -> Arc:
        """创建角度弧线。"""
        vertex = self.vertex_point.get_position()
        ray1_vec = self.ray1_point.get_position() - vertex
        ray2_vec = self.ray2_point.get_position() - vertex

        # 计算起始角度
        start_angle = np.arctan2(ray1_vec[1], ray1_vec[0])
        end_angle = np.arctan2(ray2_vec[1], ray2_vec[0])

        # 确保角度是正数且小于 2π
        angle_diff = end_angle - start_angle
        if angle_diff < 0:
            angle_diff += 2 * PI

        # 创建弧线
        arc = Arc(
            radius=self.angle_radius,
            start_angle=start_angle,
            angle=angle_diff,
            color=color,
            stroke_width=stroke_width
        ).move_arc_center_to(vertex)

        return arc

    def _get_label_position(self) -> np.ndarray:
        """计算标签位置（在角平分线上）。"""
        vertex = self.vertex_point.get_position()
        ray1_vec = self.ray1_point.get_position() - vertex
        ray2_vec = self.ray2_point.get_position() - vertex

        # 计算角平分线方向
        ray1_unit = ray1_vec / np.linalg.norm(ray1_vec)
        ray2_unit = ray2_vec / np.linalg.norm(ray2_vec)
        bisector = ray1_unit + ray2_unit
        bisector = bisector / np.linalg.norm(bisector)

        # 标签位置：顶点 + 角平分线方向 * 稍大半径
        return vertex + bisector * (self.angle_radius * 1.3)

    def get_angle_radians(self) -> float:
        """获取当前角度（弧度）。"""
        vertex = self.vertex_point.get_position()
        ray1_vec = self.ray1_point.get_position() - vertex
        ray2_vec = self.ray2_point.get_position() - vertex

        # 使用点积计算角度
        cos_angle = np.dot(ray1_vec, ray2_vec) / (
            np.linalg.norm(ray1_vec) * np.linalg.norm(ray2_vec)
        )
        # 限制在 [-1, 1] 范围内，避免数值误差
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        return float(np.arccos(cos_angle))

    def get_angle_degrees(self) -> float:
        """获取当前角度（度）。"""
        return float(np.degrees(self.get_angle_radians()))


class DynamicTriangle(VGroup):
    """
    动态三角形组件。

    由三个动态点构成的三角形，会自动跟随点移动更新。

    典型用法：
        # 创建三个点
        point_a = EllipsePoint(a=3, b=2, label="A")
        point_b = EllipsePoint(a=3, b=2, label="B", initial_t=2*PI/3)
        point_c = EllipsePoint(a=3, b=2, label="C", initial_t=4*PI/3)

        # 创建动态三角形
        triangle_abc = DynamicTriangle(
            point_a=point_a,
            point_b=point_b,
            point_c=point_c,
            color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.3
        )

        self.add(point_a, point_b, point_c, triangle_abc)

    参数说明：
        point_a, point_b, point_c: 三角形的三个顶点
        color: 边框颜色
        stroke_width: 边框宽度
        fill_color: 填充颜色
        fill_opacity: 填充透明度
    """

    def __init__(
        self,
        point_a: "DynamicPointOnCurve",
        point_b: "DynamicPointOnCurve",
        point_c: "DynamicPointOnCurve",
        color: str = WHITE,
        stroke_width: float = 2.0,
        fill_color: str = BLACK,
        fill_opacity: float = 0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c

        # 创建动态多边形
        self.triangle = always_redraw(lambda: Polygon(
            point_a.get_position(),
            point_b.get_position(),
            point_c.get_position(),
            color=color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity
        ))

        self.add(self.triangle)

    def get_area(self) -> float:
        """
        计算三角形面积（海伦公式或向量叉积）。

        使用向量叉积：面积 = 0.5 * |AB × AC|
        """
        a = self.point_a.get_position()
        b = self.point_b.get_position()
        c = self.point_c.get_position()

        # 向量 AB 和 AC
        ab = b - a
        ac = c - a

        # 2D 叉积（z 分量）
        cross = ab[0] * ac[1] - ab[1] * ac[0]

        return float(abs(cross) * 0.5)

    def get_perimeter(self) -> float:
        """计算三角形周长。"""
        a = self.point_a.get_position()
        b = self.point_b.get_position()
        c = self.point_c.get_position()

        ab = np.linalg.norm(b - a)
        bc = np.linalg.norm(c - b)
        ca = np.linalg.norm(a - c)

        return float(ab + bc + ca)
