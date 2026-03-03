"""
动态曲线动点标准范例（CRITICAL - 禁止写死坐标）

================================================================================
【重要系统提示 - 必须严格遵守】
================================================================================

当遇到解析几何、动点轨迹类的需求时，**严禁写死静态坐标**。

必须参考本范例采用以下标准模式：

1. **参数方程法**：使用参数 t 的方程描述曲线点位置
   - 椭圆：P(t) = (a*cos(t), b*sin(t))
   - 双曲线：P(t) = (a*sec(t), b*tan(t))
   - 抛物线：P(t) = (p*t², 2*p*t)

2. **ValueTracker**：使用 ValueTracker 追踪参数 t 的值，实现动画驱动

3. **always_redraw**：使用 always_redraw(lambda: ...) 实现实时更新

4. **动态关联**：需要联动的图形（线段、三角形、角度）都必须使用 always_redraw

5. **禁止以下写法**：
   ❌ 禁止：point.animate.move_to([x, y]) + wait(1) + point.animate.move_to([x', y'])
   ❌ 禁止：硬编码多个静态位置
   ❌ 禁止：使用 Transform 进行点之间的跳跃式动画

6. **正确写法**：
   ✅ 使用：ValueTracker + always_redraw + self.play(tracker.animate.set_value(...))

================================================================================

下面展示完整可运行的示例代码，请 LLM 严格模仿此模式。
================================================================================
"""

from manim import *
import numpy as np


class EllipseMovingPointExample(Scene):
    """
    椭圆动点完整示例。

    场景：椭圆 x²/a² + y²/b² = 1 上，点 P 从 t₁ 运动到 t₂，
    同时显示焦点三角形 F₁PF₂ 实时变化。
    """

    def construct(self):
        # ================================
        # Step 1: 定义椭圆参数和参数方程
        # ================================
        a = 4.0  # 半长轴
        b = 3.0  # 半短轴

        # 【核心】椭圆参数方程：P(t) = (a*cos(t), b*sin(t))
        def ellipse_point(t: float) -> np.ndarray:
            """计算椭圆上参数 t 对应的点坐标。"""
            x = a * np.cos(t)
            y = b * np.sin(t)
            return np.array([x, y, 0.0])

        # 绘制椭圆
        ellipse = Ellipse(
            width=2 * a,
            height=2 * b,
            color=BLUE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.8
        )
        self.add(ellipse)

        # ================================
        # Step 2: 标注几何特征（焦点等）
        # ================================
        c = np.sqrt(a**2 - b**2)  # 焦距

        focus_f1 = Dot(point=[-c, 0, 0], color=YELLOW, radius=0.06)
        focus_f2 = Dot(point=[c, 0, 0], color=YELLOW, radius=0.06)

        self.add(focus_f1, focus_f2)

        # ================================
        # Step 3: 创建动点 P - ValueTracker 模式
        # ================================
        # 【核心】使用 ValueTracker 追踪参数 t
        t_tracker = ValueTracker(0.0)

        # 【核心】使用 always_redraw 创建动态点
        # 每一帧都会重新计算位置，实现平滑动画
        point_p = always_redraw(
            lambda: Dot(
                point=ellipse_point(t_tracker.get_value()),
                color=RED,
                radius=0.08
            )
        )

        # 点的标签（可选，也可以是 MathTex 显示坐标）
        label_p = always_redraw(
            lambda: Text("P", font_size=20, color=WHITE).next_to(
                ellipse_point(t_tracker.get_value()),
                UP + RIGHT,
                buff=0.15
            )
        )

        self.add(point_p, label_p)

        # ================================
        # Step 4: 创建动态关联图形 - always_redraw 模式
        # ================================
        # 【核心】所有需要联动的线段、多边形都必须使用 always_redraw
        # 这样当 t_tracker 变化时，所有图形都会自动更新

        # 线段 F₁P
        line_f1p = always_redraw(
            lambda: Line(
                start=np.array([-c, 0, 0]),
                end=ellipse_point(t_tracker.get_value()),
                color=WHITE,
                stroke_width=1.5
            )
        )

        # 线段 PF₂
        line_pf2 = always_redraw(
            lambda: Line(
                start=ellipse_point(t_tracker.get_value()),
                end=np.array([c, 0, 0]),
                color=WHITE,
                stroke_width=1.5
            )
        )

        # 【核心】动态三角形（焦点三角形）
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

        self.add(line_f1p, line_pf2, triangle_f1pf2)

        # ================================
        # Step 5: 动画 - 修改 ValueTracker 的值
        # ================================
        # 【核心】动画方式：
        # - 使用 self.play(tracker.animate.set_value(target_t))
        # - run_time 控制时长
        # - rate_func 控制速度曲线（linear = 匀速）

        self.wait(1)  # 初始展示

        # 动画：t 从 0 运动到 π（半个椭圆）
        self.play(
            t_tracker.animate.set_value(PI),
            run_time=4,
            rate_func=linear
        )

        self.wait(1)


