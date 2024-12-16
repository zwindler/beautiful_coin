def get_viewbox_scale(viewbox, target_size):
    _, _, vb_width, vb_height = map(float, viewbox.split())
    scale_x = target_size[0] / vb_width
    scale_y = target_size[1] / vb_height
    return min(scale_x, scale_y)