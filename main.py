from manim import *
import itertools as it
import numpy as np

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

class PolarPlaneScene(Scene):
    def construct(self):
        e = ValueTracker(0.05)

        plane = PolarPlane(radius_max=3)
        plane.add_coordinates()
        plane.shift(LEFT * 2)
        graph1 = always_redraw(lambda:
            ParametricFunction(lambda t : plane.polar_to_point(2 * np.sin(3*t), t), t_range=[0, e.get_value()], color=GREEN)
        )
        dot1 = always_redraw(lambda : Dot(fill_color= GREEN, fill_opacity=0.8).scale(0.5).move_to(graph1.get_end()))

        axes = Axes(x_range=[0, 4, 1], x_length=3, y_range=[-3, 3, 1], y_length=3).shift(RIGHT * 4)
        axes.add_coordinates()
        graph2 = always_redraw(lambda :
            axes.plot(lambda x : 2 * np.sin(3 * x), x_range=[0, e.get_value()], color=GREEN)
        )
        dot2 = always_redraw(lambda : Dot(fill_color=GREEN, fill_opacity=0.8).scale(0.5).move_to(graph2.get_end()))

        title = MathTex("f(\\theta) = 2sin(3\\theta)", color=GREEN).next_to(axes, UP, buff=0.2)

        self.play(LaggedStart(
            Write(plane), Create(axes), Write(title), run_time=10, lag_ratio=0.5
        ))
        self.add(graph1, graph2, dot1, dot2)
        self.play(e.animate.set_value(PI), run_time=10, rate_func = linear)
        self.wait()

class Vectors(VectorScene):
    def construct(self):
        plane = self.add_plane(animate=True).add_coordinates()
        vector = self.add_vector([-3, -2], color=YELLOW)

        basis = self.get_basis_vectors()
        self.add(basis)
        self.vector_to_coords(vector=vector)

        vector2 = self.add_vector([2, 2])
        self.write_vector_coordinates(vector=vector2)

class Matrix(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True
        )

    def construct(self):
        matrix = [[2, 3], [-3, 2]]

        matrix_tex = MathTex("A = \\begin{bmatrix} 2 & 3 \\\ -3 & 2 \\end{bmatrix}").to_edge(UL).add_background_rectangle()

        unit_square = self.get_unit_square()
        self.get_basis_vectors()
        vect = self.get_vector([1, -2], color=PURPLE_B)
        text = always_redraw(lambda : MathTex("det(A)").set(width=0.7).move_to(unit_square.get_center()))

        rect1 = Rectangle(height=2, width=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6).shift(UP * 2 + LEFT * 2)

        circ1 = Circle(radius=1, stroke_color=BLUE_A, fill_color=BLUE_D, fill_opacity=0.6).shift(DOWN * 2 + RIGHT * 1)

        self.add_transformable_mobject(vect, unit_square, rect1, circ1)
        self.add_background_mobject(matrix_tex, text)
        self.apply_matrix(matrix)

        self.wait()

