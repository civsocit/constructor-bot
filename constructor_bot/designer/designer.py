import io
import textwrap

from PIL import Image, ImageDraw, ImageFont

from ..settings import DesignerSettings


def center_text(img, font, text, color):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((img.width - text_width) / 2, (img.height - text_height) / 2)
    draw.text(position, text, color, font=font, align="center")
    return img


def add_text_on_image(image: bytes, text: str) -> bytes:
    # Create PIL image object
    pil_image = Image.open(io.BytesIO(image))

    # Create PIL font object
    font = ImageFont.truetype(DesignerSettings.path_to_font(), DesignerSettings.font_size())

    # Wrap text
    text = "\n".join(textwrap.wrap(text, width=DesignerSettings.max_text_width()))

    # Draw text at center of image
    center_text(pil_image, font, text, DesignerSettings.text_color())

    # Convert back to bytes
    with io.BytesIO() as output:
        pil_image.save(output, format="PNG")
        return output.getvalue()
