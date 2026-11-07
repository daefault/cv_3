from smoothing import box_filter, median_filter, gaussian_filter, sigma_filter

def unsharp_mask(I, S, lam):
    h, w = len(I), len(I[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            v = (1.0 + lam) * I[y][x] - lam * S[y][x]
            if v < 0:
                v = 0
            elif v > 255:
                v = 255
            out[y][x] = v
    return out

def unsharp_with_filter(I, filter_name, k, lam, sigma_gauss=1.0, sigma_sigma_filter=25.0):
    if filter_name == "box":
        S = box_filter(I, k)
    elif filter_name == "median":
        S = median_filter(I, k)
    elif filter_name == "gauss":
        S = gaussian_filter(I, sigma_gauss)
    elif filter_name == "sigma":
        S = sigma_filter(I, k, sigma_sigma_filter)
    else:
        raise ValueError(filter_name)
    return unsharp_mask(I, S, lam)