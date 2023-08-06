# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent


from la_headers.gen.user_agent.brave import BRAVE_USER_AGENT
from la_headers.gen.user_agent.chrome import CHROME_USER_AGENT
from la_headers.gen.user_agent.firefox import FIREFOX_USER_AGENT
from la_headers.gen.user_agent.safari import SAFARI_USER_AGENT
from la_headers.utility import find_best_option

_user_agent = {
    "brave": BRAVE_USER_AGENT,
    "chrome": CHROME_USER_AGENT,
    "firefox": FIREFOX_USER_AGENT,
    "safari": SAFARI_USER_AGENT,
}


def generate_user_agent(browser: str, version: str, system: str, device: str) -> str:
    options = _user_agent[browser][device]
    best_option = find_best_option(version, options).format(
        version=version, system=system
    )

    return best_option
