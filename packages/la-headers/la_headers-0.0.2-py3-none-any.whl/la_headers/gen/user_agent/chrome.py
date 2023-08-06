# fmt: off
CHROME_DESKTOP_USER_AGENT = (
    ("0", "Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"),
)


CHROME_MOBILE_USER_AGENT = (
    ("0", "Mozilla/5.0 ({system}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Mobile Safari/537.36"),
)


CHROME_USER_AGENT = {
    "desktop": CHROME_DESKTOP_USER_AGENT,
    "mobile": CHROME_MOBILE_USER_AGENT,
}
# fmt: on
