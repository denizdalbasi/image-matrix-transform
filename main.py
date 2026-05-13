import math
from PIL import Image #beklenilen pillow library

def image_to_matrices(image_path):
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
    intensity = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            intensity[y][x] = int(0.299 * r[y][x] + 0.587 * g[y][x] + 0.114 * b[y][x])

    edge_m = [[0] * w for _ in range(h)]
    threshold = 25

    for y in range(h - 1):
        for x in range(w - 1):
            diff_h = abs(intensity[y][x] - intensity[y][x + 1])
            diff_v = abs(intensity[y][x] - intensity[y + 1][x])

            if (diff_h + diff_v) > threshold:
                edge_m[y][x] = 255
            else:
                edge_m[y][x] = 0
    return edge_m, edge_m, edge_m

def apply_flip(r, g, b, w, h, mode='h'):
    if mode == 'h':
        nr = [row[::-1] for row in r]
        ng = [row[::-1] for row in g]
        nb = [row[::-1] for row in b]
    else:
        nr = r[::-1]
        ng = g[::-1]
        nb = b[::-1]
    return nr, ng, nb

def get_valid_input(prompt, target_type):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty.")
            continue

        try:
            return target_type(user_input)
        except ValueError:
            type_name = target_type.__name__
            print(f"Invalid input. Please enter a valid {type_name}.")

def main():
    filename = get_valid_input("Enter image filename: ", str)
    try:
        r, g, b, w, h = image_to_matrices(filename)
    except Exception as e:
        print(f"Initial load failed: {e}")
        return

    while True:
        print("\n--- Image Processing Menu ---")
        print("1. Rotate\n2. Scale\n3. Skew\n4. Transpose")
        print("5. Greyscale\n6. Edge Detection\n7. Flip")
        print("8. Change File Name\n9. Exit")

        choice = get_valid_input("Select (1-9): ", int)

        if choice == 1:
            angle = get_valid_input("Enter rotation degrees: ", float)
            r, g, b = apply_rotation(r, g, b, w, h, angle)
        elif choice == 2:
            factor = get_valid_input("Enter scale factor (e.g. 0.5): ", float)
            r, g, b, w, h = apply_scaling(r, g, b, w, h, factor)
        elif choice == 3:
            angle = get_valid_input("Enter skew angle: ", float)
            r, g, b, w, h = apply_skewing(r, g, b, w, h, angle)
        elif choice == 4:
            r, g, b, w, h = apply_transpose(r, g, b, w, h)
        elif choice == 5:
            r, g, b = apply_greyscale(r, g, b, w, h)
        elif choice == 6:
            r, g, b = apply_edge_detection(r, g, b, w, h)
        elif choice == 7:
            mode = get_valid_input("Horizontal or Vertical? (h/v): ", str).lower()
            r, g, b = apply_flip(r, g, b, w, h, mode)
        elif choice == 8:
            new_file = get_valid_input("Enter new filename: ", str)
            try:
                r, g, b, w, h = image_to_matrices(new_file)
                print(f"Loaded {new_file}")
                continue  # Skip the save step to avoid saving a fresh image immediately
            except:
                print("Could not load file.")
                continue
        elif choice == 9:
            print("Exiting...")
            break
        else:
            print("Choice must be between 1 and 9.")
            continue

        matrices_to_image(r, g, b, w, h, "output.jpg")
        print("Transformation applied! Saved as 'output.jpg'")

if __name__ == "__main__":
    main()