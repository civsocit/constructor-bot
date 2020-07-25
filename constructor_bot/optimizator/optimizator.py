import textwrap
from typing import Tuple

import numpy as np
from PIL import ImageDraw, ImageFont
from scipy.optimize import minimize


def _vec_to_val(x) -> Tuple[int, int]:
    """
    Convert optimizator x[...] vector to font size and word wrap max length
    :param x: numpy array
    :return: Tuple [font size, word wrap max length]
    """
    # +1 because x may be 0
    return abs(int(x[0])) + 1, abs(int(x[1])) + 1


def _wrap_word(text: str, w: int) -> str:
    """
    Wrap word
    :param text: text
    :param w: max line length
    :return: Wrapped word
    """
    return "\n".join(textwrap.wrap(text, w, replace_whitespace=False, break_long_words=False))


def optimize_font_size(image, max_width: int, max_height: int, text: str, font_path: str) -> Tuple[int, str]:
    """
    Optimize font size and word wrap for image
    :param image: PIL Image
    :param max_width: maximum text width in px
    :param max_height: maximum text height in px
    :param text: text
    :param font_path: path to .ttf font file
    :return: Tuple[font size, wrapped text (with \n symbols)]
    """
    draw = ImageDraw.Draw(image)

    def _target(x):
        """
        Minimize me!
        :param x: [font size, word wrap value]
        :return: - font size (maximize font size)
        """
        font_size, max_text_len = _vec_to_val(x)

        wrapped = _wrap_word(text, max_text_len)
        font = ImageFont.truetype(font_path, font_size)

        text_width, text_height = draw.textsize(wrapped, font)

        if text_width > max_width or text_height > max_height:
            # Font is TOO big: minimize
            return (max_width - text_width) ** 2 + (max_height - text_height) ** 2

        return -font_size  # Font size must be biggest

    # Value to start optimization
    start = np.array([1, 1])  # x[0] - font size, x[1] - word wrap max phrase length
    best = minimize(_target, start, method="Powell")
    # Try 1, 5, 10... word wrap start values - it helps to find the best solution
    for s in range(1, 30, 5):
        start[1] = s
        res = minimize(_target, start, method="Powell")
        if abs(best.fun) < abs(res.fun):
            min_res = res

    font_size, max_text_len = _vec_to_val(best.x)
    return font_size, _wrap_word(text, max_text_len)
