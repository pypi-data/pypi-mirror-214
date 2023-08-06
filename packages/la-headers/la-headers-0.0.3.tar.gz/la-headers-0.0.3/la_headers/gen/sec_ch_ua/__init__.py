from packaging.version import Version

from la_headers.gen.sec_ch_ua.brave import BRAVE_SEC_CH_UA
from la_headers.gen.sec_ch_ua.chromie import CHROME_SEC_CH_UA
from la_headers.gen.sec_ch_ua.firefox import FIREFOX_SEC_CH_UA
from la_headers.utility import find_best_option

_sec_ch_ua = {
    "brave": BRAVE_SEC_CH_UA,
    "chrome": CHROME_SEC_CH_UA,
    "firefox": FIREFOX_SEC_CH_UA,
}


def generate_sec_ch_ua(browser: str, version: str, os: str) -> str:
    options = _sec_ch_ua[browser][os]
    best_option = find_best_option(version, options)

    if best_option:
        major = Version(version).major
        best_option = best_option.format(major=major)

    return best_option
