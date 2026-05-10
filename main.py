import math
from PIL import Image #beklenilen pillow library


# görüntüyü matrise dönüştürme
# Renkli bir bitmap görüntüsünü üç matrise (R, G, B) dönüştürmek.
def image_to_matrices(image_path):
    # Görüntüyü aç ve RGB modunda olduğundan emin ol
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    red_matrix = [[0 for _ in range(width)] for _ in range(height)]
    green_matrix = [[0 for _ in range(width)] for _ in range(height)]
    blue_matrix = [[0 for _ in range(width)] for _ in range(height)]

    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            red_matrix[y][x] = r
            green_matrix[y][x] = g
            blue_matrix[y][x] = b

    return red_matrix, green_matrix, blue_matrix, width, height

# matrisi görüntüye dönüştürme
# Amaç: RGB matrislerini tekrar görüntülenebilir/kaydedilebilir bir görsele dönüştürmek
def matrices_to_image(r_m, g_m, b_m, width, height, output_path):
    new_img = Image.new("RGB", (width, height))
    pixels = new_img.load()

    for y in range(height):
        for x in range(width):
            r = max(0, min(255, int(r_m[y][x])))
            g = max(0, min(255, int(g_m[y][x])))
            b = max(0, min(255, int(b_m[y][x])))
            pixels[x, y] = (r, g, b)

    new_img.save(output_path)


def apply_rotation(r, g, b, w, h, angle_deg):
    rad = math.radians(angle_deg)
    cx, cy = w // 2, h // 2
    nr = [[0] * w for _ in range(h)]
    ng = [[0] * w for _ in range(h)]
    nb = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            tx, ty = x - cx, y - cy
            ox = int(tx * math.cos(rad) + ty * math.sin(rad) + cx)
            oy = int(-tx * math.sin(rad) + ty * math.cos(rad) + cy)
            if 0 <= ox < w and 0 <= oy < h:
                nr[y][x], ng[y][x], nb[y][x] = r[oy][ox], g[oy][ox], b[oy][ox]
    return nr, ng, nb


def apply_scaling(r, g, b, w, h, factor):
    nw, nh = int(w * factor), int(h * factor)
    nr = [[0] * nw for _ in range(nh)]
    ng = [[0] * nw for _ in range(nh)]
    nb = [[0] * nw for _ in range(nh)]
    for y in range(nh):
        for x in range(nw):
            old_x, old_y = int(x / factor), int(y / factor)
            if 0 <= old_x < w and 0 <= old_y < h:
                nr[y][x], ng[y][x], nb[y][x] = r[old_y][old_x], g[old_y][old_x], b[old_y][old_x]
    return nr, ng, nb, nw, nh


def apply_skewing(r, g, b, w, h, angle_deg):
    rad = math.tan(math.radians(angle_deg))
    new_w = int(w + abs(rad * h))
    nr = [[0 for _ in range(new_w)] for _ in range(h)]
    ng = [[0 for _ in range(new_w)] for _ in range(h)]
    nb = [[0 for _ in range(new_w)] for _ in range(h)]
    for y in range(h):
        for x in range(new_w):
            old_x = int(x - rad * y)
            if 0 <= old_x < w:
                nr[y][x], ng[y][x], nb[y][x] = r[y][old_x], g[y][old_x], b[y][old_x]
    return nr, ng, nb, new_w, h


def apply_transpose(r, g, b, w, h):
    nr = [[r[y][x] for y in range(h)] for x in range(w)]
    ng = [[g[y][x] for y in range(h)] for x in range(w)]
    nb = [[b[y][x] for y in range(h)] for x in range(w)]
    return nr, ng, nb, h, w


def apply_greyscale(r, g, b, w, h):
    for y in range(h):
        for x in range(w):
            avg = (r[y][x] + g[y][x] + b[y][x]) // 3
            r[y][x] = g[y][x] = b[y][x] = avg
    return r, g, b


def apply_edge_detection(r, g, b, w, h):
    edge_m = [[0] * w for _ in range(h)]
    for y in range(h - 1):
        for x in range(w - 1):
            # Check brightness difference between neighbors
            val = (r[y][x] + g[y][x] + b[y][x]) // 3
            val_right = (r[y][x + 1] + g[y][x + 1] + b[y][x + 1]) // 3
            val_down = (r[y + 1][x] + g[y + 1][x] + b[y + 1][x]) // 3
            diff = abs(val - val_right) + abs(val - val_down)
            edge_m[y][x] = 255 if diff > 30 else 0
    return edge_m, edge_m, edge_m


def main():
    filename = input("Enter image filename: ")
    try:
        r, g, b, w, h = image_to_matrices(filename)
    except:
        print("Could not load file.")
        return

    print("\nTransformations:\n1. Rotate\n2. Scale\n3. Skew\n4. Transpose\n5. Greyscale\n6. Edge Detection")
    choice = input("Select (1-6): ")

    if choice == '1':
        angle = float(input("Degrees: "))
        r, g, b = apply_rotation(r, g, b, w, h, angle)
    elif choice == '2':
        factor = float(input("Scale (e.g., 0.5): "))
        r, g, b, w, h = apply_scaling(r, g, b, w, h, factor)
    elif choice == '3':
        angle = float(input("Skew angle: "))
        r, g, b, w, h = apply_skewing(r, g, b, w, h, angle)
    elif choice == '4':
        r, g, b, w, h = apply_transpose(r, g, b, w, h)
    elif choice == '5':
        r, g, b = apply_greyscale(r, g, b, w, h)
    elif choice == '6':
        r, g, b = apply_edge_detection(r, g, b, w, h)

    matrices_to_image(r, g, b, w, h, "output.jpg")
    print("Success! Saved as 'output.jpg'")


if __name__ == "__main__":
    main()