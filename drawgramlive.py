import cv2
import numpy as np

drawing = False  # True if mouse is pressed
ix, iy = -1, -1
canvas = np.ones((500, 700, 3), dtype=np.uint8) * 255  # White canvas

def draw(event, x, y, flags, param):
    global ix, iy, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), thickness=3)
            ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), thickness=3)

def detect_and_run(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w//2, y + h//2
        color = img[cy, cx]

        shape_type = None
        if len(approx) == 3:
            shape_type = "triangle"
        elif len(approx) == 4:
            shape_type = "square"
        elif len(approx) > 4:
            shape_type = "circle"

        if shape_type:
            shapes.append({"type": shape_type, "pos": (cx, cy), "color": color})

    # Sort shapes top to bottom
    shapes = sorted(shapes, key=lambda s: s["pos"][1])

    variables = {}
    def get_command(shape):
        color = shape["color"]
        shape_type = shape["type"]
        if shape_type == "circle" and np.array_equal(color, [0, 0, 0]):
            return "print('Hello from Live Draw!')"
        elif shape_type == "square" and np.array_equal(color, [0, 0, 0]):
            return "x = 42"
        else:
            return None

    for shape in shapes:
        cmd = get_command(shape)
        if cmd:
            print("Running:", cmd)
            exec(cmd, {}, variables)

    if "x" in variables:
        print("Variable x =", variables["x"])

def main():
    global canvas
    cv2.namedWindow('DrawGram Live')
    cv2.setMouseCallback('DrawGram Live', draw)

    print("Draw on the window. Press 'r' to run DrawGram interpreter on your drawing.")
    print("Press 'c' to clear canvas. Press 'q' to quit.")

    while True:
        cv2.imshow('DrawGram Live', canvas)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            print("\n--- Running DrawGram Interpreter ---")
            detect_and_run(canvas)
            print("--- Done ---\n")

        elif key == ord('c'):
            canvas = np.ones((500, 700, 3), dtype=np.uint8) * 255  # Clear white canvas
            print("Canvas cleared.")

        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
