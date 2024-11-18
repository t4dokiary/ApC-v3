import cv2
import os

class NodeImagens:
    def __init__(self, image_path, position, scale=1.0, parent=None):
        self.original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if self.original_image is None:
            raise FileNotFoundError(f"Image at path '{image_path}' could not be loaded.")
        if self.original_image.shape[2] == 3:
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2BGRA)
        self.image = self.original_image.copy()
        self.position = position
        self.scale = scale
        self.parent = parent
        self.children = []
        self.angle = 0
        if parent:
            parent.add_child(self)
        self.scale_image(self.scale)

    def add_child(self, child):
        self.children.append(child)

    def move(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)
        for child in self.children:
            child.move(dx, dy)

    def set_position(self, new_x, new_y):
        dx = new_x - self.position[0]
        dy = new_y - self.position[1]
        self.move(dx, dy)

    def rotate(self, angle):
        self.angle += angle
        for child in self.children:
            child.rotate(angle)

    def scale_image(self, scale):
        self.scale = scale
        h, w = self.original_image.shape[:2]
        new_size = (int(w * scale), int(h * scale))
        self.image = cv2.resize(self.original_image, new_size, interpolation=cv2.INTER_LINEAR)

    def draw(self, canvas):
        rotated_img = self.rotate_image(self.image, self.angle)
        x, y = map(int, self.position)  # Convertir a enteros
        h, w = rotated_img.shape[:2]
        if y < 0 or x < 0 or y >= canvas.shape[0] or x >= canvas.shape[1]:
            return
        h = min(h, canvas.shape[0] - y)
        w = min(w, canvas.shape[1] - x)
        overlay = canvas[y:y+h, x:x+w]
        alpha_mask = rotated_img[:h, :w, 3] / 255.0
        for c in range(0, 3):
            overlay[:, :, c] = (1. - alpha_mask) * overlay[:, :, c] + alpha_mask * rotated_img[:h, :w, c]
        canvas[y:y+h, x:x+w] = overlay
        for child in self.children:
            child.draw(canvas)


    def rotate_image(self, image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        cos = abs(rot_matrix[0, 0])
        sin = abs(rot_matrix[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        rot_matrix[0, 2] += (new_w / 2) - center[0]
        rot_matrix[1, 2] += (new_h / 2) - center[1]
        rotated = cv2.warpAffine(image, rot_matrix, (new_w, new_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        if rotated.shape[2] == 3:
            rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2BGRA)
        return rotated
    
    @staticmethod
    def save_image(canvas, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, canvas)
        
    @staticmethod
    def clear_canvas(canvas, background_path):
        background = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        if background is None:
            raise FileNotFoundError("Background image could not be loaded.")
        if background.shape[2] == 3:
            background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)
        if canvas.shape[2] == 3:
            # Convert background to 3 channels if canvas has only 3 channels
            background = cv2.cvtColor(background, cv2.COLOR_BGRA2BGR)
        canvas[:background.shape[0], :background.shape[1]] = background
