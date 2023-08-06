from typing import Callable

# fmt: off
UBUNTU_FIREFOX_SYSTEM: tuple[str, str] = (
    ("0", "X11; Ubuntu; Linux x86_64"),
)

UBUNTU_CHROME_SYSTEM: tuple[str, str] = (
    ("0", "X11; Linux x86_64"),
)

UBUNTU_VERSION: tuple[str, Callable] = (
    ("0", lambda _: ""),
)

UBUNTU_BROWSER_SYSTEM = {
    "firefox": UBUNTU_FIREFOX_SYSTEM,
    "chrome": UBUNTU_CHROME_SYSTEM,
}
# fmt: on
