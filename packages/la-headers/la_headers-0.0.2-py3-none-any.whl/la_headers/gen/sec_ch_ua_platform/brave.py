# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
# Yes, quotes are inclused in the string.

# fmt: off
BRAVE_SEC_CH_UA_PLATFORM_WINDOWS = (
    ("114.0", None),
    ("0", '"Windows"'),
)


BRAVE_SEC_CH_UA_PLATFORM_LINUX = (
    ("0", '"Linux"'),
)


BRAVE_SEC_CH_UA_PLATFORM_ANDROID = (
    ("0", '"Android"'),
)


BRAVE_SEC_CH_UA_PLATFORM_MAC = (
    ("0", '"macOS"'),
)


BRAVE_SEC_CH_UA_PLATFORM = {
    "android": BRAVE_SEC_CH_UA_PLATFORM_ANDROID,
    "linux": BRAVE_SEC_CH_UA_PLATFORM_LINUX,
    "mac": BRAVE_SEC_CH_UA_PLATFORM_MAC,
    "ubuntu": BRAVE_SEC_CH_UA_PLATFORM_LINUX,
    "windows": BRAVE_SEC_CH_UA_PLATFORM_WINDOWS,
}
# fmt: on
