"""
动态几何组件使用示例。

本文件展示如何使用动态几何组件创建动画。
这些示例会被 LLM 学习，用于生成类似的代码。
"""

from manim import *
from prompts.draw.math.geometry import (
    EllipsePoint,
    DynamicLine,
    DynamicTriangle,
    DynamicAngle,
    Ellipse,
)


class EllipseMotionExample(Scene):
    """
    椭圆动点运动示例。

    展示如何使用 ValueTracker 和 always_redraw 创建动态几何动画。
    """

    def construct(self):
        # 1. 创建椭圆
        ellipse = Ellipse(a=4, b=3, color=BLUE, stroke_width=3)
        self.add(ellipse)

        # 2. 创建右顶点 A（静态点）
        point_a = Dot(point=[4, 0, 0], color=WHITE, radius=0.08)
        label_a = Text("A", font_size=24).next_to(point_a, RIGHT, buff=0.1)
        self.add(point_a, label_a)

        # 3. 创建椭圆上的动点 M（使用 EllipsePoint）
        point_m = EllipsePoint(
            a=4,
            b=3,
            initial_t=0,
            label="M",
            point_color=RED,
            point_radius=0.08,
            show_trail=True,
            trail_length=50
        )
        self.add(point_m)

        # 4. 创建另一个动点 N
        point_n = EllipsePoint(
            a=4,
            b=3,
            initial_t=PI / 2,
            label="N",
            point_color=YELLOW,
            point_radius=0.08
        )
        self.add(point_n)

        # 5. 创建动态连线（会自动跟随点移动）
        line_am = DynamicLine(point_a=point_m, point_b=point_a, color=WHITE)
        line_an = DynamicLine(point_a=point_n, point_b=point_a, color=WHITE)
        line_mn = DynamicLine(point_a=point_m, point_b=point_n, color=GREEN)

        self.add(line_am, line_an, line_mn)

        # 6. 创建动态三角形
        triangle_amn = DynamicTriangle(
            point_a=point_m,
            point_b=point_a,
            point_c=point_n,
            color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.2
        )
        self.add(triangle_amn)

        # 7. 动画：点 M 沿椭圆运动
        self.play(
            point_m.animate_parameter(PI),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)

        # 8. 动画：两个点同时运动
        self.play(
            point_m.animate_parameter(TAU),
            point_n.animate_parameter(3 * PI / 2),
            run_time=6,
            rate_func=linear
        )


class AngleAnimationExample(Scene):
    """
    动态角度标注示例。

    展示如何使用 DynamicAngle 组件。
    """

    def construct(self):
        # 创建椭圆和三个点
        ellipse = Ellipse(a=3, b=2, color=BLUE)
        self.add(ellipse)

        point_o = EllipsePoint(a=3, b=2, initial_t=0, label="O")
        point_a = EllipsePoint(a=3, b=2, initial_t=PI / 6, label="A")
        point_b = EllipsePoint(a=3, b=2, initial_t=PI / 3, label="B")

        self.add(point_o, point_a, point_b)

        # 创建角度标注
        angle_aob = DynamicAngle(
            vertex_point=point_o,
            ray1_point=point_a,
            ray2_point=point_b,
            angle_radius=0.6,
            color=YELLOW,
            show_label=True,
            label_text="θ"
        )
        self.add(angle_aob)

        # 动画：点 A 和 B 运动，角度会自动更新
        self.play(
            point_a.animate_parameter(PI / 2),
            point_b.animate_parameter(2 * PI / 3),
            run_time=4
        )


