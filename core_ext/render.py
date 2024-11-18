import cv2
import os

class VideoRenderer:
    def __init__(self, input_dir, output_file, img_format='png', output_format='mp4', fps=30):
        self.input_dir = input_dir
        self.output_file = output_file
        self.img_format = img_format
        self.output_format = output_format
        self.fps = fps
        self.frames = []

    def get_image_files(self):
        # Obtener la lista de archivos de imagen en el directorio
        image_files = [img for img in os.listdir(self.input_dir) if img.endswith(f".{self.img_format}")]
        image_files.sort()  # Asegurarse de que las imágenes estén en orden secuencial
        return image_files

    def get_video_writer(self, width, height):
        # Mapear formatos de salida a códecs compatibles
        codecs = {
            'mp4': 'mp4v',    # Códec para archivos MP4
            'avi': 'DIVX',    # Códec para archivos AVI
            'mkv': 'X264',    # Códec para archivos MKV (requiere que OpenCV tenga soporte para X264)
            'mov': 'MJPG',    # Códec para archivos MOV
            'wmv': 'WMV2',    # Códec para archivos WMV
            # Agrega otros formatos y códecs según sea necesario
        }

        # Obtener el códec basado en el formato de salida
        codec = codecs.get(self.output_format.lower())
        if not codec:
            raise ValueError(f"Formato de video no soportado: {self.output_format}")

        fourcc = cv2.VideoWriter_fourcc(*codec)
        return cv2.VideoWriter(self.output_file, fourcc, self.fps, (width, height))

    def create_video_from_images(self):
        image_files = self.get_image_files()
        if not image_files:
            print("No se encontraron imágenes en el directorio especificado.")
            return

        # Leer la primera imagen para obtener las dimensiones
        first_image = cv2.imread(os.path.join(self.input_dir, image_files[0]))
        height, width, _ = first_image.shape

        # Configurar el objeto VideoWriter
        video_writer = self.get_video_writer(width, height)

        # Añadir imágenes al video
        for image_file in image_files:
            image_path = os.path.join(self.input_dir, image_file)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error al leer la imagen {image_file}, se omitirá.")
                continue
            video_writer.write(image)

        # Finalizar y guardar el video
        video_writer.release()
        print(f"El video ha sido creado exitosamente en {self.output_file}.")

'''
Ejemplo de uso
input_dir = 'imagenes_generadas/'  # Directorio de las imágenes
output_file = 'video_salida.mp4'  # Archivo de salida con el formato deseado
img_format = 'png'  # Formato de las imágenes (por ejemplo, 'png', 'jpg')
output_format = 'mp4'  # Formato de salida del video (por ejemplo, 'mp4', 'avi')
fps = 24  # Cuadros por segundo

renderer = VideoRenderer(input_dir, output_file, img_format, output_format, fps)
renderer.create_video_from_images()
'''
