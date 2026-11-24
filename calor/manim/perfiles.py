"""Escenas de perfiles térmicos en coordenadas de los cuadernos 04.02–04.12."""
from pathlib import Path

import numpy as np
from manim import Axes, BLUE, DOWN, GREEN, LEFT, Scene, Text, UP, VMobject
from manim import ValueTracker, VGroup, always_redraw, linear, tempconfig


def renderizar_perfiles(titulo, perfiles, intervalo, limites_x, limites_y,
                        etiquetas, eje_x="x", eje_y="u", parametro="t"):
    """perfiles(t) entrega una lista de pares (abscisas, ordenadas)."""
    from IPython.display import Video, display

    class Evolucion(Scene):
        def construct(self):
            ejes = Axes(x_range=limites_x, y_range=limites_y, x_length=9.0,
                        y_length=4.3, tips=False).shift(DOWN * 0.28)
            encabezado = Text(titulo, font_size=35).to_edge(UP)
            rotulos = VGroup(Text(eje_x, font_size=23).next_to(ejes.x_axis, DOWN),
                             Text(eje_y, font_size=23).next_to(ejes.y_axis, LEFT))
            colores = [BLUE, GREEN]
            leyenda = VGroup(*[Text(nombre, color=colores[i % 2], font_size=23)
                               for i, nombre in enumerate(etiquetas)]).arrange().to_edge(DOWN)
            reloj = ValueTracker(intervalo[0])
            origen = ejes.c2p(0, 0)
            horizontal = ejes.c2p(1, 0) - origen
            vertical = ejes.c2p(0, 1) - origen

            def curvas():
                grupo = VGroup()
                for i, (x, y) in enumerate(perfiles(reloj.get_value())):
                    puntos = origen + np.outer(x, horizontal) + np.outer(y, vertical)
                    grupo.add(VMobject(color=colores[i % 2]).set_points_as_corners(puntos))
                return grupo

            valor = always_redraw(lambda: Text(
                f"{parametro} = {reloj.get_value():.2f}", font_size=24
            ).next_to(encabezado, DOWN))
            self.add(encabezado, ejes, rotulos, leyenda, valor, always_redraw(curvas))
            self.wait(4)
            self.play(reloj.animate.set_value(intervalo[1]), run_time=8, rate_func=linear)
            self.wait(3)

    with tempconfig({"pixel_width": 2560, "pixel_height": 1440, "frame_rate": 120,
                     "write_to_movie": True, "format": "mp4", "preview": False,
                     "output_file": titulo.replace(" ", "_"), "disable_caching": True}):
        escena = Evolucion()
        escena.render()
        destino = Path(escena.renderer.file_writer.movie_file_path)
    display(Video(str(destino), embed=True))
