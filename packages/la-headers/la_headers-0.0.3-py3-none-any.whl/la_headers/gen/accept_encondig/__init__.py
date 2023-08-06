# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Encoding
# https://www.iana.org/assignments/http-parameters/http-parameters.xml#http-parameters-1


from la_headers.gen.accept_encondig.brave import BRAVE_ACCEPT_ENCODING
from la_headers.gen.accept_encondig.chrome import CHROME_ACCEPT_ENCODING
from la_headers.gen.accept_encondig.firefox import FIREFOX_ACCEPT_ENCODING
from la_headers.utility import find_best_option

_accept_encoding = {
    "brave": BRAVE_ACCEPT_ENCODING,
    "chrome": CHROME_ACCEPT_ENCODING,
    "firefox": FIREFOX_ACCEPT_ENCODING,
}


def generate_accept_encoding(browser: str, version: str) -> str:
    options = _accept_encoding[browser]
    best_option = find_best_option(version, options) or "*/*"

    return best_option
