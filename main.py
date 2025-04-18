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

        self.add(moving_slope, moving_h_line, func2, slope_value, slope_value_text, dot)
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
