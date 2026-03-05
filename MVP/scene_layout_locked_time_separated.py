from manim import *
import numpy as np

# ==========================================
# Helper Classes for Dynamic Geometry - REMOVED
# ==========================================
# 已删除导致内存泄漏的 DynamicPointOnCurve、DynamicLine、DynamicTriangle
# 现在使用 Manim 官方 API (TracedPath) 实现拖尾效果

# ==========================================
# Main Scene
# ==========================================

class MainScene(Scene):
    def construct(self):
        # Global Constants
        self.a_val = 4.0
        self.b_val = np.sqrt(12)
        self.point_a_coords = np.array([-self.a_val, 0, 0])
        self.point_m_coords = np.array([2, 3, 0])

        # Layout Anchors
        self.title_anchor = LEFT * 0.5 + UP * 2.5
        self.formula_anchor = LEFT * 0.5 + DOWN * 1.0
        self.graph_anchor = RIGHT * 0.5

        # Initialize Objects Registry
        self.objects = {}

        # Execute Scenes
        self.scene_01()
        self.scene_02()
        self.scene_03()
        self.scene_04()
        self.scene_05()
        self.scene_06()
        self.scene_07()
        self.scene_08()

    # ------------------------------------------------------------
    # Layout Helpers
    # ------------------------------------------------------------
    def create_axes(self):
        x_range = [-5, 5]
        y_range = [-4, 4]
        x_len = 6.0
        y_len = 6.0 * (8.0 / 10.0)

        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_len,
            y_length=y_len,
            tips=False
        ).to_edge(RIGHT, buff=0.5)
        return axes

    def create_ellipse(self):
        # 严格遵守 V5 铁律：获取坐标系，应用 unit_size 和 c2p
        axes = self.objects["axes_graph"]
        ellipse = Ellipse(
            width=2 * self.a_val * axes.x_axis.unit_size,
            height=2 * self.b_val * axes.y_axis.unit_size,
            color=BLUE,
            stroke_width=3
        ).move_to(axes.c2p(0, 0))
        return ellipse

    def place_text(self, mobj, zone="left"):
        if zone == "left":
            mobj.to_edge(LEFT, buff=0.5)
        elif zone == "right":
            mobj.to_edge(RIGHT, buff=0.5)
        return mobj

    # ------------------------------------------------------------
    # Scene 01: 题目分析与几何图形构建 - 【布局锁定】
    # ------------------------------------------------------------
    def scene_01(self):
        # 【布局锁定：题目绝对锁定在左上角 - 使用 VGroup + MathTex 渲染】
        # 行 1：已知条件
        q_line1 = VGroup(
            Text("已知椭圆 ", font_size=20),
            MathTex(r"C: \frac{x^2}{a^2} + \frac{y^2}{b^2} = 1 \ (a>b>0)", font_size=22),
            Text("，过点", font_size=20),
            MathTex(r"M(2, 3)", font_size=22)
        ).arrange(RIGHT)

        # 行 2：顶点与斜率
        q_line2 = VGroup(
            Text("点 ", font_size=20),
            MathTex(r"A", font_size=22),
            Text(" 为其左顶点，且 ", font_size=20),
            MathTex(r"AM", font_size=22),
            Text(" 的斜率为 ", font_size=20),
            MathTex(r"\frac{1}{2}", font_size=22),
            Text("。", font_size=20)
        ).arrange(RIGHT)

        # 行 3：求解目标
        q_line3 = VGroup(
            Text("(1) 求 ", font_size=20),
            MathTex(r"C", font_size=22),
            Text(" 的方程； (2) 求 ", font_size=20),
            MathTex(r"\triangle AMN", font_size=22),
            Text(" 面积的最大值。", font_size=20)
        ).arrange(RIGHT)

        # 整体打包并严格钉死在左上角
        q_group = VGroup(q_line1, q_line2, q_line3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        q_group.to_edge(UP + LEFT, buff=0.5)
        self.objects["question_text"] = q_group

        # 创建坐标系
        axes = self.create_axes()

        self.play(Write(q_group), run_time=1)
        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        self.objects["axes_graph"] = axes

    # ------------------------------------------------------------
    # 第（1）问解析：求解椭圆方程
    # ------------------------------------------------------------
    def scene_02(self):
        # 第（1）问解析步骤 1：使用题目文本作为锚点
        label_02 = Text("(1) 求解椭圆方程：", font_size=20, color=YELLOW)
        label_02.next_to(self.objects["question_text"], DOWN, buff=0.5, aligned_edge=LEFT)

        text_02 = Text("由题意知左顶点 A(-a,0)，M(2,3) 且斜率为 1/2", font_size=18)
        text_02.next_to(label_02, DOWN, buff=0.3, aligned_edge=LEFT)

        formula_02 = VGroup(Text("a = ", font_size=20), MathTex(r"4", font_size=20)).arrange(RIGHT)
        formula_02.next_to(text_02, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(FadeIn(label_02), FadeIn(text_02), FadeIn(formula_02), run_time=1)
        self.wait(0.5)

        self.objects["label_02"] = label_02
        self.objects["text_02"] = text_02
        self.objects["formula_02"] = formula_02

    def scene_03(self):
        # 第（1）问解析步骤 2：使用上一个公式作为锚点
        text_03_1 = VGroup(Text("M(2,3) 代入得 ", font_size=20), MathTex(r"b^2=12", font_size=20)).arrange(RIGHT)
        text_03_1.next_to(self.objects["formula_02"], DOWN, buff=0.3, aligned_edge=LEFT)

        text_03_2 = VGroup(Text("椭圆方程为 ", font_size=20, color=YELLOW), MathTex(r"\frac{x^2}{16} + \frac{y^2}{12} = 1", font_size=20, color=YELLOW)).arrange(RIGHT)
        text_03_2.next_to(text_03_1, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(FadeIn(text_03_1), FadeIn(text_03_2), run_time=1)
        self.wait(0.5)

        self.objects["formula_03_1"] = text_03_1
        self.objects["formula_03_2"] = text_03_2

        # 将第（1）问的所有解析文本保存到 VGroup，以备清屏使用
        self.objects["solution_part1"] = VGroup(
            self.objects["label_02"],
            self.objects["text_02"],
            self.objects["formula_02"],
            self.objects["formula_03_1"],
            self.objects["formula_03_2"]
        )

    # ------------------------------------------------------------
    # 第（2）问解析：求面积最大值
    # ------------------------------------------------------------
    def scene_04(self):
        # 【关键操作】：清屏，清除第（1）问的解析文字
        self.play(FadeOut(self.objects["solution_part1"]), run_time=0.5)

        # 【修复 1：第(2)问标题：先定位到题目正下方】
        part2_title = Text("(2) 求面积最大值：", font_size=20, color=YELLOW)
        part2_title.next_to(self.objects["question_text"], DOWN, buff=0.4, aligned_edge=LEFT)

        # 【修复 2：第二问的第一行解析：先定位到标题下方，X轴左对齐】
        line_am = VGroup(Text("直线 ", font_size=18), MathTex(r"AM: x-2y+4=0, \ |AM|=3\sqrt{5}", font_size=20)).arrange(RIGHT)
        line_am.next_to(part2_title, DOWN, buff=0.3)
        line_am.align_to(self.objects["question_text"], LEFT)

        # 存入 self.objects 供后续 scene 使用
        self.objects["part2_line_am"] = line_am

        self.play(Write(part2_title))
        self.play(Write(line_am))
        self.wait(0.5)

        self.objects["label_04"] = part2_title
        self.objects["formula_04"] = line_am

    # ------------------------------------------------------------
    # Scene 05: 第一问结论 - 【加白框并右移避让】
    # ------------------------------------------------------------
    def scene_05(self):
        # 构建第一问结论组
        conc_eq = MathTex(r"\frac{x^2}{16} + \frac{y^2}{12} = 1", font_size=22, color=BLUE)
        conc_group = VGroup(Text("第一问结论：", font_size=18, color=BLUE), conc_eq).arrange(RIGHT)

        # 添加白色包围框
        box = SurroundingRectangle(conc_group, color=WHITE, buff=0.1)
        part1_conc = VGroup(box, conc_group)

        # 【抛光 2：锚定在题目正下方，并向右平移 3.0 个单位以避开左侧文本边缘】
        part1_conc.next_to(self.objects["question_text"], DOWN, buff=0.4, aligned_edge=LEFT).shift(RIGHT * 3.0)
        self.play(FadeIn(part1_conc), run_time=1)
        self.wait(0.5)

        # 保存到 objects 供第二问定位使用
        self.objects["part1_conc"] = part1_conc

        # 【修复 3：调整 part2_title 的 Y 轴与白框顶部对齐】
        self.play(self.objects["label_04"].animate.align_to(self.objects["part1_conc"], UP), run_time=0.3)
        self.wait(0.2)

        # 【修复 4：调整 line_am 的 Y 轴到白框下方 0.5，X 轴保持左对齐】
        # 【最终 UI 修复：使用链式调用同时锁定 XY 轴绝对坐标】
        # Y 轴：next_to 定位到白框下方，预留 0.5 的安全区
        # X 轴：紧接 align_to 强行拉回左侧，与最顶部的题目左边缘完美对齐
        self.play(
            self.objects["formula_04"].animate
                .next_to(self.objects["part1_conc"], DOWN, buff=0.5)
                .align_to(self.objects["question_text"], LEFT),
            run_time=0.3
        )
        self.wait(0.2)

    # ------------------------------------------------------------
    # Scene 06: 动点展示 - 【布局锁定】
    # ------------------------------------------------------------
    def scene_06(self):
        # 1. 获取底层坐标系 (严格遵守 V5 铁律)
        axes = self.objects["axes_graph"]

        # 2. 绘制静态点 A 和 M 及标签
        static_point_a = Dot(axes.c2p(-self.a_val, 0), color=WHITE, radius=0.08)
        static_point_m = Dot(axes.c2p(2, 3), color=YELLOW, radius=0.08)
        label_a = Text("A", font_size=18, color=WHITE).next_to(static_point_a, DOWN + LEFT, buff=0.1)
        label_m = Text("M", font_size=18, color=YELLOW).next_to(static_point_m, DOWN + RIGHT, buff=0.1)

        self.play(
            FadeIn(static_point_a), Write(label_a),
            FadeIn(static_point_m), Write(label_m),
            run_time=1
        )

        # 3. 创建参数追踪器与动点 N (强制包裹 c2p)
        t_tracker = ValueTracker(0)
        point_n = Dot(color=RED)
        point_n.add_updater(
            lambda d: d.move_to(
                axes.c2p(
                    self.a_val * np.cos(t_tracker.get_value()),
                    self.b_val * np.sin(t_tracker.get_value())
                )
            )
        )
        label_n = always_redraw(lambda: Text("N", font_size=18, color=WHITE).next_to(point_n, UP + RIGHT, buff=0.1))

        # 4. 使用官方 TracedPath 实现丝滑拖尾，绝对不卡死！
        trail = TracedPath(point_n.get_center, stroke_color=YELLOW, stroke_width=2)

        # 5. 重绘动态三角形 AMN
        triangle = always_redraw(
            lambda: Polygon(
                static_point_a.get_center(),
                static_point_m.get_center(),
                point_n.get_center(),
                fill_color=GREEN,
                fill_opacity=0.2,
                stroke_color=GREEN,
                stroke_width=2
            )
        )

        # 6. 添加到场景并播放动画
        self.add(trail, triangle, point_n, label_n)
        self.play(
            t_tracker.animate.set_value(TAU),
            run_time=8,
            rate_func=linear
        )
        self.wait(1)

    # ------------------------------------------------------------
    # Scene 07: 辅助角公式详细推导
    # ------------------------------------------------------------
    def scene_07(self):
        # 第（2）问解析步骤：详细展开辅助角公式，使用 part2_line_am 作为锚点
        text_07_1 = VGroup(Text("设 ", font_size=18), MathTex(r"N(4\cos\theta, 2\sqrt{3}\sin\theta)", font_size=18)).arrange(RIGHT)
        text_07_1.next_to(self.objects["part2_line_am"], DOWN, buff=0.2, aligned_edge=LEFT)

        text_07_2 = VGroup(MathTex(r"d = ", font_size=18), MathTex(r"\frac{|4\cos\theta - 4\sqrt{3}\sin\theta + 4|}{\sqrt{5}}", font_size=18)).arrange(RIGHT)
        text_07_2.next_to(text_07_1, DOWN, buff=0.2, aligned_edge=LEFT)

        text_07_3 = VGroup(MathTex(r"= ", font_size=18), MathTex(r"\frac{|8\cos(\theta + \frac{\pi}{3}) + 4|}{\sqrt{5}}", font_size=18)).arrange(RIGHT)
        text_07_3.next_to(text_07_2, DOWN, buff=0.2, aligned_edge=LEFT)

        text_07_4 = VGroup(Text("当 ", font_size=18), MathTex(r"\cos(\theta + \frac{\pi}{3}) = 1", font_size=18), Text(" 时，", font_size=18), MathTex(r"d_{\max} = \frac{12}{\sqrt{5}}", font_size=18)).arrange(RIGHT)
        text_07_4.next_to(text_07_3, DOWN, buff=0.2, aligned_edge=LEFT)

        text_07_5 = VGroup(MathTex(r"S_{\max} = \frac{1}{2} |AM| \cdot d_{\max} = 18", font_size=18, color=YELLOW)).arrange(RIGHT)
        text_07_5.next_to(text_07_4, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(
            FadeIn(text_07_1),
            FadeIn(text_07_2),
            run_time=1
        )
        self.wait(0.5)

        self.play(
            FadeIn(text_07_3),
            FadeIn(text_07_4),
            run_time=1
        )
        self.wait(0.5)

        self.play(FadeIn(text_07_5), run_time=1)
        self.wait(0.5)

        self.objects["formula_07_1"] = text_07_1
        self.objects["formula_07_2"] = text_07_2
        self.objects["formula_07_3"] = text_07_3
        self.objects["formula_07_4"] = text_07_4
        self.objects["formula_07_5"] = text_07_5

        # 将第（2）问的所有解析文本保存到 VGroup
        self.objects["solution_part2"] = VGroup(
            self.objects["label_04"],
            self.objects["formula_04"],
            self.objects["formula_07_1"],
            self.objects["formula_07_2"],
            self.objects["formula_07_3"],
            self.objects["formula_07_4"],
            self.objects["formula_07_5"]
        )

    # ------------------------------------------------------------
    # Scene 08: 总结 - 【双结论完美清屏展示】
    # ------------------------------------------------------------
    def scene_08(self):
        # 【关键操作】：清屏，清除第（2）问的繁琐推导过程
        self.play(FadeOut(self.objects["solution_part2"]), run_time=0.5)

        # 最终结论汇总
        final_text = Text("最终结论汇总：", font_size=24, color=YELLOW)

        final_eq1 = VGroup(
            Text("(1) 椭圆方程：", font_size=20),
            MathTex(r"\frac{x^2}{16} + \frac{y^2}{12} = 1", font_size=22)
        ).arrange(RIGHT)

        final_eq2 = VGroup(
            Text("(2) 面积最大值：", font_size=20),
            MathTex(r"S_{\max} = 18", font_size=22)
        ).arrange(RIGHT)

        final_group = VGroup(final_text, final_eq1, final_eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # 【微调 2：构建 final_group 后，重新定位】
        # Y 轴定在白框下方（预留充足空间）
        final_group.next_to(self.objects["part1_conc"], DOWN, buff=0.8)
        # X 轴强行与题目左边缘对齐！
        final_group.align_to(self.objects["question_text"], LEFT)

        self.play(Write(final_group), run_time=2)
        self.wait(1)

        # 高亮展示椭圆
        ellipse = self.create_ellipse()
        self.play(Create(ellipse), run_time=1.5)
        self.wait(1)
