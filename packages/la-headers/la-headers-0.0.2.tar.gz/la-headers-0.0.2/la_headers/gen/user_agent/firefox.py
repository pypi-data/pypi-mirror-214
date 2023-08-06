# fmt: off
FIREFOX_DESKTOP_USER_AGENT = (
    ("114.0", "Mozilla/5.0 ({system}; rv:109.0) Gecko/20100101 Firefox/{version}"),
    ("109.0", "Mozilla/5.0 ({system}; rv:109.0) Gecko/20100101 Firefox/{version}"),
    ("0", "Mozilla/5.0 ({system}; rv:{version}) Gecko/20100101 Firefox/{version}"),
)


FIREFOX_MOBILE_USER_AGENT = (
    ("0", "Mozilla/5.0 ({system}; rv:{version}) Gecko/{version} Firefox/{version}"),
)


FIREFOX_USER_AGENT = {
    "desktop": FIREFOX_DESKTOP_USER_AGENT,
    "mobile": FIREFOX_MOBILE_USER_AGENT,
}
# fmt: on
