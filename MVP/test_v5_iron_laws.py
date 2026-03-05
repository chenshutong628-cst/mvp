from manim import *
import numpy as np

class MainScene(Scene):
    def construct(self):
        # 【V5 铁律 1：防重叠排版】
        # 左侧推导文字组必须使用 .to_edge(LEFT, buff=0.5)
        # 右侧坐标系及其附属图形必须使用 .to_edge(RIGHT, buff=0.5)

        # Title zone - 题目常驻（左上角）
        global_problem_text = VGroup(
            Text("已知椭圆 C: x²/a² + y²/b² = 1 (a > b > 0) 过点 M(2,3)，", font_size=16),
            Text("点 A 为其左顶点，且 AM 的斜率为 1/2。", font_size=16),
            Text("1. 求 C 的方程；", font_size=16),
            Text("2. 点 N 为椭圆上任意一点，求 △AMN 的面积的最大值。", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # V5：强制使用 .to_edge(LEFT, buff=0.5)
        global_problem_text.to_edge(LEFT, buff=0.5)
        self.add(global_problem_text)

        # 【V5 铁律 2：1:1 防畸变坐标系】
        # Axes 的 x_range 跨度与 x_length 的比值，必须严格等于 y_range 跨度与 y_length 的比值

        # 计算：x_range = [-5, 5], y_range = [-4, 4]
        # x_range 跨度 = 5 - (-5) = 10
        # y_range 跨度 = 4 - (-4) = 8
        # 比例 = 10 / 8 = 1.25
        # 所以 x_length / y_length = 1.25

        # 设置 x_length = 7.5，则 y_length = 7.5 / 1.25 = 6.0
        # 或者 x_length = 6.0，则 y_length = 6.0 / 1.25 = 4.8

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=6.0,         # x_range 跨度 10，y_range 跨度 8，比例 1.25:1
            y_length=4.8,         # 6.0 / 4.8 = 1.25 = 10/8 ✅
            axis_config={"color": GREY, "stroke_width": 1}
        )

        # V5：强制使用 .to_edge(RIGHT, buff=0.5)
        axes.to_edge(RIGHT, buff=0.5)
        self.add(axes)

        # 【V5 铁律 3：几何体缩放铁律】
        # 绘制椭圆时，严禁使用绝对物理数值，必须使用 axes.x_axis.unit_size 和 axes.y_axis.unit_size

        # 椭圆 x²/16 + y²/12 = 1
        # a = 4, b = 2√3
        # 强制使用 unit_size 进行真实数学比例缩放
        ellipse = Ellipse(
            width=8 * axes.x_axis.unit_size,                    # 2a = 8 * unit_size
            height=4 * np.sqrt(3) * axes.y_axis.unit_size,          # 2b = 2 * (2√3) * unit_size
            color=BLUE,
            stroke_width=2
        ).move_to(axes.c2p(0, 0))
        self.play(Create(ellipse), run_time=1)

        # 【V5 铁律 4：动态与锚定铁律】
        # 点 M、A 以及动点 N、多边形 △AMN，必须 100% 绑定到 axes.c2p(x, y) 上
        # 动点 N 的轨迹动画必须通过 ValueTracker 配合 always_redraw / add_updater 实现

        # 点 A(-4, 0) 和 M(2, 3)
        point_a = Dot(axes.c2p(-4, 0), color=WHITE, radius=0.06)
        label_a = Text("A", font_size=16, color=WHITE).next_to(point_a, DOWN, buff=0.1)
        point_m = Dot(axes.c2p(2, 3), color=WHITE, radius=0.06)
        label_m = Text("M", font_size=16, color=WHITE).next_to(point_m, UP, buff=0.1)
        self.play(FadeIn(point_a, label_a, point_m, label_m), run_time=0.5)

        # Scene 01-02: 求 a
        # V5：左侧文本组必须使用 .to_edge(LEFT, buff=0.5)
        q1_step1 = VGroup(
            Text("根据斜率公式：", font_size=20, color=WHITE),
            MathTex(r"k_{AM} = \frac{3}{2+a} = \frac{1}{2}", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step1.to_edge(LEFT, buff=0.5)
        self.play(Write(q1_step1), run_time=1)
        self.wait(0.5)

        q1_step2 = MathTex(r"\Rightarrow a = 4", font_size=20, color=YELLOW).to_edge(LEFT, buff=0.5)
        self.play(Write(q1_step2), run_time=0.8)
        self.wait(0.5)

        # Scene 03: 求 b
        q1_step3 = VGroup(
            Text("将 M(2,3) 代入椭圆方程：", font_size=20, color=WHITE),
            MathTex(r"\frac{4}{16} + \frac{9}{b^2} = 1", font_size=18, color=YELLOW),
            MathTex(r"\Rightarrow b^2 = 12", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step3.to_edge(LEFT, buff=0.5)
        self.play(Write(q1_step3), run_time=1.5)
        self.wait(0.5)

        # Scene 04: 椭圆方程与直线 AM
        q1_step4 = VGroup(
            Text("椭圆方程：", font_size=20, color=WHITE),
            MathTex(r"\frac{x^2}{16} + \frac{y^2}{12} = 1", font_size=18, color=YELLOW),
            Text("直线 AM: x - 2y + 4 = 0", font_size=18, color=WHITE),
            MathTex(r"|AM| = 3\sqrt{5}", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q1_step4.to_edge(LEFT, buff=0.5)
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

        # V5：动点 N 必须使用 axes.c2p(x, y) 进行锚定
        def ellipse_point(t):
            x = 4 * np.cos(t)
            y = 2 * np.sqrt(3) * np.sin(t)
            return axes.c2p(x, y)  # 强制锚定到坐标系

        point_n = always_redraw(lambda: Dot(ellipse_point(theta_tracker.get_value()), color=RED, radius=0.08))
        label_n = always_redraw(lambda: Text("N", font_size=16, color=RED).next_to(ellipse_point(theta_tracker.get_value()), UP + RIGHT, buff=0.1))
        self.add(point_n, label_n)

        # V5：动态三角形必须使用 axes.c2p(x, y) 进行锚定
        triangle = always_redraw(lambda: Polygon(
            axes.c2p(-4, 0),      # 点 A：强制锚定到坐标系
            axes.c2p(2, 3),       # 点 M：强制锚定到坐标系
            ellipse_point(theta_tracker.get_value()),  # 点 N：强制锚定到坐标系
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
            # 点到直线距离公式：|Ax + By + C| / sqrt(A^2 + B^2)
            # 直线 AM: x - 2y + 4 = 0，所以 A=1, B=-2, C=4
            d = abs(x_n - 2 * y_n + 4) / np.sqrt(5)
            return 0.5 * 3 * np.sqrt(5) * d

        area_text = always_redraw(lambda: Text(
            f"S = {get_area():.2f}",
            font_size=24,
            color=YELLOW
        ).to_edge(LEFT, buff=0.5))  # V5：强制使用 .to_edge(LEFT, buff=0.5)
        self.add(area_text)

        # 第二问推导步骤
        q2_step1 = VGroup(
            Text("设 N(4cosθ, 2√3sinθ)", font_size=20, color=WHITE),
            Text("点到直线距离：", font_size=20, color=WHITE),
            MathTex(r"d = \frac{|4\cos\theta - 4\sqrt{3}\sin\theta + 4|}{\sqrt{5}}", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step1.to_edge(LEFT, buff=0.5)  # V5：强制使用 .to_edge(LEFT, buff=0.5)
        self.play(Write(q2_step1), run_time=1.5)
        self.wait(0.5)

        q2_step2 = VGroup(
            Text("利用辅助角公式：", font_size=20, color=WHITE),
            MathTex(r"4\cos\theta - 4\sqrt{3}\sin\theta = 8\cos(\theta + \frac{\pi}{3})", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step2.to_edge(LEFT, buff=0.5)  # V5：强制使用 .to_edge(LEFT, buff=0.5)
        self.play(Write(q2_step2), run_time=1.5)
        self.wait(0.5)

        self.play(FadeOut(q2_step1), run_time=0.3)

        q2_step3 = VGroup(
            Text("最小值为 -8，代入距离公式：", font_size=20, color=WHITE),
            MathTex(r"d_{max} = \frac{4\sqrt{5}}{5}", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step3.to_edge(LEFT, buff=0.5)  # V5：强制使用 .to_edge(LEFT, buff=0.5)
        self.play(Write(q2_step3), run_time=1.5)
        self.wait(0.5)

        self.play(FadeOut(q2_step2), run_time=0.3)

        q2_step4 = VGroup(
            Text("三角形面积最大值：", font_size=20, color=WHITE),
            MathTex(r"S_{max} = \frac{1}{2} \times 3\sqrt{5} \times \frac{4\sqrt{5}}{5} = 6", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q2_step4.to_edge(LEFT, buff=0.5)  # V5：强制使用 .to_edge(LEFT, buff=0.5)
        self.play(Write(q2_step4), run_time=1.5)
        self.wait(0.5)

        # 动画：点 N 运动
        self.play(theta_tracker.animate.set_value(TAU), run_time=8, rate_func=linear)
        self.wait(1)