class EllipseWithFoci(Scene):
    """
    带焦点的椭圆示例。

    展示椭圆的第一定义：到两焦点距离之和为常数。
    """

    def construct(self):
        # 1. 创建椭圆并显示焦点
        a, b = 4, 3
        ellipse = Ellipse(a=a, b=b, color=BLUE, stroke_width=3)
        ellipse.show_foci_points(color=YELLOW, radius=0.06)
        self.add(ellipse)

        # 2. 创建椭圆上的动点 P
        point_p = EllipsePoint(
            a=a,
            b=b,
            initial_t=0,
            label="P",
            point_color=RED,
            show_trail=True
        )
        self.add(point_p)

        # 3. 创建焦点（静态）
        c = np.sqrt(a**2 - b**2)
        focus_f1 = Dot(point=[-c, 0, 0], color=YELLOW, radius=0.06)
        focus_f2 = Dot(point=[c, 0, 0], color=YELLOW, radius=0.06)
        label_f1 = Text("F₁", font_size=20).next_to(focus_f1, DOWN, buff=0.1)
        label_f2 = Text("F₂", font_size=20).next_to(focus_f2, DOWN, buff=0.1)

        self.add(focus_f1, focus_f2, label_f1, label_f2)

        # 4. 连接 PF₁ 和 PF₂（需要手动创建，因为焦点是静态点）
        # 这里展示如何混合使用静态点和动态点
        line_pf1 = always_redraw(lambda: Line(
            start=point_p.get_position(),
            end=focus_f1.get_center(),
            color=WHITE,
            stroke_width=1.5
        ))
        line_pf2 = always_redraw(lambda: Line(
            start=point_p.get_position(),
            end=focus_f2.get_center(),
            color=WHITE,
            stroke_width=1.5
        ))

        self.add(line_pf1, line_pf2)

        # 5. 显示距离和
        distance_text = always_redraw(lambda: Text(
            f"|PF₁| + |PF₂| = {2 * a:.1f}",
            font_size=24,
            color=WHITE
        ).to_edge(UP))

        self.add(distance_text)

        # 6. 动画：点 P 绕椭圆运动一整圈
        self.play(
            point_p.animate_parameter(TAU),
            run_time=10,
            rate_func=linear
        )


class ComplexGeometryAnimation(Scene):
    """
    复杂几何动画示例。

    展示多个动态组件的组合使用。
    """

    def construct(self):
        # 设置背景
        self.camera.background_color = BLACK

        # 1. 创建两个相交的椭圆
        ellipse1 = Ellipse(a=4, b=3, color=BLUE, stroke_width=2)
        ellipse2 = Ellipse(a=3, b=4, color=GREEN, stroke_width=2)
        self.add(ellipse1, ellipse2)

        # 2. 在第一个椭圆上创建动点 M
        point_m = EllipsePoint(
            a=4,
            b=3,
            initial_t=0,
            label="M",
            point_color=RED,
            show_trail=True,
            trail_length=30
        )

        # 3. 在第二个椭圆上创建动点 N
        point_n = EllipsePoint(
            a=3,
            b=4,
            initial_t=PI / 2,
            label="N",
            point_color=YELLOW,
            show_trail=True,
            trail_length=30
        )

        self.add(point_m, point_n)

        # 4. 创建动态连线
        line_mn = DynamicLine(
            point_a=point_m,
            point_b=point_n,
            color=WHITE,
            stroke_width=2
        )

        # 5. 标注原点 O
        origin = Dot(point=ORIGIN, color=WHITE, radius=0.06)
        label_o = Text("O", font_size=20).next_to(origin, DOWN + LEFT)
        self.add(origin, label_o)

        # 6. 创建动态角度 ∠MON
        # 需要创建原点上的动点引用
        class FixedPoint:
            """将静态点包装成类似 DynamicPointOnCurve 的接口。"""
            def __init__(self, position: np.ndarray):
                self.position = position

            def get_position(self) -> np.ndarray:
                return self.position

        fixed_origin = FixedPoint(ORIGIN)
        angle_mon = DynamicAngle(
            vertex_point=fixed_origin,
            ray1_point=point_m,
            ray2_point=point_n,
            angle_radius=0.5,
            color=YELLOW
        )

        self.add(line_mn, angle_mon)

        # 7. 添加说明文字
        title = Text("椭圆上的动点", font_size=36).to_edge(UP)
        self.add(title)

        # 8. 动画：两个点同时运动
        self.play(
            point_m.animate_parameter(2 * PI),
            point_n.animate_parameter(2 * PI),
            run_time=12,
            rate_func=linear
        )
