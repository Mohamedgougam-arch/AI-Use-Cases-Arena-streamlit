from __future__ import annotations

import base64
from pathlib import Path

# Project root: arena/ui/brand.py -> arena -> root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGO_PATH = _PROJECT_ROOT / "assets" / "invest-nl-logo.png"


def logo_exists() -> bool:
    return LOGO_PATH.is_file()


def logo_box_html(*, width: int = 48) -> str:
    """Invest-NL logo in the white rounded tile (matches Next.js landing)."""
    if not logo_exists():
        return '<div class="logo-box logo-box-fallback" aria-hidden="true">IN</div>'
    data = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return (
        f'<div class="logo-box">'
        f'<img src="data:image/png;base64,{data}" alt="Invest-NL" '
        f'width="{width}" style="width:{width}px;height:auto;object-fit:contain;display:block;" />'
        f"</div>"
    )
