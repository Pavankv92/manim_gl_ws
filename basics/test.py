# These are the examples from manimGL :  https://github.com/3b1b/manim/blob/master/docs/source/getting_started/example_scenes.rst
# all the credits goes to the origianal author.


from manim_imports import *


class MyScene(
    Scene
):  # Renamed the class to MyScene to avoid conflict and be more descriptive
    def construct(self):
        # --- Choose your font from the list ---
        font_name = "Snell Roundhand"  # Or "Brush Script MT", etc.

        # Create the text with underline using the new function
        # Using DARK_BLUE for the gradient as in your provided code
        my_mobject = create_text_with_underline(
            text_str="Markup Text",
            font_name=font_name,
            color_gradient=(DARK_BLUE, WHITE, DARK_BLUE),
            font_size=100,  # Using 1.5, adjust if you want it larger/smaller
            underline_thickness=2,
        )

        # 1. Show creation of the combined mobject
        self.play(ShowCreation(my_mobject))
        self.wait(1)

        self.play(my_mobject.animate.to_edge(UP))  # Shift 3 units to the right
        self.wait(1)
        self.embed()


class InteractiveDevelopment(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEG))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text(
            """
                In general, using the interactive shell
                is very helpful when developing new scenes
            """
        )
        self.play(Write(text))
        self.embed()


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary complex functions, treating the points defining the mobject as complex numbers.

        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function, which takes in functions form R^3 to R^3
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2],
                ]
            ),
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    def construct(self):
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
                The most important difference between Text and TexText is that\n
                you can change the font more easily, but can't use the LaTeX grammar
                """,
            font="Arial",
            font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE},
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN},
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED},
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            Tex("A^2", "+", "B^2", "=", "C^2"),
            Tex("A^2", "=", "C^2", "-", "B^2"),
            # Creates a LaTeX mobject for the expression A^2 = (C + B)(C - B).
            # The isolate keyword tells ManimGL to treat each string in the list as a separate submobject.
            # This means "A^2" and everything in to_isolate (["B", "C", "=", "(", ")"]) will be their own submobjects.
            # Why is this useful?
            # When you animate or color parts of the equation, you can target "A^2", "B", "C", "=", "(", and ")" individually.
            # It also helps with animations like TransformMatchingTex, which can match and animate these parts separately.
            # Example:
            # If you want to color all "B"s green, you can do:
            # and only the "B" submobjects will be colored.
            # Summary:
            # The isolate argument makes specified substrings their own submobjects for easier animation and styling.
            # Tex("A^2 = (C + B)(C - B)", isolate=["A^2", *to_isolate]),
            Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate]),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=["A", *to_isolate]),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map(
                {
                    "A": BLUE,
                    "B": TEAL,
                    "C": GREEN,
                }
            )

        play_kw = {"run_time": 2}
        self.add(lines[0])

        self.play(
            TransformMatchingTex(
                lines[0].copy(),
                lines[1],
                path_arc=90 * DEG,
            ),
            **play_kw
        )
        self.wait()

        # Now, we could try this again on the next line...
        self.play(TransformMatchingTex(lines[1].copy(), lines[2]), **play_kw)
        self.wait()

        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(),
                lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                },
            ),
            **play_kw
        )
        self.wait()
        new_line2 = Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate])
        new_line2.replace(lines[2])
        new_line2.match_style(lines[2])

        self.play(
            TransformMatchingTex(
                new_line2,
                lines[3],
            ),
            **play_kw
        )
        self.wait(3)
        self.play(FadeOut(lines, RIGHT))
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)

        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI / 2}

        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, source, **kw))
        self.wait()
        self.embed()


class UpdaterExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)
        brace = always_redraw(Brace, square, UP)
        label = VGroup(
            Text("width= "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            ),
        )
        text, number = label
        label.arrange(RIGHT)

        # always(label.next_to, brace, UP)
        # this ensures that the method decimal.next_to(square) is called every frame
        # you can also use lambda functions to do that
        label.add_updater(lambda m: m.next_to(brace, UP))
        # when the function value itself changes, use the f_always.
        f_always(number.set_value, lambda: square.get_width())
        # you could also write an updater function to do the same
        # number.add_updater(lambda m: m.set_value(square.get_width()))
        self.add(square, brace, label)
        self.play(square.animate.scale(2), rate_func=there_and_back, run_time=2)
        self.wait()
        self.play(square.animate.set_width(5, stretch=True), run_time=3)
        self.wait()
        self.play(square.animate.set_width(2), run_time=3)
        self.wait()

        w0 = square.get_width()
        now = self.time
        square.add_updater(lambda m: m.set_width(w0 * math.cos(self.time - now)))
        self.wait(4 * PI)


class CoordinateSystemExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=(-1, 10),
            y_range=(-2, 2, 0.5),
            axis_config={"stroke_color": GREEN_A, "stroke_width": 2},
            y_axis_config={
                "include_tip": False,
            },
        )
        axes.add_coordinate_labels(font_size=20, num_decimal_places=1)
        self.add(axes)
        self.wait()

        dot = Dot()
        dot.set_fill(RED, opacity=1)
        dot.set_stroke(RED, width=2)

        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))

        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(ShowCreation(h_line))
        self.play(ShowCreation(v_line))

        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(axes.animate.scale(0.75).to_corner(UL), run_time=2)
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))


class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        # By default, it draws it so as to somewhat smoothly interpolate
        # between sampled points (x, f(x)).  If the graph is meant to have
        # a corner, though, you can set use_smoothing to False
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # For discontinuous functions, you can specify the point of
        # discontinuity so that it does not try to draw over the gap.
        step_graph = axes.get_graph(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
            color=GREEN,
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(FadeOut(step_graph), FadeOut(step_label), ShowCreation(parabola))
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot()
        dot.set_fill(RED, opacity=1)
        dot.set_stroke(RED, width=2)

        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        f_always(dot.move_to, lambda: axes.i2gp(x_tracker.get_value(), parabola))

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()


class SurfaceExample(Scene):
    CONFIG = {"camera_config": ThreeDCamera}

    import os

    os.makedirs("downloads", exist_ok=True)

    def construct(self):
        surface_text = Text("Use 3d scenes they area amazing!")
        surface_text.fix_in_frame()
        self.play(surface_text.animate.to_edge(UP))
        # self.add(surface_text)
        self.wait()

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)

        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        # set camera perspective
        frame = self.camera.frame
        frame.set_euler_angles(theta=-30 * DEG, phi=70 * DEG)

        surface = surfaces[0]
        self.play(
            FadeIn(surface), ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3)
        )

        for mob in surfaces:
            mob.add(mob.mesh)

        surface.save_state()

        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(Transform(surface, surfaces[1]), run_time=3)

        self.play(
            Transform(surface, surfaces[2]),
            frame.animate.increment_phi(-10 * DEG),
            frame.animate.increment_theta(-20 * DEG),
            run_time=3,
        )

        # add ambient rotation

        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # light position

        light_text = Text("You can move the light source!")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Move me!")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()


class OpeningManimExample(Scene):
    def construct(self):
        intro_words = Text(
            """ 
                    The sole focus of this channel is to 
                    simplify the German Grammar. 
                """
        )

        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        # Linear Transform
        grid = NumberPlane((-10, 10), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        linear_transform_words = VGroup(
            Text("This is what a matrix"), IntegerMatrix(matrix), Text("looks like")
        )

        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(BLACK)

        self.play(
            ShowCreation(grid), FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        # complex map
        c_grid = ComplexPlane()
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        complex_map_words = TexText(
            """
                                    Just some random shit!!!
                                    """
        )
        complex_map_words.to_corner(UR)
        complex_map_words.set_stroke(BLACK)
        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2), run_time=6
        )
        self.wait(2)
