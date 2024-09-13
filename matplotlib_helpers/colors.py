import matplotlib.colors


def set_lightness(color, lightness):
    rgb = matplotlib.colors.to_rgb(color)
    hsv = matplotlib.colors.rgb_to_hsv(rgb)
    hsv[-1] = hsv[-1] * lightness
    rgb = matplotlib.colors.hsv_to_rgb(hsv)
    return rgb