class VGroupsAnim(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-5, 5, 1], y_range=[-4, 4, 1], x_length=10, y_length=7)
        plane.add_coordinates()
        plane.shift(RIGHT * 2)

        vect1 = Line(start=plane.coords_to_point(0, 0), end=plane.coords_to_point(3, 2), stroke_color=YELLOW).add_tip()
        vect1_name = MathTex("\\vec{v}").next_to(vect1, RIGHT, buff=0.1).set_color(YELLOW)

        vect2 = Line(start=plane.coords_to_point(0, 0), end=plane.coords_to_point(-2, 1), stroke_color=RED).add_tip()
        vect2_name = MathTex("\\vec{w}").next_to(vect2, LEFT, buff=0.1).set_color(RED)

        vect3 = Line(start=plane.coords_to_point(3, 2), end=plane.coords_to_point(1, 3), stroke_color=RED).add_tip()

        vect4 = Line(start=plane.coords_to_point(0, 0), end=plane.coords_to_point(1, 3), stroke_color=GREEN).add_tip()
        vect4_name = MathTex("\\vec{v} + \\vec{w}").next_to(vect4, LEFT, buff=0.1).set_color(GREEN)

        stuff = VGroup(plane, vect1, vect1_name, vect2, vect2_name, vect3, vect4, vect4_name)

        box = RoundedRectangle(height=1.5, width=1.5, corner_radius=0.1, stroke_color=PINK).to_edge(DL)

        self.play(DrawBorderThenFill(plane), run_time=2)
        self.wait()
        self.play(GrowFromPoint(vect1, point=vect1.get_start()), Write(vect1_name), run_time=2)
        self.wait()
        self.play(GrowFromPoint(vect2, point=vect2.get_start()), Write(vect2_name), run_time=2)
        self.wait()
        self.play(Transform(vect2, vect3), vect2_name.animate.next_to(vect3, UP, buff=0.1), run_time=2)
        self.wait()
        self.play(LaggedStart(GrowFromPoint(vect4, point=vect4.get_start())), Write(vect4_name), run_time=3, lag_ratio=1)
        self.wait()
        self.add(box)
        self.wait()
        self.play(stuff.animate.move_to(box.get_center()).set(width=1.2), run_time=3)
        self.wait()

class ThreeDimensional(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6
        )

        graph = axes.plot(lambda x : x**2, x_range=[-2, 2, 1], color=YELLOW)
        rects = axes.get_riemann_rectangles(
            graph=graph, x_range=[-2, 2], dx=0.1, stroke_color=WHITE
        )

        graph2 = axes.plot_parametric_curve(
            lambda t : np.array([np.cos(t), np.sin(t), t]), 
            t_range=[-2*PI, 2*PI], 
            color=RED
        )

        self.add(axes, graph)
        self.wait()

        self.move_camera(phi = 60 * DEGREES)
        self.wait()
        self.move_camera(theta = -45 * DEGREES)

        self.begin_ambient_camera_rotation(
            rate = PI/10, about="theta"
        )
        self.wait()
        self.play(Create(rects), run_time=3)
        self.play(Create(graph2))
        self.wait()

        self.stop_ambient_camera_rotation()

        self.wait()

        self.begin_ambient_camera_rotation(
            rate = PI/10, about="phi"
        )

        self.wait(2)

        self.stop_ambient_camera_rotation()

class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()

        graph = axes.plot(lambda x : x**2, x_range=[-2, 2], color=YELLOW)
        surface = Surface(lambda u, v : axes.c2p(v * np.cos(u), v * np.sin(u), 0.5 * v**2),
                          u_range=[0, 2*PI],
                          v_range=[0, 3],
                          checkerboard_colors=[GREEN, RED])
        
        three_d_stuff = VGroup(axes, graph, surface)

        self.add(axes, graph)
        self.begin_ambient_camera_rotation(rate=PI/20)
        self.play(Create(surface), run_time = 5)
        self.play(three_d_stuff.animate.shift(LEFT * 5), run_time=5)

class ThreeDCone(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi = 45 * DEGREES, theta = -45 * DEGREES)

        axes = ThreeDAxes(y_range = [-3, 10, 3], y_length = 7).add_coordinates()

        graph = axes.plot(lambda x : x, x_range = [0, 3], color = RED_B)

        area = axes.get_area(graph=graph, x_range=[0, 3])

        e = ValueTracker(0)

        surface = always_redraw(
            lambda : Surface(
                lambda u, v : axes.c2p(v, v*np.cos(u), v*np.sin(u)),
                u_range = [0, e.get_value()],
                v_range = [0, 3],
                checkerboard_colors = [GREEN, PURPLE]
            )
        )

        self.add(axes, surface)
        self.begin_ambient_camera_rotation(rate=PI/15)
        self.play(LaggedStart(Create(graph), Create(area), run_time = 5, lag_ratio = 1))
        self.play(Rotating(area, axis=RIGHT, radians = 2 * PI, about_point = axes.c2p(0, 0, 0)), 
                  e.animate.set_value(2*PI),
                  run_time = 6,
                  rate_func = linear
        )

        self.stop_ambient_camera_rotation()
        self.wait()

