# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Upgrade-Insecure-Requests

from la_headers.gen.upgrade_insecure_requests.brave import (
    BRAVE_UPGRADE_INSECURE_REQUESTS,
)
from la_headers.gen.upgrade_insecure_requests.chrome import (
    CHROME_UPGRADE_INSECURE_REQUESTS,
)
from la_headers.gen.upgrade_insecure_requests.firefox import (
    FIREFOX_UPGRADE_INSECURE_REQUESTS,
)
from la_headers.gen.upgrade_insecure_requests.safari import (
    SAFARI_UPGRADE_INSECURE_REQUESTS,
)
from la_headers.utility import find_best_option

_upgrade_insecure_requests = {
    "brave": BRAVE_UPGRADE_INSECURE_REQUESTS,
    "chrome": CHROME_UPGRADE_INSECURE_REQUESTS,
    "firefox": FIREFOX_UPGRADE_INSECURE_REQUESTS,
    "safari": SAFARI_UPGRADE_INSECURE_REQUESTS,
}


def generate_upgrade_insecure_requests(browser: str, version: str) -> str:
    options = _upgrade_insecure_requests[browser]
    best_option = find_best_option(version, options)

    return best_option
