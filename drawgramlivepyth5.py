import sys
import os
import json
import numpy as np
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

# === Part 1: Generate or load color palette ===

COLOR_FOLDER = "coloursdrawgram"
N_COLORS = 1200

def generate_colors_drawgram(folder=COLOR_FOLDER, n_colors=N_COLORS):
    os.makedirs(folder, exist_ok=True)
    colors = []
    for i in range(n_colors):
        h = int((i * 360 / n_colors))
        s = 255
        v = 255
        hsv = np.uint8([[[h//2, s, v]]])
        rgb_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
        r, g, b = int(rgb_bgr[2]), int(rgb_bgr[1]), int(rgb_bgr[0])
        colors.append((r, g, b))
        img = np.zeros((32, 32, 3), dtype=np.uint8)
        img[:] = (b, g, r)
        filename = os.path.join(folder, f"color_{i:04d}_{r}_{g}_{b}.png")
        cv2.imwrite(filename, img)
    with open(os.path.join(folder, "colors.json"), "w") as f:
        json.dump(colors, f)
    print(f"Generated {n_colors} colors in '{folder}'")

class ColorPalette:
    def __init__(self, folder=COLOR_FOLDER):
        self.folder = folder
        self.colors = []
        self.load_colors()

    def load_colors(self):
        json_path = os.path.join(self.folder, "colors.json")
        if not os.path.exists(json_path):
            print("Palette not found, generating...")
            generate_colors_drawgram()
        with open(json_path, "r") as f:
            self.colors = json.load(f)
        self.colors = [tuple(c) for c in self.colors]
        print(f"Loaded {len(self.colors)} colors from palette.")

    def find_nearest_color(self, rgb):
        arr = np.array(self.colors)
        diff = arr - np.array(rgb)
        dist = np.linalg.norm(diff, axis=1)
        idx = np.argmin(dist)
        return self.colors[idx], idx

# === Part 2: Mapping colors and shapes to commands ===

# Example simplified command maps (add more as you want)
LINUX_COMMANDS = [
    "ls", "cd", "pwd", "mkdir", "rmdir", "rm", "cp", "mv", "touch", "cat",
    "less", "head", "tail", "chmod", "chown", "find", "file",
    # ... add more from your list
]

PYTHON_COMMANDS = [
    "print()", "input()", "if-else", "for loop", "while loop", "def function()",
    "try-except", "import module", "list append()", "dict access",
    # ... add more
]

JAVA_COMMANDS = [
    "System.out.println()", "public class", "for loop", "if-else", "try-catch",
    "import java.util.*", "ArrayList add()", "HashMap put()", "Thread start()",
    # ... add more
]

# Map color index ranges to commands for each mode
# (For demo: evenly split color indices among commands)

def get_command_from_color_index(color_idx, mode):
    if mode == 'linux':
        cmds = LINUX_COMMANDS
    elif mode == 'python':
        cmds = PYTHON_COMMANDS
    elif mode == 'java':
        cmds = JAVA_COMMANDS
    else:
        return "Unknown mode"

    # Wrap index around commands list length
    cmd = cmds[color_idx % len(cmds)]
    return cmd

# === Part 3: PyQt5 Drawing Board with eraser and run button ===

class DrawBoard(QtWidgets.QWidget):
    def __init__(self, palette):
        super().__init__()
        self.setWindowTitle("DrawGram Live Drawing Board")
        self.setGeometry(200, 200, 640, 480)
        self.palette = palette

        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)

        self.drawing = False
        self.brushSize = 6
        self.brushColor = QtGui.QColor(0, 0, 0)
        self.lastPoint = QtCore.QPoint()

        self.current_mode = 'linux'  # default mode, changes on special symbols

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Canvas
        self.canvas = QtWidgets.QLabel()
        self.canvas.setPixmap(QtGui.QPixmap.fromImage(self.image))
        layout.addWidget(self.canvas)

        # Buttons layout
        btn_layout = QtWidgets.QHBoxLayout()

        # Color picker button to pick from palette colors
        self.color_btn = QtWidgets.QPushButton("Pick Color")
        self.color_btn.clicked.connect(self.pick_color)
        btn_layout.addWidget(self.color_btn)

        # Eraser button
        self.eraser_btn = QtWidgets.QPushButton("Eraser")
        self.eraser_btn.clicked.connect(self.use_eraser)
        btn_layout.addWidget(self.eraser_btn)

        # Clear button
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_canvas)
        btn_layout.addWidget(self.clear_btn)

        # Run interpreter button
        self.run_btn = QtWidgets.QPushButton("Run DrawGram")
        self.run_btn.clicked.connect(self.run_drawgram)
        btn_layout.addWidget(self.run_btn)

        layout.addLayout(btn_layout)

    def pick_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.brushColor = color
            self.current_mode = 'linux'  # Reset mode on color pick

    def use_eraser(self):
        self.brushColor = QtGui.QColor(255, 255, 255)  # White = eraser

    def clear_canvas(self):
        self.image.fill(QtCore.Qt.white)
        self.canvas.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) & self.drawing:
            painter = QtGui.QPainter(self.image)
            pen = QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.canvas.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = False

    def run_drawgram(self):
        # Save current drawing to temporary PNG
        temp_file = "drawing_capture.png"
        self.image.save(temp_file)

        # Load image with OpenCV and process
        img = cv2.imread(temp_file)
        if img is None:
            print("Failed to load drawing image.")
            return

        # Check for special symbols in the image (simple detection)
        mode = self.detect_mode_symbol(img)
        self.current_mode = mode

        # Process image: downscale, find average colors of shapes (simplified)
        commands = self.interpret_image(img, mode)
        print("\n=== DrawGram Interpreter Output ===")
        print(f"Mode: {mode.upper()}")
        for cmd in commands:
            print("-", cmd)
        print("==================================\n")

    def detect_mode_symbol(self, img):
        # Detect presence of special symbols:
        # For demo: check if "!" (red pixel cluster), "^" (green cluster), ")" (blue cluster) is present
        # In real scenario, shape detection + OCR or symbol detection needed

        # Convert to HSV for easier color range detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Red range for '!' symbol detection
        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170,70,50])
        upper_red2 = np.array([180,255,255])
        mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
        red_count = cv2.countNonZero(mask_red)

        # Green range for '^' symbol detection
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        green_count = cv2.countNonZero(mask_green)

        # Blue range for ')' symbol detection
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_count = cv2.countNonZero(mask_blue)

        threshold = 500  # pixels

        if red_count > threshold:
            return 'python'  # !
        elif green_count > threshold:
            return 'java'  # ^
        elif blue_count > threshold:
            return 'linux'  # )
        else:
            return 'linux'  # default mode

    def interpret_image(self, img, mode):
        # Simplified: Sample pixels on a grid, map color to nearest palette color, then map to command
        commands_found = set()
        height, width, _ = img.shape

        step_x = max(1, width // 50)
        step_y = max(1, height // 50)

        for y in range(0, height, step_y):
            for x in range(0, width, step_x):
                b, g, r = img[y, x]
                if (r, g, b) == (255, 255, 255):
                    continue  # skip white
                nearest_color, idx = self.palette.find_nearest_color((r, g, b))
                cmd = get_command_from_color_index(idx, mode)
                commands_found.add(cmd)

        return sorted(commands_found)

# === Part 4: Run application ===

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Load or generate palette
    palette = ColorPalette()

    window = DrawBoard(palette)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
