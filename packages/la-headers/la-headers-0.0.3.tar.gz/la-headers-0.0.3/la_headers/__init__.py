from random import choice

from la_headers.gen.accept import generate_accept
from la_headers.gen.accept_encondig import generate_accept_encoding
from la_headers.gen.sec_ch_ua import generate_sec_ch_ua
from la_headers.gen.sec_ch_ua_mobile import generate_sec_ch_ua_mobile
from la_headers.gen.sec_ch_ua_platform import generate_sec_ch_ua_platform
from la_headers.gen.system import generate_system
from la_headers.gen.upgrade_insecure_requests import generate_upgrade_insecure_requests
from la_headers.gen.user_agent import generate_user_agent
from la_headers.prefabs import get_prefabs


def generate_headers(
    os: str,
    os_version: str,
    browser: str,
    version: str,
    device: str = "desktop",
    context: str = "default",
) -> dict:
    """
    Generate a specific headers.

    os:
        android
        linux
        mac
        ubuntu
        windows

    os_version:
        major.minor.patch

    browser options:
        chrome
        firefox

    version:
        major.minor.patch

    device:
        desktop
        mobile

    context:
        default
        image
        video
        audio
        script
        css
    """

    system = generate_system(os, os_version, browser)

    headers = {
        "Accept": generate_accept(browser, version, context),
        "Accept-Encoding": generate_accept_encoding(browser, version),
        "Accept-Language": None,
        "Connection": None,
        "Sec-Ch-Ua": generate_sec_ch_ua(browser, version, os),
        "Sec-Ch-Ua-Mobile": generate_sec_ch_ua_mobile(browser, version, device),
        "Sec-Ch-Ua-Platform": generate_sec_ch_ua_platform(browser, version, os),
        "Upgrade-Insecure-Requests": generate_upgrade_insecure_requests(
            browser, version
        ),
        "User-Agent": generate_user_agent(browser, version, system, device),
    }

    # Remove fields with None
    return {k: v for k, v in headers.items() if v is not None}


def generate_random_headers(
    os: list[str] = [],
    os_version: list[str] = [],
    browser: list[str] = [],
    version: list[str] = [],
    device: list[str] = [],
    context: list[str] = [],
) -> dict:
    """
    Generate a random headers.
    All paramaters are a list of possibilities but
    empty list means that you accept any possibility in the field.

    os:
        windows
        linux
        android
        mac

    os_version:
        major.minor.patch

    browser options:
        chrome
        firefox

    version:
        major.minor.patch

    device:
        desktop
        mobile

    context:
        default
        image
        video
        audio
        script
        css
    """

    prefabs = get_prefabs(
        os=os,
        os_version=os_version,
        browser=browser,
        version=version,
        device=device,
        context=context,
    )

    prefab = choice(prefabs)

    for k in prefab:
        prefab[k] = choice(prefab[k])

    return generate_headers(**prefab)