def get_horizontal_line_to_graph(axes, function, x, width, color):
    result = VGroup()
    line = DashedLine(
        start = axes.c2p(0, function.underlying_function(x)),
        end = axes.c2p(x, function.underlying_function(x)),
        stroke_width = width,
        stroke_color = color
    )
    dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
    result.add(line, dot)
    return result

class Derivative(Scene):
    def construct(self):

        k = ValueTracker(-3)

        plane1 = (
            NumberPlane(x_range = [-3, 4, 1], x_length = 5, y_range = [-8, 9, 2], y_length = 5)
            .add_coordinates()
            .shift(LEFT * 3.5)
        )

        func1 = plane1.plot(
            lambda x : (1 / 3) * x ** 3, x_range = [-3, 3], color = RED_C
        )

        func1_lab = (
            MathTex("f(x) = \\frac{1}{3} {x}^{3}")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(RED_C)
        )

        moving_slope = always_redraw(
            lambda : plane1.get_secant_slope_group(
                x = k.get_value(),
                graph = func1,
                dx = 0.05,
                secant_line_length = 4,
                secant_line_color = YELLOW
            )
        )

        dot = always_redraw(
            lambda : Dot().move_to(
                plane1.c2p(k.get_value(), func1.underlying_function(k.get_value()))
            )
        )

        plane2 = (
            NumberPlane(x_range=[-3, 4, 1], x_length = 5, y_range = [0, 11, 2], y_length=5)
            .add_coordinates()
            .shift(RIGHT * 3.5)
        )

        func2 = always_redraw(
            lambda : plane2.plot(
                lambda x : x**2, x_range = [-3, k.get_value()], color=GREEN
            )
        )

        func2_lab = (
            MathTex("f'(x) = {x}^{2}")
            .set(width=2.5)
            .next_to(plane2, UP, buff=0.2)
            .set_color(GREEN)
        )

        moving_h_line = always_redraw(
            lambda : get_horizontal_line_to_graph(
                axes = plane2, function=func2, x = k.get_value(), width=4, color=YELLOW
            )
        )

        moving_v_line = always_redraw(
            lambda : DashedLine(
                start = plane2.c2p(k.get_value(), 0),
                end = plane2.c2p(k.get_value(), func2.underlying_function(k.get_value())),
                stroke_width = 4,
                stroke_color = YELLOW
            )
        )

        slope_value_text = (
            Text("Slope Value : ")
            .next_to(plane1, DOWN, buff=0.1)
            .set_color(YELLOW)
            .add_background_rectangle()
        )

        slope_value = always_redraw(
            lambda : DecimalNumber(num_decimal_places = 1)
            .set_value(func2.underlying_function(k.get_value()))
            .next_to(slope_value_text, RIGHT, buff=0.1)
            .set_color(YELLOW)
        )

        self.play(
            LaggedStart(
                DrawBorderThenFill(plane1),
                DrawBorderThenFill(plane2),
                Create(func1),
                Write(func1_lab),
                Write(func2_lab),
                run_time = 5,
                lag_ratio = 0.5
            )
        )

        self.add(moving_slope, moving_h_line, moving_v_line, func2, slope_value, slope_value_text, dot)
        self.play(k.animate.set_value(3), run_time = 15, rate_func = linear)
        self.wait()

