from copy import copy
from io import BytesIO
from typing import Dict, Tuple

from PIL import Image

from constructor_bot.designer import add_text_on_image
from constructor_bot.settings import DesignerSettings


class Template:
    def __init__(self, path: str, name: str):
        """
        Create image template
        :param path: path to .eps file
        """
        self._name = name

        self._pil_image = Image.open(path)
        scale = round(DesignerSettings.default_width() / self._pil_image.width)
        scale = max(scale, 1)  # Scale must be >= 1
        self._pil_image.load(scale=scale)  # High resolution

        with BytesIO() as output:
            preview = self.pil_image
            preview.thumbnail((DesignerSettings.default_preview_width(), DesignerSettings.default_preview_width()))
            preview.save(output, format="PNG")
            self._png_preview = output.getvalue()

    @property
    def name(self) -> str:
        return self._name

    @property
    def pil_image(self):
        return copy(self._pil_image)

    @property
    def preview(self) -> bytes:
        return copy(self._png_preview)


class TemplatesManager:
    def __init__(self):
        self._templates = dict()

    async def update_templates(self):
        # Debug ...
        from asyncio import sleep

        await sleep(1)

        # TODO: read from backend
        self._templates = dict()
        self._templates["blue"] = Template("constructor_bot/templates/Poster-Blue.eps", "blue")
        self._templates["red"] = Template("constructor_bot/templates/Poster-Red.eps", "red")

    def all_templates(self) -> Dict[str, Template]:
        return self._templates

    def process_template(self, identifier: str, text: str) -> Tuple[bytes, bytes]:
        return add_text_on_image(self._templates[identifier].pil_image, text)
