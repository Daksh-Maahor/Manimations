from manim import *

class BoxMove(Scene):
    def construct(self):
        box = Rectangle(height=1, width=1)
        box.set_fill(color=RED_B, opacity=0.5)
        box.set_stroke(color=GREEN_C, opacity=0.7)

        self.add(box)
        self.play(box.animate.shift(RIGHT * 2), run_time=2)
        self.play(box.animate.shift(UP * 3), run_time=2)
        self.play(box.animate.shift(DOWN * 5 + LEFT * 5), run_time=2)
        self.play(box.animate.shift(UP * 1.5 + RIGHT * 1), run_time=2)

class FittingObjects(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6, y_length=6)
        axes.to_edge(LEFT, buff=0.5)

        circle = Circle(radius=1)
        circle.set_stroke(width=6, color=YELLOW)
        circle.set_fill(color=RED_C, opacity=0.8)
        circle.to_edge(DR, buff=0)

        triangle = Triangle()
        triangle.set_stroke(color=ORANGE, width=10)
        triangle.set_fill(color=GREY)
        triangle.height = 2
        triangle.shift(DOWN * 3 + RIGHT * 3)

        self.play(Write(axes))
        self.play(Write(circle))
        self.play(circle.animate.set_stroke(width=1).scale(0.5))
        self.play(Transform(circle, triangle), run_time=3)

class Updaters(Scene):
    def construct(self):
        rectangle = RoundedRectangle(width=4.5, height=2)
        rectangle.set_stroke(width=8, color=WHITE)
        rectangle.set_fill(color=BLUE_B)
        rectangle.shift(UP * 3 + LEFT * 4)

        mathText = MathTex("\\frac{3}{4} = 0.75").set_color_by_gradient(GREEN, PINK)
        mathText.height = 1.5
        mathText.move_to(rectangle.get_center())
        mathText.add_updater(lambda x : x.move_to(rectangle.get_center()))

        self.play(FadeIn(rectangle))
        self.play(Write(mathText))
        self.play(rectangle.animate.shift(RIGHT * 1.5 + DOWN * 5), run_time=6)
        self.wait()
        mathText.clear_updaters()
        self.play(rectangle.animate.shift(LEFT * 2 + UP * 1), run_time=6)

class Tute4(Scene):
    def construct(self):
        r = ValueTracker(0.5) # tracks the value of radius

        circle = always_redraw(lambda : Circle(r.get_value(), stroke_color=YELLOW, stroke_width=5))
        line_radius = always_redraw(lambda : Line(start=circle.get_center(), end=circle.get_bottom(), stroke_color=RED_B, stroke_width=10))
        line_circumference = always_redraw(lambda : Line(stroke_color=YELLOW, stroke_width=5).set_length(2 * PI * r.get_value()).next_to(circle, DOWN, buff=0.2))
        triangle = always_redraw(lambda : Polygon(circle.get_top(), circle.get_left(), circle.get_right(), fill_color=GREEN_C))

        self.play(LaggedStart(Create(circle), DrawBorderThenFill(line_radius), DrawBorderThenFill(triangle), run_time=4, lag_ratio=0.75))
        self.play(ReplacementTransform(circle.copy(), line_circumference), run_time=2)
        self.play(r.animate.set_value(2), run_time=5)

class GraphingMovement(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 3, 1], x_length=5, y_length=3, axis_config={"include_tip":True, "numbers_to_exclude" : [0]}).add_coordinates()
        axes.to_edge(UR)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(lambda x : x**0.5, x_range=[0, 4], color=YELLOW)
        graphing_stuff = VGroup(axes, graph, axes_labels)

        self.play(DrawBorderThenFill(axes), Write(axes_labels), run_time=5)
        self.play(Create(graph), run_time=5)
        self.play(graphing_stuff.animate.shift(DOWN * 4), run_time=5)
        self.play(axes.animate.shift(LEFT * 3), run_time=5)

class Graphing(Scene):
    def f(self, x):
        return 0.1 * x * (x-5) * (x+5)

    def construct(self):
        my_plane = NumberPlane(x_range=[-6, 6], x_length=5, y_range=[-10, 10], y_length=5)
        my_plane.shift(RIGHT * 3)

        my_function = my_plane.plot(lambda x : self.f(x), x_range=[-6, 6], color=GREEN_B)
        area = my_plane.get_area(graph=my_function, x_range=[-5, 5], color=[BLUE, YELLOW])

        label = MathTex("f(x) = 0.1x(x-5)(x+5)").next_to(my_plane, UP, buff=0.2)

        y_val = self.f(-2)

        horiz_line = Line(start=my_plane.c2p(0, y_val), end=my_plane.c2p(-2, y_val), stroke_color=YELLOW, stroke_width=1)

        self.play(DrawBorderThenFill(my_plane))
        self.play(Create(my_function), Write(label))
        self.play(FadeIn(area))
        self.play(Create(horiz_line))

class CoordinateSystem(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4, 4, 1], x_length=4, y_range=[0, 20, 5], y_length=4)
        plane.add_coordinates()
        plane.shift(LEFT * 3)
        plane_graph = plane.plot(lambda x : x**2, x_range=[-4, 4], color=GREEN)
        area = plane.get_riemann_rectangles(graph=plane_graph, x_range=[-2, 2], dx=0.05)

        axes = Axes(x_range=[-4, 4, 1], x_length=4, y_range=[-20, 20, 5], y_length=4)
        axes.add_coordinates()
        axes.shift(RIGHT * 3)
        axes_graph = axes.plot(lambda x : 2*x, x_range=[-4, 4], color=YELLOW)
        v_lines = axes.get_vertical_lines_to_graph(axes_graph, x_range=[-3, 3], num_lines=12)

        self.play(Write(plane), Create(axes))
        self.play(Create(plane_graph), Create(axes_graph), run_time=2)
        self.add(area, v_lines)
        self.wait(2)
