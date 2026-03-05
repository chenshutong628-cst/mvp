from manim import *
import numpy as np

class MainScene(Scene):
    def construct(self):
        # Title zone - 题目常驻
        title_text = VGroup(
            Text("已知椭圆 C: x²/a² + y²/b² = 1 (a > b > 0) 过点 M(2,3)，", font_size=18),
            Text("点 A 为其左顶点，且 AM 的斜率为 1/2。", font_size=18),
            Text("1. 求 C 的方程；", font_size=18),
            Text("2. 点 N 为椭圆上任意一点，求 △AMN 的面积的最大值。", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        title_text.to_corner(UL).shift(RIGHT * 0.3 + DOWN * 0.2)
        self.add(title_text)

        # Graph zone - 坐标系与椭圆
        # 强制 1:1 等距坐标系（X轴和Y轴单位长度完全一致）
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 5, 1],
            x_length=6,          # X轴长度=6（X轴跨度12）→ unit_size = 0.5
            y_length=5,          # Y轴长度=5（Y轴跨度10）→ unit_size = 0.5
            axis_config={"color": GREY, "stroke_width": 1}
        ).to_edge(RIGHT).shift(LEFT * 0.5)
        self.add(axes)

        # 椭圆 x²/16 + y²/12 = 1
        # 强制使用 unit_size 约束椭圆大小（数学尺寸 * 坐标系单位物理长度）
        ellipse = Ellipse(
            width=8 * axes.x_axis.unit_size,           # 横向半径 = 4 * unit_size = 4 * 0.5 = 2
            height=4 * np.sqrt(3) * axes.y_axis.unit_size,  # 纵向半径 = 2√3 * unit_size = 2 * 0.5 = 1
            color=BLUE,
            stroke_width=2
        ).move_to(axes.c2p(0, 0))
        self.play(Create(ellipse), run_time=1)

        # 点 A(-4, 0) 和 M(2, 3)
        point_a = Dot(axes.c2p(-4, 0), color=WHITE, radius=0.06)
        label_a = Text("A", font_size=16).next_to(point_a, DOWN, buff=0.1)
        point_m = Dot(axes.c2p(2, 3), color=WHITE, radius=0.06)
        label_m = Text("M", font_size=16).next_to(point_m, UP, buff=0.1)
        self.play(FadeIn(point_a, label_a, point_m, label_m), run_time=0.5)

        # Scene 01-02: 求 a
        q1_step1 = VGroup(
            Text("根据斜率公式：", font_size=20),
            MathTex(r"k_{AM} = \frac{3}{2+a} = \frac{1}{2}", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step1.next_to(title_text, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(q1_step1), run_time=1)
        self.wait(0.5)

        q1_step2 = MathTex(r"\Rightarrow a = 4", font_size=20).next_to(q1_step1, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(q1_step2), run_time=0.8)
        self.wait(0.5)

        # Scene 03: 求 b
        q1_step3 = VGroup(
            Text("将 M(2,3) 代入椭圆方程：", font_size=20),
            MathTex(r"\frac{4}{16} + \frac{9}{b^2} = 1", font_size=18),
            MathTex(r"\Rightarrow b^2 = 12", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step3.next_to(q1_step2, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q1_step3), run_time=1.5)
        self.wait(0.5)

        # Scene 04: 椭圆方程与直线 AM
        q1_step4 = VGroup(
            Text("椭圆方程：", font_size=20),
            MathTex(r"\frac{x^2}{16} + \frac{y^2}{12} = 1", font_size=18),
            Text("直线 AM: x - 2y + 4 = 0", font_size=18),
            MathTex(r"|AM| = 3\sqrt{5}", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step4.next_to(q1_step3, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q1_step4), run_time=1.5)
        self.wait(1)

        # 直线 AM
        line_am = Line(axes.c2p(-4, 0), axes.c2p(2, 3), color=WHITE, stroke_width=1.5)
        self.play(Create(line_am), run_time=0.5)
        self.wait(0.5)

        # 擦黑板 - 清除第一问
        self.play(FadeOut(q1_step1, q1_step2, q1_step3, q1_step4), run_time=0.5)

        # Scene 05-08: 第二问 - 动点 N 与面积最值
        theta_tracker = ValueTracker(0.0)

        def ellipse_point(t):
            x = 4 * np.cos(t)
            y = 2 * np.sqrt(3) * np.sin(t)
            return axes.c2p(x, y)

        point_n = always_redraw(lambda: Dot(ellipse_point(theta_tracker.get_value()), color=RED, radius=0.08))
        label_n = always_redraw(lambda: Text("N", font_size=16, color=RED).next_to(ellipse_point(theta_tracker.get_value()), UP + RIGHT, buff=0.1))
        self.add(point_n, label_n)

        # 动态三角形
        triangle = always_redraw(lambda: Polygon(
            axes.c2p(-4, 0),
            axes.c2p(2, 3),
            ellipse_point(theta_tracker.get_value()),
            stroke_color=GREEN,
            stroke_width=1.5,
            fill_color=GREEN,
            fill_opacity=0.2
        ))
        self.add(triangle)

        # 动态面积显示
        def get_area():
            t = theta_tracker.get_value()
            x_n = 4 * np.cos(t)
            y_n = 2 * np.sqrt(3) * np.sin(t)
            d = abs(x_n - 2 * y_n + 4) / np.sqrt(5)
            return 0.5 * 3 * np.sqrt(5) * d

        area_text = always_redraw(lambda: Text(
            f"S = {get_area():.2f}",
            font_size=24,
            color=YELLOW
        ).next_to(title_text, DOWN, buff=0.4, aligned_edge=LEFT))
        self.add(area_text)

        # 第二问推导步骤
        q2_step1 = VGroup(
            Text("设 N(4cosθ, 2√3sinθ)", font_size=20),
            Text("点到直线距离：", font_size=20),
            MathTex(r"d = \frac{|4\cos\theta - 4\sqrt{3}\sin\theta + 4|}{\sqrt{5}}", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step1.next_to(area_text, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q2_step1), run_time=1.5)
        self.wait(0.5)

        q2_step2 = VGroup(
            Text("利用辅助角公式：", font_size=20),
            MathTex(r"4\cos\theta - 4\sqrt{3}\sin\theta = 8\cos(\theta + \frac{\pi}{3})", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step2.next_to(q2_step1, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q2_step2), run_time=1.5)
        self.wait(0.5)

        self.play(FadeOut(q2_step1), run_time=0.3)

        q2_step3 = VGroup(
            Text("最小值为 -8，代入距离公式：", font_size=20),
            MathTex(r"d_{max} = \frac{4\sqrt{5}}{5}", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step3.next_to(q2_step2, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q2_step3), run_time=1.5)
        self.wait(0.5)

        self.play(FadeOut(q2_step2), run_time=0.3)

        q2_step4 = VGroup(
            Text("三角形面积最大值：", font_size=20),
            MathTex(r"S_{max} = \frac{1}{2} \times 3\sqrt{5} \times \frac{4\sqrt{5}}{5} = 6", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step4.next_to(q2_step3, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(q2_step4), run_time=1.5)
        self.wait(0.5)

        # 动画：点 N 运动
        self.play(theta_tracker.animate.set_value(TAU), run_time=8, rate_func=linear)
        self.wait(1)