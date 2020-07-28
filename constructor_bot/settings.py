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
        return 120  # in seconds

    @classmethod
    def access_chat_id(cls) -> int:
        return -434380704

    @classmethod
    def access_cache_ttl(cls) -> int:
        return 30  # in seconds


class DesignerSettings:
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
        return 0.088, 0.250, 0.912, 0.625

    @classmethod
    def default_width(cls) -> int:
        # A3 size 16.54 inh with 150 DPI
        # Warning: Pillow uses discrete scale factor, so, 150 or 170 DPI may be equal
        return int(16.54 * 200.0)

    @classmethod
    def default_preview_width(cls) -> int:
        # A7 size 4.13 inh with 150 DPI
        return 620
