from core_ext import render

# valores para la generacion del video
input_dir = 'output/'
output_file = 'video_salida.avi'
img_format = 'png'
output_format = 'avi'
fps = 24
# video creado
renderer = render.VideoRenderer(input_dir, output_file, img_format, output_format, fps)
renderer.create_video_from_images()