class CircleArcExample(Scene):
    """
    圆弧动点示例。

    圆 x² + y² = r² 上，点 P 沿圆弧运动。
    """

    def construct(self):
        r = 3.0  # 半径

        def circle_point(t: float) -> np.ndarray:
            """圆的参数方程：P(t) = (r*cos(t), r*sin(t))"""
            x = r * np.cos(t)
            y = r * np.sin(t)
            return np.array([x, y, 0.0])

        # 绘制圆
        circle = Circle(radius=r, color=BLUE, stroke_width=2, fill_opacity=0.8)
        self.add(circle)

        # 创建动点
        t_tracker = ValueTracker(0.0)

        point_p = always_redraw(
            lambda: Dot(
                point=circle_point(t_tracker.get_value()),
                color=RED,
                radius=0.08
            )
        )

        # 连线到圆心
        line_op = always_redraw(
            lambda: Line(
                start=ORIGIN,
                end=circle_point(t_tracker.get_value()),
                color=WHITE,
                stroke_width=1
            )
        )

        self.add(point_p, line_op)

        # 动画：沿四分之一圆弧运动
        self.play(
            t_tracker.animate.set_value(PI / 2),
            run_time=3,
            rate_func=linear
        )


class MultiplePointsOnCurve(Scene):
    """
    多点同曲线运动示例。

    圆上两个动点 P 和 Q，以不同速度运动。
    """

    def construct(self):
        r = 3.0

        def circle_point(t: float) -> np.ndarray:
            x = r * np.cos(t)
            y = r * np.sin(t)
            return np.array([x, y, 0.0])

        circle = Circle(radius=r, color=BLUE, stroke_width=2)
        self.add(circle)

        # 【核心】两个独立的 ValueTracker，控制不同的点
        t_p_tracker = ValueTracker(0.0)
        t_q_tracker = ValueTracker(PI / 2)

        # 动点 P
        point_p = always_redraw(
            lambda: Dot(
                point=circle_point(t_p_tracker.get_value()),
                color=RED,
                radius=0.08
            )
        )

        # 动点 Q
        point_q = always_redraw(
            lambda: Dot(
                point=circle_point(t_q_tracker.get_value()),
                color=YELLOW,
                radius=0.08
            )
        )

        # 【核心】动态连接线
        line_pq = always_redraw(
            lambda: Line(
                start=circle_point(t_p_tracker.get_value()),
                end=circle_point(t_q_tracker.get_value()),
                color=WHITE,
                stroke_width=1.5
            )
        )

        # 动态三角形（包含圆心）
        triangle_opq = always_redraw(
            lambda: Polygon(
                ORIGIN,
                circle_point(t_p_tracker.get_value()),
                circle_point(t_q_tracker.get_value()),
                stroke_color=WHITE,
                stroke_width=1.5,
                fill_color=GREEN,
                fill_opacity=0.15
            )
        )

        self.add(point_p, point_q, line_pq, triangle_opq)

        # 【核心】同时动画两个点（使用 AnimationGroup）
        self.play(
            t_p_tracker.animate.set_value(PI),
            t_q_tracker.animate.set_value(3 * PI / 2),
            run_time=4,
            rate_func=linear
        )