class Test(Scene):
    def construct(self):
        S = Tex("S = ")
        expanded_sum = MathTex("\\frac{1}{1^2} + \\frac{1}{2^2} + \\frac{1}{3^2} + \\cdots").set_color_by_gradient(BLUE, GREEN, YELLOW)
        compressed_sum = MathTex("\\sum_{n=1}^{\\infty} \\frac{1}{n^2}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        answer = MathTex("= \\frac{\\pi^2}{6}").set_color_by_gradient(BLUE, GREEN, YELLOW)

        S.next_to(expanded_sum, LEFT, buff=0.1)
        answer.next_to(compressed_sum, DOWN, buff=0.1)

        self.play(Write(S), run_time = 1)
        self.play(Write(expanded_sum), run_time = 3)
        self.play(Transform(expanded_sum, compressed_sum), run_time = 3)
        self.play(Write(answer), run_time = 3)

        self.wait()

class Integral(Scene):
    def construct(self):
        title = Tex("Solving an Integral").set_color_by_gradient(BLUE, GREEN, YELLOW)
        title.add_background_rectangle()
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=1.0), run_time=2)

        integral = MathTex("\\int_{0}^{\\infty} \\frac{1}{1+x^2} \\, dx").set_color_by_gradient(BLUE, GREEN, YELLOW)

        self.play(Write(integral), run_time=3)
        self.wait(1)

        substitution = MathTex("x = \\tan{\\theta}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        differential = MathTex("dx = \\sec^2{\\theta} \\, d\\theta").set_color_by_gradient(BLUE, GREEN, YELLOW)
        substitution.next_to(integral, DOWN, buff=0.5)
        differential.next_to(substitution, DOWN, buff=0.5)
        self.play(Write(substitution), run_time=3)
        self.play(Write(differential), run_time=3)
        self.wait(1)

        integral2 = MathTex("\\int_{0}^{\\frac{\\pi}{2}} \\frac{\\sec^2{\\theta}}{1+\\tan^2{\\theta}} \\, d\\theta").set_color_by_gradient(BLUE, GREEN, YELLOW)
        integral2.move_to(integral.get_center())
        self.play(Transform(integral, integral2), run_time=3)
        self.wait(1)

        self.play(FadeOut(substitution), FadeOut(differential), run_time=2)

        integral3 = MathTex("\\int_{0}^{\\frac{\\pi}{2}} \\, d\\theta").set_color_by_gradient(BLUE, GREEN, YELLOW)
        integral3.move_to(integral.get_center())

        self.play(Transform(integral, integral3), run_time=3)

        result = MathTex("= \\frac{\\pi}{2}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        result.next_to(integral, DOWN, buff=0.5)
        self.play(Write(result), run_time=3)
        self.wait(1)

        final_result = MathTex("\\int_{0}^{\\infty} \\frac{1}{1+x^2} \\, dx = \\frac{\\pi}{2}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        final_result.move_to(integral.get_center())

        self.play(Transform(integral, final_result), FadeOut(result), run_time=3)

        self.wait()

class Integral2(Scene):
    def construct(self):
        title = Tex("Solving another Integral").set_color_by_gradient(BLUE, GREEN, YELLOW)
        title.add_background_rectangle()
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP, buff=1.0), run_time=2)

        integral = MathTex("\\int_{0}^{\\infty} \\frac{x}{1+x^4} \\, dx").set_color_by_gradient(BLUE, GREEN, YELLOW)

        self.play(Write(integral), run_time=3)
        self.wait(1)

        substitution = MathTex("x = \\sqrt{\\tan{\\theta}}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        differential = MathTex("dx = \\frac{1}{2\\sqrt{\\tan{\\theta}}}\\sec^2{\\theta} \\, d\\theta").set_color_by_gradient(BLUE, GREEN, YELLOW)
        substitution.next_to(integral, DOWN, buff=0.5)
        differential.next_to(substitution, DOWN, buff=0.5)
        self.play(Write(substitution), run_time=3)
        self.play(Write(differential), run_time=3)
        self.wait(1)

        integral2 = MathTex("\\int_{0}^{\\frac{\\pi}{2}} \\frac{\\sec^2{\\theta}}{2(1+\\tan^2{\\theta})} \\, d\\theta").set_color_by_gradient(BLUE, GREEN, YELLOW)
        integral2.move_to(integral.get_center())
        self.play(Transform(integral, integral2), run_time=3)
        self.wait(1)

        self.play(FadeOut(substitution), FadeOut(differential), run_time=2)

        integral3 = MathTex("\\int_{0}^{\\frac{\\pi}{2}} \\, \\frac{d\\theta}{2}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        integral3.move_to(integral.get_center())

        self.play(Transform(integral, integral3), run_time=3)

        result = MathTex("= \\frac{\\pi}{4}").set_color_by_gradient(BLUE, GREEN, YELLOW)
        result.next_to(integral, DOWN, buff=0.5)
        self.play(Write(result), run_time=3)
        self.wait()

class RotatingArrows(Scene):
    def construct(self):
        frequencies = [-20.0, -19.0, -18.0, -17.0, -16.0, -15.0, -14.0, -13.0, -12.0, -11.0, -10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
        amplitudes = [0.01043114926806085, 0.009643593351586916, 0.009200118733871162, 0.025638791427428538, 0.019908979279643076, 0.021855557473562406, 0.014801051219105289, 0.0027471068922981638, 0.029924248757527923, 0.05698263486120211, 0.02685387569947661, 0.012844547828340597, 0.008839273465624974, 0.08927824014057074, 0.2488978656897346, 0.08371744150573968, 0.022695653703798297, 0.011082371496437928, 0.13399256221225816, 2.0, 0.13399256221225816, 0.011082371496437928, 0.022695653703798297, 0.08371744150573968, 0.2488978656897346, 0.08927824014057074, 0.008839273465624974, 0.012844547828340597, 0.02685387569947661, 0.05698263486120211, 0.029924248757527923, 0.0027471068922981638, 0.014801051219105289, 0.021855557473562406, 0.019908979279643076, 0.025638791427428538, 0.009200118733871162, 0.009643593351586916, 0.01043114926806085, 0.007748423513743007, 0.014374086743600347]
        phase = [2.5232530916291234, -0.679956744060104, -2.5144869697381416, -2.848018830237726, -3.058893510090971, -0.5401497734800441, 2.718226552706625, -0.022577520846763528, 0.36978140526083253, -0.007150872717065652, 2.6672582609087354, -0.17476561582749248, -1.4803811076055364, -2.8027096009307777, 3.136077203369095, -0.4086862095239852, 2.763599151591405, 3.0510502735229377, 0.3753547415234295, -0.0, -0.3753547415234295, -3.0510502735229377, -2.763599151591405, 0.4086862095239852, -3.136077203369095, 2.8027096009307777, 1.4803811076055364, 0.17476561582749248, -2.6672582609087354, 0.007150872717065652, -0.36978140526083253, 0.022577520846763528, -2.718226552706625, 0.5401497734800441, 3.058893510090971, 2.848018830237726, 2.5144869697381416, 0.679956744060104, -2.5232530916291234, -0.06243398869742327, -0.42985653066333634]

        # Create a ValueTracker for the angle
        t = ValueTracker(0)

        # Number of arrows to create
        num_arrows = min(len(frequencies), len(amplitudes), len(phase))

        scale = ValueTracker(1)

        # Create a VGroup to hold all the arrows
        arrows = VGroup()

        # Loop to create arrows dynamically
        for i in range(num_arrows):
            arrow = always_redraw(lambda i=i: Arrow(
                start=(ORIGIN if i == 0 else arrows[i - 1].get_end()),
                end=(ORIGIN if i == 0 else arrows[i - 1].get_end()) +
                    scale.get_value() * amplitudes[i] * RIGHT * np.cos(frequencies[i] * t.get_value() + phase[i]) +
                    scale.get_value() * amplitudes[i] * UP * np.sin(frequencies[i] * t.get_value() + phase[i]),
                color=PINK,
                buff=0.0  # Add a small buffer to avoid overlap
            ))
            arrows.add(arrow)

        # Add the arrows to the scene
        self.add(arrows)

        self.play(
            scale.animate.set_value(0.5),
            run_time=2,
            rate_func=linear
        )

        # Pause for 2 seconds
        self.wait(2)

        # Add a traced path for the tip of the last arrow
        trace = TracedPath(lambda: arrows[-1].get_end(), stroke_color=BLUE, stroke_width=4)
        self.add(trace)

        # Animate the rotation of the arrows
        run_time = 2 * PI
        self.play(
            t.animate.set_value(run_time),
            run_time=run_time,
            rate_func=linear
        )

        # Pause to display the traced path
        self.wait()

class FourierSeriesIllustration(Scene):
    def construct(self):
        self.n_range = range(1, 11)

        # Create axes and arrow
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.shift(2 * UP)
        aaa_group.shift_onto_screen()
        axes1, arrow, axes2 = aaa_group

        # Add target function graph to the second axes
        target_func_graph = self.get_target_func_graph(axes2)
        self.add(axes1, arrow, axes2, target_func_graph)  # Add all elements to the scene

        # Generate sine graphs and partial sums
        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)

        # Add sine graphs and partial sums to the scene
        for graph in sine_graphs:
            self.play(Create(graph), run_time=1)
        for partial_sum in partial_sums:
            self.play(Create(partial_sum), run_time=1)

    def get_axes_arrow_axes(self):
        axes1 = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 1, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_tip": False}
        )
        axes1.add_coordinates()
        axes2 = axes1.copy()

        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        group = VGroup(axes1, arrow, axes2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        return group

    def get_sine_graphs(self, axes):
        sine_graphs = VGroup(*[
            axes.plot(self.generate_nth_func(n), color=color)
            for n, color in zip(self.n_range, it.cycle([BLUE, GREEN, RED, YELLOW, PINK]))
        ])
        sine_graphs.set_stroke(width=3)
        return sine_graphs

    def get_partial_sums(self, axes, sine_graphs):
        partial_sums = VGroup(*[
            axes.plot(self.generate_kth_partial_sum_func(k + 1), color=graph.get_color())
            for k, graph in enumerate(sine_graphs)
        ])
        return partial_sums

    def get_sum_tex(self):
        return MathTex(
            "\\frac{4}{\\pi} \\left(",
            "\\frac{\\cos(\\pi x)}{1}",
            "-\\frac{\\cos(3\\pi x)}{3}",
            "+\\frac{\\cos(5\\pi x)}{5}",
            "- \\cdots \\right)"
        ).scale(0.75)

    def get_sum_tex_pieces(self, sum_tex):
        return sum_tex[1:4]

    def get_target_func_tex(self):
        step_tex = MathTex(
            """
            1 \\quad \\text{if $x < 0.5$} \\\\
            0 \\quad \\text{if $x = 0.5$} \\\\
            -1 \\quad \\text{if $x > 0.5$} \\\\
            """
        )
        lb = Brace(step_tex, LEFT, buff=SMALL_BUFF)
        step_tex.add(lb)
        return step_tex

    def get_target_func_graph(self, axes):
        # Create the step function graph
        step_func = axes.plot(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
            color=YELLOW,
            stroke_width=3,
        )
        # Add a dot at the discontinuity
        dot = Dot(axes.c2p(0.5, 0), color=step_func.get_color())
        dot.scale(0.5)
        # Group the step function and dot
        step_func_group = VGroup(step_func, dot)
        return step_func_group

    def generate_nth_func(self, n):
        return lambda x: (4 / PI) * (1 / n) * (-1)**((n - 1) / 2) * np.cos(PI * n * x)

    def generate_kth_partial_sum_func(self, k):
        return lambda x: sum([
            self.generate_nth_func(n)(x)
            for n in self.n_range[:k]
        ])
    
class AdditiveFunctions(Scene):
    def construct(self):
        axes = (
            Axes(
                x_range=[0, 2.1, 1],
                x_length=12,
                y_range=[0, 7, 2],
                y_length=7
            )
            .add_coordinates()
            .to_edge(DL, buff=0.25)
        )

        func1 = axes.plot(lambda x: x**2, x_range=[0, 2], color=YELLOW)
        func1_label = (
            MathTex(r"y={x}^{2}")
            .scale(0.8)
            .next_to(func1, UR, buff=0)
            .set_color(YELLOW)
        )

        func2 = axes.plot(lambda x: x, x_range=[0, 2], color=GREEN)
        func2_label = (
            MathTex(r"y=x")
            .scale(0.8)
            .next_to(func2, UR, buff=0)
            .set_color(GREEN)
        )

        func3 = axes.plot(lambda x: x**2 + x, x_range=[0, 2], color=PURPLE_D)
        func3_label = (
            MathTex(r"y={x}^{2} + x")
            .scale(0.8)
            .next_to(func3, UR, buff=0)
            .set_color(PURPLE_D)
        )

        self.add(
            axes, func1, func2, func3,
            func1_label, func2_label, func3_label
        )
        self.wait()

        for k in np.arange(0.2, 2.1, 0.2):
            line1 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func1.underlying_function(k)),
                stroke_color=YELLOW,
                stroke_width=5
            )

            line2 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func2.underlying_function(k)),
                stroke_color=GREEN,
                stroke_width=7
            )

            line3 = DashedLine(
                start=axes.c2p(k, 0),
                end=axes.c2p(k, func3.underlying_function(k)),
                stroke_color=PURPLE,
                stroke_width=10
            )

            self.play(Create(line1), run_time=0.5)
            self.play(Create(line2), run_time=0.5)

            if(len(line1) > len(line2)):
                self.play(line2.animate.shift(UP*line1.get_length()), run_time=1)
            else:
                self.play(line1.animate.shift(UP*line2.get_length()), run_time=1)

            self.play(Create(line3), run_time=0.5)
        self.wait()

        # areas
        area1 = axes.get_riemann_rectangles(
            graph=func1,
            x_range=[0, 2],
            dx=0.1,
            color=[BLUE, GREEN]
        )

        area2 = axes.get_riemann_rectangles(
            graph=func2,
            x_range=[0, 2],
            dx=0.1,
            color=[YELLOW, PURPLE]
        )

        self.play(Create(area1), run_time=5)
        self.play(area1.animate.set_opacity(0.5))
        self.play(Create(area2), run_time=5)
        self.wait()
        for k in range(20):
            self.play(area2[k].animate.shift(UP*area1[k].height), run_time=0.25)
        self.wait()

