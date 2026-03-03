"""
本地动态几何组件测试脚本。

测试内容：
1. 绘制标准椭圆：x²/16 + y²/9 = 1
2. 标出左右焦点
3. 使用参数方程和 ValueTracker 创建动点 P
4. 连接三焦点形成动态焦点三角形
5. 动画：t 从 0 运动到 π，时长 4 秒

核心要点：
- 演示 ValueTracker + always_redraw 的标准用法
- 展示动态几何关系的实时更新
"""

from manim import *
import numpy as np


class DynamicGeometryTest(Scene):
    """动态几何测试场景。"""

    def construct(self):
        # ================================
        # 1. 创建椭圆（标准方程：x²/16 + y²/9 = 1）
        # ================================
        ellipse = Ellipse(
            width=8,   # 2 * a, a = 4
            height=6,  # 2 * b, b = 3
            color=BLUE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.8
        )
        self.add(ellipse)

        # ================================
        # 2. 标出左右焦点
        # ================================
        # 椭圆焦点计算：c² = a² - b² = 16 - 9 = 7, c = √7
        a, b = 4, 3
        c = np.sqrt(a**2 - b**2)

        focus_f1 = Dot(point=[-c, 0, 0], color=YELLOW, radius=0.06)
        focus_f2 = Dot(point=[c, 0, 0], color=YELLOW, radius=0.06)

        label_f1 = MathTex(r"F_1", font_size=20, color=YELLOW).next_to(focus_f1, DOWN, buff=0.1)
        label_f2 = MathTex(r"F_2", font_size=20, color=YELLOW).next_to(focus_f2, DOWN, buff=0.1)

        self.add(focus_f1, focus_f2, label_f1, label_f2)

        # ================================
        # 3. 创建动点 P（使用 ValueTracker + always_redraw）
        # ================================
        # 椭圆参数方程：x = a*cos(t), y = b*sin(t)
        def ellipse_point(t: float) -> np.ndarray:
            x = a * np.cos(t)
            y = b * np.sin(t)
            return np.array([x, y, 0.0])

        # 创建 ValueTracker 追踪参数 t
        t_tracker = ValueTracker(0.0)

        # 使用 always_redraw 创建动态点 P
        point_p = always_redraw(
            lambda: Dot(
                point=ellipse_point(t_tracker.get_value()),
                color=RED,
                radius=0.08
            )
        )

        # 点 P 的标签（跟随移动）
        label_p = always_redraw(
            lambda: Text("P", font_size=20, color=WHITE).next_to(
                ellipse_point(t_tracker.get_value()),
                UP + RIGHT,
                buff=0.15
            )
        )

        self.add(point_p, label_p)

        # ================================
        # 4. 创建动态焦点三角形（F₁P F₂）
        # ================================
        # 使用 always_redraw 创建动态线段
        line_f1p = always_redraw(
            lambda: Line(
                start=np.array([-c, 0, 0]),
                end=ellipse_point(t_tracker.get_value()),
                color=WHITE,
                stroke_width=1.5
            )
        )

        line_pf2 = always_redraw(
            lambda: Line(
                start=ellipse_point(t_tracker.get_value()),
                end=np.array([c, 0, 0]),
                color=WHITE,
                stroke_width=1.5
            )
        )

        # 底边 F₁F₂（静态）
        line_f1f2 = Line(
            start=np.array([-c, 0, 0]),
            end=np.array([c, 0, 0]),
            color=WHITE,
            stroke_width=1.5
        )

        # 创建动态三角形
        triangle_f1pf2 = always_redraw(
            lambda: Polygon(
                np.array([-c, 0, 0]),
                np.array([c, 0, 0]),
                ellipse_point(t_tracker.get_value()),
                stroke_color=WHITE,
                stroke_width=2,
                fill_color=GREEN,
                fill_opacity=0.2
            )
        )

        self.add(line_f1p, line_pf2, line_f1f2, triangle_f1pf2)

        # ================================
        # 5. 显示标题和说明
        # ================================
        title = Text("动态几何测试", font_size=28).to_edge(UP, buff=0.5)

        equation = MathTex(
            r"\frac{x^2}{16} + \frac{y^2}{9} = 1",
            font_size=24
        ).next_to(ellipse, LEFT, buff=1).to_edge(UP, buff=0.3)

        param_eq = MathTex(
            r"P(t) = (4\cos(t), 3\sin(t))",
            font_size=20
        ).next_to(ellipse, RIGHT, buff=1).to_edge(UP, buff=0.3)

        info_text = Text(
            "t: 0 → π, |F₁P| + |PF₂| > |F₁F₂|",
            font_size=16,
            color=GRAY
        ).to_edge(DOWN, buff=0.3)

        self.add(title, equation, param_eq, info_text)

        # ================================
        # 6. 动画：点 P 沿椭圆运动
        # ================================
        self.wait(1)

        # 动画：t 从 0 运动到 π
        self.play(
            t_tracker.animate.set_value(PI),
            run_time=4,
            rate_func=linear
        )

        self.wait(1)


if __name__ == "__main__":
    # 使用 Manim 渲染场景
    # -ql: 最低质量（快速渲染）
    # -p: 打印进度
    scene = DynamicGeometryTest()
    scene.render()
