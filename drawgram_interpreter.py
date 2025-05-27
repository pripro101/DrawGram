import cv2
import numpy as np

def get_command(shape):
    color = shape["color"]
    shape_type = shape["type"]

    # BGR color checks (OpenCV loads images in BGR format)
    # White circle = print
    if shape_type == "circle" and np.array_equal(color, [255, 255, 255]):
        return "print('Hello World!')"
    # Red square = variable declaration
    elif shape_type == "square" and np.array_equal(color, [0, 0, 255]):
        return "x = 1"
    else:
        return None

def main():
    # Load image
    img = cv2.imread('test.png')
    if img is None:
        print("Error: Image 'test.png' not found.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours (shapes)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2
        color = img[cy, cx]  # BGR center pixel color

        shape_type = None
        if len(approx) == 3:
            shape_type = "triangle"
        elif len(approx) == 4:
            shape_type = "square"
        elif len(approx) > 4:
            shape_type = "circle"

        if shape_type:
            shapes.append({"type": shape_type, "pos": (cx, cy), "color": color})

    # Detect lines (connections)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=5)
    connections = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            connections.append(((x1, y1), (x2, y2)))

    # Sort shapes by vertical position (top to bottom)
    shapes = sorted(shapes, key=lambda s: s["pos"][1])

    # Interpreter: Map shapes to commands and execute
    variables = {}
    for shape in shapes:
        cmd = get_command(shape)
        if cmd:
            print("Running:", cmd)
            # Using exec with variables dictionary to keep state
            exec(cmd, {}, variables)

    # If variable x was declared, try printing its value after running commands
    if "x" in variables:
        print("Variable x =", variables["x"])

if __name__ == "__main__":
    main()

