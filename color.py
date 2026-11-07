import math

def log_transform(I, c=None):
    h, w = len(I), len(I[0])
    rmin = min(min(row) for row in I)
    rmax = max(max(row) for row in I)
    denom = math.log1p(rmax) - math.log1p(rmin)
    if c is None:
        c = 255.0 / denom if denom > 0 else 1.0
    base = math.log1p(rmin)
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            out[y][x] = c * (math.log1p(I[y][x]) - base)
    return out

def gamma_transform(I, gamma, c=None):
    h, w = len(I), len(I[0])
    rmin = min(min(row) for row in I)
    rmax = max(max(row) for row in I)
    rmin_g = rmin ** gamma
    rmax_g = rmax ** gamma
    denom = rmax_g - rmin_g
    if c is None:
        c = 255.0 / denom if denom > 0 else 1.0
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            out[y][x] = c * (I[y][x] ** gamma - rmin_g)
    return out


def binarize(I, threshold):
    h, w = len(I), len(I[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            out[y][x] = 255.0 if I[y][x] >= threshold else 0.0
    return out

def intensity_clip_const(I, lo, hi, const):
    h, w = len(I), len(I[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            v = I[y][x]
            out[y][x] = v if lo <= v <= hi else const
    return out

def intensity_clip_keep(I, lo, hi):
    h, w = len(I), len(I[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            out[y][x] = I[y][x]
    return out