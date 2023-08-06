# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA-Platform
# Yes, quotes are inclused in the string.

# fmt: off
CHROME_SEC_CH_UA_PLATFORM_WINDOWS = (
    ("114.0", None),
    ("0", '"Windows"'),
)


CHROME_SEC_CH_UA_PLATFORM_LINUX = (
    ("0", '"Linux"'),
)


CHROME_SEC_CH_UA_PLATFORM_ANDROID = (
    ("0", '"Android"'),
)


CHROME_SEC_CH_UA_PLATFORM_MAC = (
    ("0", '"macOS"'),
)


CHROME_SEC_CH_UA_PLATFORM = {
    "android": CHROME_SEC_CH_UA_PLATFORM_ANDROID,
    "linux": CHROME_SEC_CH_UA_PLATFORM_LINUX,
    "mac": CHROME_SEC_CH_UA_PLATFORM_MAC,
    "ubuntu": CHROME_SEC_CH_UA_PLATFORM_LINUX,
    "windows": CHROME_SEC_CH_UA_PLATFORM_WINDOWS,
}
# fmt: on
