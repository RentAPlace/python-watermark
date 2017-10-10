from datetime import datetime

watermark     = r".\watermark.png"
position      = (1, 0.05)
ratio         = 0.11
font          = r".\Roboto.ttf"
font_color    = (255, 255, 255)
font_position = (0.99, 0.985)
font_ratio    = 55/3072
text          = "© {} Rent A Place".format(datetime.now().year)

# ----------------------------
# DO NOT ALTER THE CODE BELOW
# ----------------------------
import os

def absoluteify(src):
    if not os.path.isabs(src):
        dirname = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(dirname, src))
    return src

watermark = absoluteify(watermark)
font      = absoluteify(font)