class DynamicAngleExample(Scene):
    """
    动态角度标注示例。

    三个点 A、B、C，点 B 运动，显示 ∠ABC 的实时变化。
    """

    def construct(self):
        # 两个固定点
        point_a = Dot(point=[-2, 0, 0], color=WHITE, radius=0.06)
        point_c = Dot(point=[2, 0, 0], color=WHITE, radius=0.06)

        self.add(point_a, point_c)

        # 标签
        label_a = Text("A", font_size=18).next_to(point_a, DOWN)
        label_c = Text("C", font_size=18).next_to(point_c, DOWN)
        self.add(label_a, label_c)

        # 【核心】动点 B：沿上半圆运动
        r = 2.0
        t_tracker = ValueTracker(0.0)

        def arc_point(t: float) -> np.ndarray:
            x = r * np.cos(t)
            y = abs(r * np.sin(t))  # 只取上半圆
            return np.array([x, y, 0.0])

        point_b = always_redraw(
            lambda: Dot(
                point=arc_point(t_tracker.get_value()),
                color=RED,
                radius=0.08
            )
        )

        label_b = always_redraw(
            lambda: Text("B", font_size=18, color=WHITE).next_to(
                arc_point(t_tracker.get_value()),
                UP
            )
        )

        self.add(point_b, label_b)

        # 【核心】动态连线
        line_ab = always_redraw(
            lambda: Line(start=[-2, 0, 0], end=arc_point(t_tracker.get_value()), color=WHITE)
        )
        line_bc = always_redraw(
            lambda: Line(start=arc_point(t_tracker.get_value()), end=[2, 0, 0], color=WHITE)
        )

        # 【核心】动态角度标注
        # 使用 always_redraw 计算和显示角度
        def get_angle(p1, vertex, p2) -> float:
            """计算角度（弧度）。"""
            v1 = p1 - vertex
            v2 = p2 - vertex
            # 使用 atan2 计算角度差
            angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
            if angle < 0:
                angle += 2 * PI
            return angle

        dynamic_angle = always_redraw(
            lambda: Arc(
                radius=0.8,
                start_angle=get_angle(np.array([-2, 0, 0]), arc_point(t_tracker.get_value()), np.array([2, 0, 0])),
                angle=get_angle(np.array([2, 0, 0]), arc_point(t_tracker.get_value()), np.array([-2, 0, 0])),
                color=YELLOW,
                stroke_width=2
            )
        )

        # 显示角度数值
        angle_text = always_redraw(
            lambda: Text(
                f"{np.degrees(get_angle(np.array([-2, 0, 0]), arc_point(t_tracker.get_value()), np.array([2, 0, 0]))):.1f}°",
                font_size=20,
                color=YELLOW
            ).next_to(
                arc_point(t_tracker.get_value()),
                UP + LEFT,
                buff=0.5
            )
        )

        self.add(line_ab, line_bc, dynamic_angle, angle_text)

        # 动画
        self.play(t_tracker.animate.set_value(PI), run_time=4)


# ============================================================================
# 【给 LLM 的关键模式总结】
# ============================================================================
#
# 1. 参数方程 + ValueTracker + always_redraw = 平滑动画
# 2. 所有需要联动的对象（线、多边形、角度）都用 always_redraw
# 3. 动画使用：self.play(tracker.animate.set_value(target), run_time=X)
# 4. 禁止写死静态坐标和多次 animate + wait 的跳跃式动画
#
# ============================================================================
