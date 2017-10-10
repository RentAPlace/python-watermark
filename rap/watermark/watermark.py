from PIL import (Image, ImageDraw, ImageFont)


def watermark(image_src, config):
    """ Adds a watermark to an image.

    Args:
       image_src (str): The original image path.
       config (config_setup.Config): The initialized configuration object.

    Returns:
       PIL.Image: The modified image.
    """
    image        = Image.open(image_src)
    watermark    = Image.open(config.watermark)
    font_size    = config.font_ratio * image.height
    font         = ImageFont.truetype(config.font, __to_px(font_size))
    draw_context = ImageDraw.Draw(image)

    relative_watermark_size = __compute_relative_watermark_size(image.size, watermark.size, config.ratio)
    relative_watermark_position = __compute_relative_position(image.size, relative_watermark_size, config.position)

    resized_watermark = watermark.resize(relative_watermark_size)
    image.paste(resized_watermark, relative_watermark_position, resized_watermark)

    text_size = draw_context.textsize(config.text, font=font)
    relative_text_position = __compute_relative_position(image.size, text_size, config.font_position)
    draw_context.text(relative_text_position, config.text, font=font, fill=(255,255,255))

    return image


def __compute_relative_position(image_size, watermark_size, position):
    image_width, image_height = image_size
    watermark_width, watermark_height = watermark_size
    x_ratio, y_ratio = position
    return (int((image_width - watermark_width) * x_ratio),
            int((image_height - watermark_height) * y_ratio))


def __compute_relative_watermark_size(image_size, watermark_size, ratio):
    image_width, image_height = image_size
    watermark_width, watermark_height = watermark_size
    size_relative_segment, _ = min(("width", image_width/image_height),
                                   ("height", image_height/image_width),
                                   key=__snd)

    if size_relative_segment == "width":
        watermark_aspect_ratio = watermark_height/watermark_width
        relative_watermark_width  = int(image_width * ratio)
        relative_watermark_height = int(relative_watermark_width * watermark_aspect_ratio)
    else:
        watermark_aspect_ratio = watermark_width/watermark_height
        relative_watermark_height = int(image_height * ratio)
        relative_watermark_width  = int(relative_watermark_height * watermark_aspect_ratio)
    return (relative_watermark_width, relative_watermark_height)


def __snd(elems):
    _, b = elems
    return b


def __to_px(pt):
    return int(pt * (4/3))
