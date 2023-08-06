# fmt: off
FIREFOX_DEFAULT_ACCEPT = (
    ("92.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"),
    ("72.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
    ("66.0", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
    ("65.0", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
    ("0.0", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
)

FIREFOX_IMAGE_ACCEPT = (
    ("92.0", "image/avif,image/webp,*/*"),
    ("65.0", "image/webp,*/*"),
    ("47.0", "*/*"),
    ("0.0", "image/png,image/*;q=0.8,*/*;q=0.5"),
)

FIREFOX_VIDEO_ACCEPT = (
    ("3.6", "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5"),
)

FIREFOX_AUDIO_ACCEPT = (
    ("3.6", "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5"),
)

FIREFOX_SCRIPT_ACCEPT = (
    ("0.0", "*/*"),
)

FIREFOX_CSS_ACCEPT = (
    ("4.0", "text/css,*/*;q=0.1"),
)

FIREFOX_ACCEPT = {
    "default": FIREFOX_DEFAULT_ACCEPT,
    "image": FIREFOX_IMAGE_ACCEPT,
    "video": FIREFOX_VIDEO_ACCEPT,
    "audio": FIREFOX_DEFAULT_ACCEPT,
    "script": FIREFOX_SCRIPT_ACCEPT,
    "css": FIREFOX_CSS_ACCEPT,
}
# fmt: on
