from manim import *
import numpy as np

class EllipticalOrbitKinematics(Scene):
    def construct(self):
        theta_tracker = ValueTracker(0)
        
        title = Text("Kinematics on Elliptical Orbit", font_size=20, color=WHITE)
        title.to_corner(UL).shift(RIGHT * 0.05 + DOWN * 0.15)
        if title.width > config.frame_width * 0.28:
            title.scale_to_width(config.frame_width * 0.28)
        
        info_group = always_redraw(lambda: VGroup(
            Text(f"θ = {theta_tracker.get_value():.2f}", font_size=16),
            Text(f"P = ({2*np.cos(theta_tracker.get_value()):.2f}, {np.sin(theta_tracker.get_value()):.2f})", font_size=16)
        ).arrange(DOWN, buff=0.3).to_edge(LEFT).shift(RIGHT * 0.05 + DOWN * 0.5))
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=5.5,
            y_length=8,
            axis_config={"include_numbers": True, "font_size": 14}
        ).to_edge(RIGHT).shift(LEFT * 0.15)
        
        ellipse = axes.plot_parametric_curve(
            lambda t: np.array([2*np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=BLUE
        )
        
        point_p = always_redraw(lambda: Dot(
            axes.c2p(2*np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value())),
            color=WHITE
        ))
        
        tangent_vector = always_redraw(lambda: Arrow(
            start=axes.c2p(2*np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value())),
            end=axes.c2p(
                2*np.cos(theta_tracker.get_value()) - 2*np.sin(theta_tracker.get_value())*0.5,
                np.sin(theta_tracker.get_value()) + np.cos(theta_tracker.get_value())*0.5
            ),
            color=YELLOW,
            buff=0
        ))
        
        normal_vector = always_redraw(lambda: Arrow(
            start=axes.c2p(2*np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value())),
            end=axes.c2p(
                2*np.cos(theta_tracker.get_value()) - np.cos(theta_tracker.get_value())*0.5,
                np.sin(theta_tracker.get_value()) - 4*np.sin(theta_tracker.get_value())*0.5
            ),
            color=RED,
            buff=0
        ))
        
        self.add(title, info_group, axes, ellipse, point_p, tangent_vector, normal_vector)
        self.play(theta_tracker.animate.set_value(2*PI), run_time=6, rate_func=linear)
        self.wait(1)