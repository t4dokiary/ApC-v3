import numpy as np
from PIL import Image
import math
import pathlib
import sys
import os

# Obtener el directorio del paquete
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.base import Base
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.texture import Texture
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from material.phong import PhongMaterial
from material.texture import TextureMaterial
from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry
from extras.movement_rig import MovementRig
from extras.directional_light import DirectionalLightHelper
from OpenGL.GL import glReadPixels, GL_RGB, GL_UNSIGNED_BYTE


class Example(Base):
    """
    Renderizar sombras usando paso de sombras por buffers de profundidad para la luz direccional.
    """

    def initialize(self):
        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 5])

        luz_ambiental = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(luz_ambiental)
        self.directional_light = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, 0])
        self.directional_light.set_position([2, 4, 0])
        self.scene.add(self.directional_light)
        direct_helper = DirectionalLightHelper(self.directional_light)
        self.directional_light.add(direct_helper)

        esfera_geometría = SphereGeometry()
        material_phong1 = PhongMaterial(
            texture=Texture("images/luna.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )
        material_piso = PhongMaterial(
            texture=Texture("images/grass.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )
        material_phong2 = PhongMaterial(
            texture=Texture("images/tierra.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        esfera1 = Mesh(esfera_geometría, material_phong1)
        esfera1.set_position([-2, 1, 0])
        self.scene.add(esfera1)

        esfera2 = Mesh(esfera_geometría, material_phong2)
        esfera2.set_position([1, 2.2, -0.5])
        self.scene.add(esfera2)

        self.renderer.enable_shadows(self.directional_light)

        piso = Mesh(RectangleGeometry(width=20, height=20), material_piso)
        piso.rotate_x(-math.pi / 2)
        self.scene.add(piso)

        # Crear carpeta 'output' si no existe
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Inicializar variables para guardar fotogramas
        self.frame_count = 0
        self.total_frames = 120  # 24 fotogramas en total
        self.seconds = 5
        self.target_fps = self.total_frames / self.seconds
        self.frame_interval = 1 / self.target_fps  # Tiempo entre cada fotograma
        self.next_frame_time = 0

    def update(self):
        # Rotar luz direccional
        self.directional_light.rotate_y(0.01337, False)
        self.rig.update(self.input, self.delta_time)

        # Guardar fotogramas si corresponde
        if self.frame_count < self.total_frames and self.time >= self.next_frame_time:
            self.save_frame()
            self.next_frame_time += self.frame_interval

        # Renderizar escena
        self.renderer.render(self.scene, self.camera)

    def save_frame(self):
        # Usar el tamaño de la pantalla definido al inicio
        width, height = 800, 600  # Reemplaza estos valores si cambias el tamaño de pantalla
        gl_pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = np.frombuffer(gl_pixels, dtype=np.uint8).reshape((height, width, 3))
        image = np.flipud(image)  # OpenGL lee de abajo hacia arriba

        # Guardar la imagen como PNG
        frame_path = os.path.join(self.output_dir, f"frame_{self.frame_count:03d}.png")
        Image.fromarray(image).save(frame_path)
        print(f"Fotograma guardado: {frame_path}")
        self.frame_count += 1


# Instanciar esta clase y ejecutar el programa
Example(screen_size=[800, 600]).run()
