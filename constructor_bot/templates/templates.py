from typing import Dict
from constructor_bot.designer import add_text_on_image


class TemplatesManager:
    def __init__(self):
        self._templates = dict()

    async def update_templates(self):
        self._templates = dict()

        # Debug ...
        from asyncio import sleep
        await sleep(1)

        # TODO: read from backend
        with open("constructor_bot/templates/example2.jpg", "rb") as photo:
            self._templates["foo"] = photo.read()
        with open("constructor_bot/templates/example1.jpg", "rb") as photo:
            self._templates["bar"] = photo.read()

    def all_templates(self) -> Dict[str, bytes]:
        return self._templates

    def process_template(self, identifier: str, text: str) -> bytes:
        return add_text_on_image(self._templates[identifier], text)
