from typing import Callable

from packaging.version import Version

# fmt: off
WINDOWS_SYSTEM: tuple[str, str] = (
    ("0", "Windows NT {os_version}; Win64; x64"),
)

WINDOWS_VERSION: tuple[str, Callable] = (
    ("0", lambda v: str(Version(v).major) + ".0"),
)

WINDOWS_BROWSER_SYSTEM = {
    "firefox": WINDOWS_SYSTEM,
    "chrome": WINDOWS_SYSTEM,
}
# fmt: on
