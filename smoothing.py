import math

def _pad(I, k):
    h, w = len(I), len(I[0])
    H = h + 2 * k
    W = w + 2 * k
    P = [[0.0] * W for _ in range(H)]
    for y in range(H):
        sy = y - k
        if sy < 0:
            sy = 0
        elif sy >= h:
            sy = h - 1
        for x in range(W):
            sx = x - k
            if sx < 0:
                sx = 0
            elif sx >= w:
                sx = w - 1
            P[y][x] = I[sy][sx]
    return P

def _convolve2d(I, kernel):
    kh = len(kernel)
    kw = len(kernel[0])
    k = kh // 2
    S = sum(sum(row) for row in kernel)
    if S == 0:
        S = 1.0
    h, w = len(I), len(I[0])
    P = _pad(I, k)
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            acc = 0.0
            for i in range(kh):
                for j in range(kw):
                    acc += kernel[i][j] * P[y + i][x + j]
            out[y][x] = acc / S
    return out

def box_filter(I, k):
    size = 2 * k + 1
    kernel = [[1.0] * size for _ in range(size)]
    return _convolve2d(I, kernel)

def median_filter(I, k):
    h, w = len(I), len(I[0])
    P = _pad(I, k)
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            win = []
            for i in range(2 * k + 1):
                for j in range(2 * k + 1):
                    win.append(P[y + i][x + j])
            win.sort()
            n = len(win)
            if n % 2 == 1:
                out[y][x] = win[n // 2]
            else:
                out[y][x] = 0.5 * (win[n // 2 - 1] + win[n // 2])
    return out

def gaussian_kernel(sigma):
    k = max(1, int(round(3 * sigma)) - 1)
    if k < 1:
        k = 1
    size = 2 * k + 1
    kernel = [[0.0] * size for _ in range(size)]
    total = 0.0
    for i in range(size):
        for j in range(size):
            x = i - k
            y = j - k
            v = math.exp(-(x * x + y * y) / (2.0 * sigma * sigma))
            kernel[i][j] = v
            total += v
    for i in range(size):
        for j in range(size):
            kernel[i][j] /= total
    return kernel

def gaussian_filter(I, sigma):
    return _convolve2d(I, gaussian_kernel(sigma))

def sigma_filter(I, k, sigma):
    h, w = len(I), len(I[0])
    P = _pad(I, k)
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = I[y][x]
            lo = c - sigma
            hi = c + sigma
            s = 0.0
            n = 0
            for i in range(2 * k + 1):
                for j in range(2 * k + 1):
                    v = P[y + i][x + j]
                    if lo <= v <= hi:
                        s += v
                        n += 1
            out[y][x] = (s / n) if n > 0 else c
    return out

def abs_diff_map(A, B):
    h, w = len(A), len(A[0])
    out = [[0.0] * w for _ in range(h)]
    m = 0.0
    for y in range(h):
        for x in range(w):
            d = abs(A[y][x] - B[y][x])
            out[y][x] = d
            if d > m:
                m = d
    if m > 0:
        for y in range(h):
            for x in range(w):
                out[y][x] = out[y][x] / m * 255.0
    return out