from manim import *
import numpy as np

# ==========================================
# 2020年江苏高考数学第18题 - 动态讲解视频
# ==========================================

class JiangsuMath18(Scene):
    def construct(self):
        # 初始化对象注册表
        self.objects = {}

        # ==========================
        # Scene 01: 题目展示
        # ==========================
        self.scene_01_display_problem()
        self.wait(1)

        # ==========================
        # Scene 02: 第一问 - 求三角形 AF1F2 的周长
        # ==========================
        self.scene_02_calculate_perimeter()
        self.wait(1)

        # ==========================
        # Scene 03: 第二问 - 求 OP + OQ 的最小值
        # ==========================
        self.scene_03_calculate_minimum_vector()
        self.wait(1)

        # ==========================
        # Scene 04: 第二问 - 求点 M 的坐标
        # ==========================
        self.scene_04_calculate_point_m()
        self.wait(1)

        # ==========================
        # Scene 05: 最终总结
        # ==========================
        self.scene_05_final_summary()
        self.wait(2)

    # ------------------------------------------------------------
    # Layout Helpers (V5 铁律)
    # ------------------------------------------------------------
    def create_axes(self, x_range=(-3, 4), y_range=(-2, 3)):
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=7.0,
            y_length=5.0,
            tips=False
        ).to_edge(RIGHT, buff=0.5)
        return axes

    def create_ellipse(self, a=2, b=np.sqrt(3)):
        # 严格遵守 V5 铁律：使用 Axes.c2p 进行坐标映射
        axes = self.objects["axes_graph"]
        ellipse = Ellipse(
            width=2 * a * axes.x_axis.unit_size,
            height= 2 * b * axes.y_axis.unit_size,
            color=BLUE,
            stroke_width=2
        ).move_to(axes.c2p(0, 0))
        return ellipse

    # ------------------------------------------------------------
    # Scene 01: 题目展示
    # ------------------------------------------------------------
    def scene_01_display_problem(self):
        # 创建坐标系
        axes = self.create_axes(x_range=(-3, 4), y_range=(-2, 3))
        self.objects["axes_graph"] = axes

        # 题目文本 - 使用 VGroup + MathTex 拼接法
        q_line1 = VGroup(
            Text("在平面直角坐标系 ", font_size=20),
            MathTex(r"xOy", font_size=24),
            Text(" 中，已知椭圆 ", font_size=20),
            MathTex(r"E: \frac{x^2}{4} + \frac{y^2}{3} = 1", font_size=22, color=BLUE)
        ).arrange(RIGHT)

        q_line2 = VGroup(
            Text(" 的左、右焦点分别为 ", font_size=20),
            MathTex(r"F_1, F_2", font_size=22),
            Text("，点 ", font_size=20),
            MathTex(r"A", font_size=22),
            Text(" 在椭圆 ", font_size=20),
            MathTex(r"E", font_size=22),
            Text(" 上且在第一象限内，", font_size=20),
            MathTex(r"AF_2 \perp F_1F_2", font_size=22)
        ).arrange(RIGHT)

        q_line3 = VGroup(
            Text("直线 ", font_size=20),
            MathTex(r"AF_1", font_size=22),
            Text(" 与椭圆 ", font_size=20),
            MathTex(r"E", font_size=22),
            Text(" 相交于另一点 ", font_size=20),
            MathTex(r"B", font_size=22),
            Text("。", font_size=20)
        ).arrange(RIGHT)

        # 题目问题组
        q_problem_1 = VGroup(
            Text("(1) 求 ", font_size=22, color=YELLOW),
            MathTex(r"\triangle AF_1F_2", font_size=22),
            Text(" 的周长；", font_size=20)
        ).arrange(RIGHT)

        q_problem_2 = VGroup(
            Text("(2) 在 ", font_size=22, color=YELLOW),
            MathTex(r"x", font_size=20),
            Text(" 轴上任取一点 ", font_size=20),
            MathTex(r"P", font_size=22),
            Text("，直线 ", font_size=20),
            MathTex(r"AP", font_size=22),
            Text(" 与椭圆 ", font_size=20),
            MathTex(r"E", font_size=22),
            Text(" 的右准线相交于点 ", font_size=20),
            MathTex(r"Q", font_size=22),
            Text("，求 ", font_size=20),
            MathTex(r"\overrightarrow{OP} \cdot \overrightarrow{QP}", font_size=22, color=YELLOW),
            Text(" 的最小值；", font_size=20)
        ).arrange(RIGHT)

        q_problem_3 = VGroup(
            Text("(3) 设点 ", font_size=22, color=YELLOW),
            MathTex(r"M", font_size=20),
            Text(" 在椭圆 ", font_size=20),
            MathTex(r"E", font_size=22),
            Text(" 上，记 ", font_size=20),
            MathTex(r"\triangle OAB", font_size=20),
            Text(" 与 ", font_size=20),
            MathTex(r"\triangle MAB", font_size=20),
            Text(" 的面积分别为 ", font_size=20),
            MathTex(r"S_1, S_2", font_size=20),
            Text("，若 ", font_size=20),
            MathTex(r"S_2 = 3S_1", font_size=20, color=YELLOW),
            Text("，求点 ", font_size=20),
            MathTex(r"M", font_size=20),
            Text(" 的坐标。", font_size=20)
        ).arrange(RIGHT)

        # 布局
        q_group = VGroup(q_line1, q_line2, q_line3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        q_group.to_edge(UP + LEFT, buff=0.5)

        problems = VGroup(q_problem_1, q_problem_2, q_problem_3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        problems.next_to(q_group, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(Write(q_group), run_time=1)
        self.play(Write(problems), run_time=1.5)
        self.play(Create(axes), run_time=1)

        self.wait(0.5)
        self.objects["question_text"] = q_group
        self.objects["problems"] = problems

    # ------------------------------------------------------------
    # Scene 02: 第一问 - 求三角形 AF1F2 的周长
    # ------------------------------------------------------------
    def scene_02_calculate_perimeter(self):
        # 左侧解析文本
        step1 = VGroup(
            Text("解：", font_size=18, color=BLUE),
            MathTex(r"a = 2, b = \sqrt{3}, c = 1", font_size=20)
        ).arrange(RIGHT)

        step2 = VGroup(
            Text("点 ", font_size=18),
            MathTex(r"A", font_size=20),
            Text(" 在椭圆上且 ", font_size=18),
            MathTex(r"x_A = 1", font_size=20, color=YELLOW)
        ).arrange(RIGHT)

        step3 = VGroup(
            Text("代入椭圆方程：", font_size=18),
            MathTex(r"\frac{1^2}{4} + \frac{y^2}{3} = 1", font_size=18),
            Text("，得 ", font_size=18),
            MathTex(r"\frac{y^2}{3} = \frac{3}{4}", font_size=18),
            MathTex(r"y_A = \pm \frac{3}{2}", font_size=18),
            Text("（第一象限取正）", font_size=16)
        ).arrange(RIGHT)

        # 答式：周长公式
        step4 = VGroup(
            Text("根据定义：", font_size=18),
            MathTex(r"|AF_1| + |F_1F_2| + |F_2A|", font_size=20),
            Text(" = ", font_size=18),
            MathTex(r"2a + 2c", font_size=20, color=YELLOW)
        ).arrange(RIGHT)

        step5 = VGroup(
            Text("答案：", font_size=18, color=BLUE),
            MathTex(r"L = 4 + 2\sqrt{3}", font_size=22, color=YELLOW)
        ).arrange(RIGHT)

        # 布局
        solution = VGroup(step1, step2, step3, step4, step5).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        solution.next_to(self.objects["question_text"], DOWN, buff=0.8, aligned_edge=LEFT)

        # 显示解析过程
        self.play(FadeIn(solution), run_time=1)
        self.wait(1)

        # 绘制椭圆和点
        axes = self.objects["axes_graph"]
        ellipse = self.create_ellipse()

        # 绘制焦点
        f1_dot = Dot(axes.c2p(-1, 0), color=RED, radius=0.08)
        f2_dot = Dot(axes.c2p(1, 0), color=RED, radius=0.08)
        label_f1 = Text("F₁", font_size=16, color=RED).next_to(f1_dot, DOWN + LEFT, buff=0.1)
        label_f2 = Text("F₂", font_size=16, color=RED).next_to(f2_dot, DOWN + RIGHT, buff=0.1)

        # 点 A
        a_dot = Dot(axes.c2p(1, 3/2), color=GREEN, radius=0.08)
        label_a = Text("A", font_size=16, color=GREEN).next_to(a_dot, UP, buff=0.1)

        self.play(Create(ellipse), run_time=1)
        self.play(
            FadeIn(f1_dot), Write(label_f1),
            FadeIn(f2_dot), Write(label_f2),
            FadeIn(a_dot), Write(label_a),
            run_time=1
        )

        # 绘制三角形 AF1F2
        triangle_af1f2 = Polygon(
            axes.c2p(1, 3/2),
            axes.c2p(-1, 0),
            axes.c2p(1, 0),
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_color=YELLOW,
            stroke_width=2
        )

        self.play(Create(triangle_af1f2), run_time=1.5)
        self.wait(1)

    # ------------------------------------------------------------
    # Scene 03: 第二问 - 求 OP + OQ 的最小值
    # ------------------------------------------------------------
    def scene_03_calculate_minimum_vector(self):
        # 清除上一问的内容
        self.remove(*self.mobjects)

        # 恢复问题文本
        self.add(self.objects["question_text"])

        # 左侧解析文本
        step1 = VGroup(
            Text("解：", font_size=18, color=BLUE),
            Text("点 ", font_size=18),
            MathTex(r"P", font_size=20),
            Text(" 的坐标为 ", font_size=18),
            MathTex(r"(x, 0)", font_size=20)
        ).arrange(RIGHT)

        step2 = VGroup(
            Text("直线 ", font_size=18),
            MathTex(r"AP", font_size=20),
            Text(" 的斜率为 ", font_size=18),
            MathTex(r"k = \frac{y_A}{x - 1}", font_size=20)
        ).arrange(RIGHT)

        step3 = VGroup(
            Text("直线 ", font_size=18),
            MathTex(r"AP", font_size=20),
            Text(" 的方程为：", font_size=18),
            MathTex(r"y = \frac{3}{2}(x + 1)", font_size=20)
        ).arrange(RIGHT)

        step4 = VGroup(
            Text("由椭圆性质，点 ", font_size=18),
            MathTex(r"Q", font_size=20),
            Text(" 在椭圆上，且 ", font_size=18),
            MathTex(r"\frac{x_Q^2}{4} + \frac{y_Q^2}{3} = 1", font_size=18)
        ).arrange(RIGHT)

        step5 = VGroup(
            Text("将 ", font_size=18),
            MathTex(r"AP", font_size=20),
            Text(" 方程代入，解得：", font_size=18),
            MathTex(r"y_Q = \pm\sqrt{3 - \frac{3}{4}(x + 1)^2}", font_size=20)
        ).arrange(RIGHT)

        step6 = VGroup(
            Text("向量：", font_size=18),
            MathTex(r"\overrightarrow{OP} = (1, 0) - (x, 0)", font_size=20),
            MathTex(r" = (1 - x, 0)", font_size=20)
        ).arrange(RIGHT)

        step7 = VGroup(
            Text("向量：", font_size=18),
            MathTex(r"\overrightarrow{QP} = (x - x_Q, y_Q - 0)", font_size=20),
            Text(" = (x - x_Q, y_Q)", font_size=20)
        ).arrange(RIGHT)

        step8 = VGroup(
            Text("点积：", font_size=18),
            MathTex(r"\overrightarrow{OP} \cdot \overrightarrow{QP} = (1 - x) \cdot x + 0 \cdot y_Q", font_size=20),
            Text(" = (1 - x) \cdot x + 0 \cdot y_Q", font_size=20)
        ).arrange(RIGHT)

        step9 = VGroup(
            Text("代入 ", font_size=18),
            MathTex(r"y_Q = \pm\sqrt{3 - \frac{3}{4}(1 - x)^2}", font_size=20),
            Text("，得：", font_size=18),
            MathTex(r"y_Q = \pm\sqrt{3 - \frac{3}{4}(1 - x)^2}", font_size=20)
        ).arrange(RIGHT)

        step10 = VGroup(
            Text("点积化简：", font_size=18),
            MathTex(r"(1 - x) \cdot x + 0 \cdot \left[\pm\sqrt{3 - \frac{3}{4}(1 - x)^2}\right] = \left[1 - x \pm (1 - x)\sqrt{4 - \frac{3}{4}(1 - x)^2}\right]", font_size=20)
        ).arrange(RIGHT)

        step11 = VGroup(
            Text("平方：", font_size=18),
            MathTex(r"(1 - x) \pm (1 - x)\sqrt{4 - \frac{3}{4}(1 - x)^2} = (1 - x)^2 + (1 - x)^2(1 - \frac{3}{4})", font_size=20)
        ).arrange(RIGHT)

        step12 = VGroup(
            Text("平方：", font_size=18),
            MathTex(r"(1 - x)^2 + (1 - x)^2(1 - \frac{3}{4}) = (1 - \frac{3}{4}) - \frac{3}{4}x^2", font_size=20)
        ).arrange(RIGHT)

        step13 = VGroup(
            Text("求导：", font_size=18),
            MathTex(r"\frac{d}{dx}\left[(1 - x) \pm (1 - x)\sqrt{4 - \frac{3}{4}(1 - x)^2}\right] = \left[1 - \frac{3}{2}x\right]", font_size=20, color=YELLOW)
        ).arrange(RIGHT)

        step14 = VGroup(
            Text("令导数为 0：", font_size=18),
            MathTex(r"1 - \frac{3}{2}x = 0", font_size=20),
            Text("，", font_size=18),
            MathTex(r"x = \frac{2}{3}", font_size=20, color=YELLOW)
        ).arrange(RIGHT)

        step15 = VGroup(
            Text("对应点积：", font_size=18),
            MathTex(r"(1 - x) \cdot x + 0 \cdot \left[-\sqrt{4 - \frac{3}{4}(\frac{2}{3})^2}\right] = -\frac{1}{3}", font_size=20)
        ).arrange(RIGHT)

        step16 = VGroup(
            Text("答案：", font_size=18, color=BLUE),
            MathTex(r"\overrightarrow{OP} \cdot \overrightarrow{QP} = -\frac{1}{3}", font_size=22, color=YELLOW)
        ).arrange(RIGHT)

        # 布局
        solution = VGroup(step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12, step13, step14, step15, step16).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        solution.next_to(self.objects["question_text"], DOWN, buff=0.8, aligned_edge=LEFT)

        # 显示解析过程
        self.play(FadeIn(solution), run_time=1)

        # 动画演示：点 P 在 x 轴上移动
        axes = self.objects["axes_graph"]
        ellipse = self.create_ellipse()

        # 创建动点 P
        x_tracker = ValueTracker(-2)
        point_p = Dot(color=RED, radius=0.08)
        point_p.add_updater(lambda d: d.move_to(axes.c2p(x_tracker.get_value(), 0)))

        # 创建点 Q
        point_q = Dot(color=YELLOW, radius=0.08)
        point_q.add_updater(
            lambda d: d.move_to(
                axes.c2p(
                    x_tracker.get_value(),
                    np.sqrt(3) if x_tracker.get_value() <= 0 else -np.sqrt(3)
                )
            )
        )

        # 创建向量标注
        op_arrow = Arrow(axes.c2p(0, 0), axes.c2p(1, 3/2), color=ORANGE, buff=0.1)
        qp_arrow = Arrow(axes.c2p(2/3, 0), axes.c2p(1, 3/2), color=PURPLE, buff=0.1)

        self.play(Create(ellipse), run_time=1)

        # 标注点 A 和 P
        label_p = always_redraw(lambda: Text("P", font_size=16, color=RED).next_to(point_p, DOWN, buff=0.1))

        # 添加到场景
        self.add(point_p, point_q, label_p)

        # 动画：点 P 从 -2 移动到 2/3
        self.play(
            x_tracker.animate.set_value(2/3),
            run_time=4,
            rate_func=linear
        )

        # 显示向量 OP 和 QP
        self.play(Create(op_arrow), Create(qp_arrow), run_time=1)
        self.wait(1)

        # 标注向量值
        vector_value = MathTex(r"\overrightarrow{OP} \cdot \overrightarrow{QP} = -\frac{1}{3}", font_size=20, color=YELLOW)
        vector_value.to_edge(LEFT, buff=0.5).shift(DOWN * 2)
        self.play(Write(vector_value), run_time=1)
        self.wait(2)

    # ------------------------------------------------------------
    # Scene 04: 第二问 - 求点 M 的坐标
    # ------------------------------------------------------------
    def scene_04_calculate_point_m(self):
        # 清除上一问的内容
        self.remove(*self.mobjects)
        self.add(self.objects["question_text"])

        # 左侧解析文本
        step1 = VGroup(
            Text("解：", font_size=18, color=BLUE),
            Text("点 ", font_size=18),
            MathTex(r"M", font_size=20),
            Text(" 的坐标为 ", font_size=18),
            MathTex(r"(1, \frac{3}{2})", font_size=20)
        ).arrange(RIGHT)

        step2 = VGroup(
            Text("椭圆方程：", font_size=18),
            MathTex(r"\frac{x^2}{4} + \frac{y^2}{3} = 1", font_size=18),
            Text("，点 ", font_size=18),
            MathTex(r"M", font_size=20),
            Text(" 满足方程", font_size=18)
        ).arrange(RIGHT)

        step3 = VGroup(
            Text("验证面积条件：", font_size=18, color=YELLOW),
            MathTex(r"S_1 = \frac{1}{2}|(-4) \cdot \frac{3}{2}|", font_size=18),
            MathTex(r"= 3", font_size=20)
        ).arrange(RIGHT)

        step4 = VGroup(
            Text("点 ", font_size=18),
            MathTex(r"M", font_size=20),
            Text(" 与 ", font_size=18),
            MathTex(r"O(0, 0)", font_size=20),
            Text("、", font_size=18),
            MathTex(r"A(-2, 0)", font_size=20),
            Text("、", font_size=18),
            MathTex(r"B(2, 0)", font_size=20),
            Text(" 构成", font_size=18),
            MathTex(r"\triangle OAB", font_size=20),
            Text("，", font_size=18),
            MathTex(r"\triangle MAB", font_size=20),
            Text(" 的面积相等", font_size=18)
        ).arrange(RIGHT)

        step5 = VGroup(
            Text("由 ", font_size=18),
            MathTex(r"S_2 = \frac{1}{2}|AB| \cdot d", font_size=18),
            MathTex(r"= 3", font_size=20, color=YELLOW)
        ).arrange(RIGHT)

        step6 = VGroup(
            Text("其中 ", font_size=18),
            MathTex(r"|AB| = \sqrt{(2)^2 + (\frac{3}{2})^2} = \frac{5}{2}", font_size=18)
        ).arrange(RIGHT)

        step7 = VGroup(
            Text("边距 ", font_size=18),
            MathTex(r"d = \frac{|4\sqrt{3} \cdot 1 - \frac{3}{2}|}{\sqrt{5}}", font_size=18),
            MathTex(r"= \frac{2\sqrt{3} \cdot \frac{1}{2}}{\sqrt{5}} = \frac{\sqrt{3}}{\sqrt{5}}", font_size=18)
        ).arrange(RIGHT)

        step8 = VGroup(
            Text("因此点 ", font_size=18),
            MathTex(r"M", font_size=20),
            Text(" 的坐标为 ", font_size=18),
            MathTex(r"(1, \frac{3}{2})", font_size=22, color=YELLOW)
        ).arrange(RIGHT)

        # 布局
        solution = VGroup(step1, step2, step3, step4, step5, step6, step7, step8).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        solution.next_to(self.objects["question_text"], DOWN, buff=0.8, aligned_edge=LEFT)

        # 显示解析过程
        self.play(FadeIn(solution), run_time=1)

        # 绘制椭圆和点
        axes = self.objects["axes_graph"]
        ellipse = self.create_ellipse()

        # 绘制点
        dot_o = Dot(axes.c2p(0, 0), color=WHITE, radius=0.08)
        dot_a = Dot(axes.c2p(-2, 0), color=YELLOW, radius=0.08)
        dot_b = Dot(axes.c2p(2, 0), color=YELLOW, radius=0.08)
        dot_m = Dot(axes.c2p(1, 3/2), color=GREEN, radius=0.08)

        label_o = Text("O", font_size=16, color=WHITE).next_to(dot_o, DOWN + LEFT, buff=0.1)
        label_a = Text("A", font_size=16, color=YELLOW).next_to(dot_a, DOWN + LEFT, buff=0.1)
        label_b = Text("B", font_size=16, color=YELLOW).next_to(dot_b, DOWN, buff=0.1)
        label_m = Text("M", font_size=16, color=GREEN).next_to(dot_m, UP, buff=0.1)

        # 绘制三角形 OAB 和 MAB
        triangle_oab = Polygon(
            axes.c2p(0, 0),
            axes.c2p(-2, 0),
            axes.c2p(2, 0),
            fill_color=YELLOW,
            fill_opacity=0.15,
            stroke_color=YELLOW,
            stroke_width=2
        )

        triangle_mab = Polygon(
            axes.c2p(0, 0),
            axes.c2p(2, 0),
            axes.c2p(1, 3/2),
            fill_color=GREEN,
            fill_opacity=0.15,
            stroke_color=GREEN,
            stroke_width=2
        )

        self.play(Create(ellipse), run_time=1)

        self.play(
            FadeIn(dot_o), Write(label_o),
            FadeIn(dot_a), Write(label_a),
            FadeIn(dot_b), Write(label_b),
            FadeIn(dot_m), Write(label_m),
            run_time=1
        )

        self.play(Create(triangle_oab), run_time=1)
        self.wait(1)
        self.play(Create(triangle_mab), run_time=1)
        self.wait(1)

        # 标注面积相等
        area_text = VGroup(
            MathTex(r"S_1 = \frac{1}{2}|(-4) \cdot \frac{3}{2}| = 3", font_size=18, color=YELLOW),
            MathTex(r"\qquad S_2 = \frac{1}{2}|AB| \cdot d = 3", font_size=18, color=GREEN)
        ).arrange(DOWN)

        area_text.to_edge(LEFT, buff=0.5)
        self.play(FadeIn(area_text), run_time=1)
        self.wait(1)

    # ------------------------------------------------------------
    # Scene 05: 最终总结
    # ------------------------------------------------------------
    def scene_05_final_summary(self):
        # 清除之前的内容
        self.remove(*self.mobjects)
        self.add(self.objects["question_text"])

        # 总结三问的答案
        answer1 = VGroup(
            Text("(1) ", font_size=20, color=BLUE),
            MathTex(r"L = 4 + 2\sqrt{3}", font_size=24, color=YELLOW)
        ).arrange(RIGHT)

        answer2 = VGroup(
            Text("(2) ", font_size=20, color=BLUE),
            MathTex(r"\overrightarrow{OP} \cdot \overrightarrow{QP} = -\frac{1}{3}", font_size=24, color=YELLOW)
        ).arrange(RIGHT)

        answer3 = VGroup(
            Text("(3) ", font_size=20, color=BLUE),
            MathTex(r"M(1, \frac{3}{2})", font_size=24, color=YELLOW)
        ).arrange(RIGHT)

        # 布局
        answers = VGroup(
            Text("答案汇总：", font_size=22, color=WHITE),
            answer1,
            answer2,
            answer3
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        answers.to_edge(LEFT, buff=0.5)
        self.play(Write(answers), run_time=2)

        # 显示最终椭圆
        axes = self.objects["axes_graph"]
        ellipse = self.create_ellipse()
        self.play(Create(ellipse), run_time=1.5)
        self.wait(2)
