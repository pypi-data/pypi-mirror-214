# fmt: off
CHROME_DEFAULT_ACCEPT = (
    ("114.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"),
    ("97.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"),
    ("0.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"),
)

CHROME_IMAGE_ACCEPT = (
    ("97.0", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"),
    ("0.0", "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"),
)

CHROME_VIDEO_ACCEPT = (
    ("0.0", "*/*"),
)

CHROME_AUDIO_ACCEPT = (
    ("0.0", "*/*"),
)

CHROME_SCRIPT_ACCEPT = (
    ("0.0", "*/*"),
)

CHROME_CSS_ACCEPT = (
    ("0.0", "text/css,*/*;q=0.1"),
)

CHROME_ACCEPT = {
    "default": CHROME_DEFAULT_ACCEPT,
    "image": CHROME_IMAGE_ACCEPT,
    "video": CHROME_VIDEO_ACCEPT,
    "audio": CHROME_AUDIO_ACCEPT,
    "script": CHROME_SCRIPT_ACCEPT,
    "css": CHROME_CSS_ACCEPT,
}
# fmt: on