class IntegralThroughReimannRectangles(Scene):
    def construct(self):
        # Initialize the ValueTracker for dx
        dx = ValueTracker(0.5)

        # Create the NumberPlane
        plane = NumberPlane(x_range=[-9, 9, 1], y_range=[-10, 10, 2], x_length=14, y_length=10)
        plane.add_coordinates()

        # Define the graph
        graph = plane.plot(
            lambda x: 0.00349632 * x**3 + 0.0280286 * x**2 - 0.660808 * x - 1.70342,
            x_range=[-8, 8],
            color=YELLOW
        )

        # Define the Riemann rectangles
        area = always_redraw(lambda: plane.get_riemann_rectangles(
            graph=graph,
            x_range=[-8, 8],
            dx=dx.get_value(),
            fill_opacity=0.5
        ))

        # Add the plane and graph to the scene
        self.play(Write(plane), Create(graph), run_time=2)
        self.play(Create(area), run_time=2)

        # Periodically decrease the step size (dx)
        step_sizes = [0.4, 0.3, 0.2, 0.1]  # Define the step sizes
        for step in step_sizes:
            self.play(dx.animate.set_value(step), run_time=0.5, rate_func=linear)

        # Pause to display the final result
        self.wait()

class ArcLength(Scene):
    def get_arc_lines_on_function(self, graph, plane, dx=1, line_color=WHITE, line_width=1, x_min=None, x_max=None):

        dots = VGroup()
        lines = VGroup()
        result = VGroup(dots, lines)

        x_range = np.arange(x_min, x_max, dx)
        colors = color_gradient([BLUE_B, GREEN_B], len(x_range))

        for x, color in zip(x_range, colors):
            p1 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x, graph))
            p2 = Dot().scale(0.7).move_to(plane.input_to_graph_point(x + dx, graph))
            dots.add(p1, p2)
            dots.set_fill(colors, opacity=0.8)

            line = Line(
                p1.get_center(),
                p2.get_center(),
                stroke_color=line_color,
                stroke_width=line_width,
            )
            lines.add(line)

        return result
    
    def construct(self):

        axes = (
            Axes(x_range=[-1, 4.1, 1], x_length=8, y_range=[0, 3.1, 1], y_length=6)
            .to_edge(DL)
            .add_coordinates()
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(
            lambda x: 0.1 * x * (x + 1) * (x - 3) + 1, x_range=[-1, 4], color=BLUE
        )

        # Mobjects for explaining construction of Line Integral
        dist = ValueTracker(1)

        dx = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(2, graph.underlying_function(2)),
                end=axes.c2p(2 + dist.get_value(), graph.underlying_function(2)),
                stroke_color=GREEN,
            )
        )

        dx_brace = always_redraw(lambda: Brace(dx).next_to(dx, DOWN, buff=0.1))
        dx_text = always_redraw(
            lambda: MathTex("dx").set(width=0.3).next_to(dx_brace, DOWN, buff=0)
        )

        dy = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(
                    2 + dist.get_value(),
                    graph.underlying_function(2 + dist.get_value()),
                ),
                end=axes.c2p(2 + dist.get_value(), graph.underlying_function(2)),
                stroke_color=GREEN,
            )
        )

        dy_brace = always_redraw(
            lambda: Brace(dy, direction=RIGHT).next_to(dy, RIGHT, buff=0.1)
        )
        dy_text = always_redraw(
            lambda: MathTex("dy").set(width=0.3).next_to(dy_brace, RIGHT, buff=0)
        )

        dl = always_redraw(
            lambda: Line(
                start=axes.c2p(2, graph.underlying_function(2)),
                end=axes.c2p(
                    2 + dist.get_value(),
                    graph.underlying_function(2 + dist.get_value()),
                ),
                stroke_color=YELLOW,
            )
        )

        dl_brace = always_redraw(
            lambda: BraceBetweenPoints(point_1=dl.get_end(), point_2=dl.get_start())
        )
        dl_text = always_redraw(
            lambda: MathTex("dL")
            .set(width=0.3)
            .next_to(dl_brace, UP, buff=0)
            .set_color(YELLOW)
        )

        demo_mobjects = VGroup(
            dx, dx_brace, dx_text, dy, dy_brace, dy_text, dl, dl_brace, dl_text
        )

        # Adding the Latex Mobjects for Mini-Proof
        helper_text = (
            MathTex("dL \\ approximates \\ curve \\ as \\ dx\\ approaches \\ 0")
            .set(width=6)
            .to_edge(UR, buff=0.2)
        )
        line1 = MathTex("{dL}^{2}={dx}^{2}+{dy}^{2}")
        line2 = MathTex("{dL}^{2}={dx}^{2}(1+(\\frac{dy}{dx})^{2})")
        line3 = MathTex(
            "dL = \\sqrt{ {dx}^{2}(1+(\\frac{dy}{dx})^{2}) }"
        )  # Then using surds
        line4 = MathTex("dL = \\sqrt{1 + (\\frac{dy}{dx})^{2} } dx")
        proof = (
            VGroup(line1, line2, line3, line4)
            .scale(0.8)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(helper_text, DOWN, buff=0.25)
        )

        box = SurroundingRectangle(helper_text)

        # The actual line integral
        dx_tracker = ValueTracker(1)  # Tracking the dx distance of line integral

        line_integral = always_redraw(
            lambda: self.get_arc_lines_on_function(
                graph=graph,
                plane=axes,
                dx=dx_tracker.get_value(),
                x_min=-1,
                x_max=4,
                line_color=RED,
                line_width=5,
            )
        )

        self.add(axes, labels, graph)

        self.play(Create(dx), Create(dy), run_time=1)
        self.play(Create(dl), run_time=1)

        self.add(dx_brace, dx_text, dy_brace, dy_text, dl_brace, dl_text)

        self.play(Write(line1), run_time=2)
        self.play(Write(line2), run_time=2)
        self.play(Write(line3), run_time=2)
        self.play(Write(line4), run_time=2)
        
        self.play(Write(helper_text), run_time=2)
        self.play(Create(box), run_time=1)

        self.play(dist.animate.set_value(0.5), run_time=4)

        self.play(FadeOut(demo_mobjects), FadeOut(line1, line2, line3, line4), run_time=2)

        self.play(Create(line_integral), run_time=4)

        self.play(dx_tracker.animate.set_value(0.2), run_time=4)
        self.wait()
