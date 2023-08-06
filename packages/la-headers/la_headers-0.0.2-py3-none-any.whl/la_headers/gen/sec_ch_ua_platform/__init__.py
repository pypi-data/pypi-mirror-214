from la_headers.gen.sec_ch_ua_platform.brave import BRAVE_SEC_CH_UA_PLATFORM
from la_headers.gen.sec_ch_ua_platform.chromie import CHROME_SEC_CH_UA_PLATFORM
from la_headers.gen.sec_ch_ua_platform.firefox import FIREFOX_SEC_CH_UA_PLATFORM
from la_headers.utility import find_best_option

_sec_ch_ua_platform = {
    "brave": BRAVE_SEC_CH_UA_PLATFORM,
    "chrome": CHROME_SEC_CH_UA_PLATFORM,
    "firefox": FIREFOX_SEC_CH_UA_PLATFORM,
}


def generate_sec_ch_ua_platform(browser: str, version: str, os: str) -> str:
    options = _sec_ch_ua_platform[browser][os]
    best_option = find_best_option(version, options)

    return best_option
