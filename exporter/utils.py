""" Some utils function, some are ported from latest xlsxwriter. """


def pixels_to_height(pixels):
    # Convert the height of a cell from pixels to character units.
    return 0.75 * pixels


def pixels_to_width(pixels):
    # Convert the width of a cell from pixels to character units.
    max_digit_width = 7.0  # For Calabri 11.
    padding = 5.0

    if pixels <= 12:
        width = pixels / (max_digit_width + padding)
    else:
        width = (pixels - padding) / max_digit_width

    return width


def get_tolerance(tolerance_percent: int, raw_value):
    return raw_value + (raw_value * (tolerance_percent / 100))

# CONSTANT
CONFIG_PREFIX = 'xlsx_image_export_odoo'
