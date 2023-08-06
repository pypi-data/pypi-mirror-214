from typing import Callable

# fmt: off
MAC_SYSTEM: tuple[str, str] = (
    ("0", "Macintosh; Intel Mac OS X {os_version}"),
)

MAC_VERSION: tuple[str, Callable] = (
    ("0", lambda v: v.replace(".", "_")),
)

MAC_BROWSER_SYSTEM = {
    "firefox": MAC_SYSTEM,
    "chrome": MAC_SYSTEM,
}
# fmt: on
