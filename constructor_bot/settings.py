import os
from typing import Tuple

from dotenv import load_dotenv

load_dotenv()


class BotSettings:
    @classmethod
    def token(cls) -> str:
        token = os.getenv("TOKEN")
        if not token:
            raise ValueError("Token must be specified (missing .env file or TOKEN environment variable?)")
        return token

    @classmethod
    def templates_refresh_time(cls) -> int:
        return 30  # Refresh templates list every 30 seconds


class DesignerSettings:
    @classmethod
    def max_text_width(cls) -> int:
        # TODO: read that parameter from backend
        return 20

    @classmethod
    def path_to_font(cls) -> str:
        # TODO: load font from backend
        from os.path import abspath, dirname, join

        return join(abspath(dirname(__file__)), "designer", "main.ttf")

    @classmethod
    def text_color(cls) -> Tuple[int, int, int]:
        # TODO: read that parameter from backend
        return 255, 255, 255

    @classmethod
    def text_position(cls) -> Tuple[float, float, float, float]:
        # TODO: read that parameter from backend
        # Relative position x0, y0, x1, y1
        return (0.088, 0.250, 0.912, 0.625)
