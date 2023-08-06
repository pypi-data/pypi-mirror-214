# fmt: off
CHROME_ANDROID_SEC_CH_UA = (
    ("0", '"Not.A/Brand";v="8", "Chromium";v="{major}", "Google Chrome";v="{major}"'),
)

CHROME_LINUX_SEC_CH_UA = (
    ("114", '"Not.A/Brand";v="8", "Chromium";v="{major}", "Google Chrome";v="{major}"'),
    ("105", '"Google Chrome";v="{major}", "Not)A;Brand";v="8", "Chromium";v="{major}"'),
    ("99", '" Not;A Brand";v="99", "Chromium";v="{major}", "Google Chrome";v="{major}"'),
    ("0", '" Not;A Brand";v="99", "Google Chrome";v="{major}", "Chromium";v="{major}"'),
)

CHROME_WINDOWS_SEC_CH_UA = (
    ("114", None),
    ("105", '"Google Chrome";v="{major}", "Not)A;Brand";v="8", "Chromium";v="{major}"'),
    ("99", '" Not;A Brand";v="99", "Chromium";v="{major}", "Google Chrome";v="{major}"'),
    ("0", '" Not;A Brand";v="99", "Google Chrome";v="{major}", "Chromium";v="{major}"'),
)

CHROME_MACOS_SEC_CH_UA = (
    ("0", None)
)

CHROME_SEC_CH_UA = {
    "android": CHROME_ANDROID_SEC_CH_UA,
    "linux": CHROME_LINUX_SEC_CH_UA,
    "macOS": CHROME_MACOS_SEC_CH_UA,
    "windows": CHROME_WINDOWS_SEC_CH_UA,
}
# fmt: on
