from PIL import Image

def load_image(path):
    img = Image.open(path).convert("L")
    w, h = img.size
    px = img.load()
    return [[float(px[x, y]) for x in range(w)] for y in range(h)]

def save_image(path, img):
    h = len(img)
    w = len(img[0])
    out = Image.new("L", (w, h))
    px = out.load()
    for y in range(h):
        for x in range(w):
            v = img[y][x]
            if v < 0:
                v = 0
            elif v > 255:
                v = 255
            px[x, y] = int(v)
    out.save(path)

def clone(img):
    return [row[:] for row in img]

def size(img):
    return len(img[0]), len(img)