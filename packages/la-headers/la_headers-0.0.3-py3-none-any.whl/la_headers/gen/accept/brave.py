# fmt: off
BRAVE_DEFAULT_ACCEPT = (
    ("0.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"),
)

BRAVE_IMAGE_ACCEPT = (
    ("0.0", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"),
)

BRAVE_VIDEO_ACCEPT = (
    ("0.0", "*/*"),
)

BRAVE_AUDIO_ACCEPT = (
    ("0.0", "*/*"),
)

BRAVE_SCRIPT_ACCEPT = (
    ("0.0", "*/*"),
)

BRAVE_CSS_ACCEPT = (
    ("0.0", "text/css,*/*;q=0.1"),
)

BRAVE_ACCEPT = {
    "default": BRAVE_DEFAULT_ACCEPT,
    "image": BRAVE_IMAGE_ACCEPT,
    "video": BRAVE_VIDEO_ACCEPT,
    "audio": BRAVE_AUDIO_ACCEPT,
    "script": BRAVE_SCRIPT_ACCEPT,
    "css": BRAVE_CSS_ACCEPT,
}
# fmt: on
