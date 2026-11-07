import os
from io_utils import load_image, save_image
from color import (log_transform, gamma_transform, binarize,
                   intensity_clip_const, intensity_clip_keep)
from smoothing import box_filter, median_filter, gaussian_filter, \
                       sigma_filter, abs_diff_map
from sharpening import unsharp_with_filter

OUT = "output"
os.makedirs(OUT, exist_ok=True)

I = load_image("images/input.png")

save_image(OUT + "/1_1_log.png", log_transform(I))

for g in (0.4, 1.0, 2.2):
    save_image(OUT + "/1_2_gamma_" + str(g) + ".png", gamma_transform(I, g))

save_image(OUT + "/1_3_bin_128.png", binarize(I, 128))

save_image(OUT + "/1_4a_clip_const.png", intensity_clip_const(I, 80, 180, 0))
save_image(OUT + "/1_4b_clip_keep.png", intensity_clip_keep(I, 80, 180))

In = load_image("images/noised.png")

for k in (1, 2):
    save_image(OUT + "/2_1_box_" + str(2 * k + 1) + ".png", box_filter(In, k))
    save_image(OUT + "/2_1_median_" + str(2 * k + 1) + ".png", median_filter(In, k))

for s in (0.5, 1.0, 2.0, 3.0):
    save_image(OUT + "/2_2_gauss_sigma_" + str(s) + ".png", gaussian_filter(In, s))

for s in (15.0, 30.0, 50.0):
    save_image(OUT + "/2_3_sigma_" + str(s) + ".png", sigma_filter(In, 1, s))

save_image(OUT + "/2_4_diff_box3.png", abs_diff_map(In, box_filter(In, 1)))
save_image(OUT + "/2_4_diff_median3.png", abs_diff_map(In, median_filter(In, 1)))
save_image(OUT + "/2_4_diff_gauss1.png", abs_diff_map(In, gaussian_filter(In, 1.0)))
save_image(OUT + "/2_4_diff_sigma30.png", abs_diff_map(In, sigma_filter(In, 1, 30.0)))

Ia = load_image("images/antialiased.png")

for fname in ("box", "median", "gauss", "sigma"):
    for k in (1, 2):
        for lam in (0.5, 1.0, 2.0):
            J = unsharp_with_filter(Ia, fname, k, lam, 1.0, 25.0)
            name = OUT + "/3_" + fname + "_k" + str(k) + "_lam" + str(lam) + ".png"
            save_image(name, J)

print("Готово:", OUT)