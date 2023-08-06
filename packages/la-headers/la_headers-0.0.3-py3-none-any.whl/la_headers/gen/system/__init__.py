from la_headers.gen.system.android import ANDROID_BROWSER_SYSTEM, ANDROID_VERSION
from la_headers.gen.system.linux import LINUX_BROWSER_SYSTEM, LINUX_VERSION
from la_headers.gen.system.mac import MAC_BROWSER_SYSTEM, MAC_VERSION
from la_headers.gen.system.ubuntu import UBUNTU_BROWSER_SYSTEM, UBUNTU_VERSION
from la_headers.gen.system.windows import WINDOWS_BROWSER_SYSTEM, WINDOWS_VERSION
from la_headers.utility import find_best_function, find_best_option

_system = {
    "android": ANDROID_BROWSER_SYSTEM,
    "linux": LINUX_BROWSER_SYSTEM,
    "mac": MAC_BROWSER_SYSTEM,
    "ubuntu": UBUNTU_BROWSER_SYSTEM,
    "windows": WINDOWS_BROWSER_SYSTEM,
}

_version = {
    "android": ANDROID_VERSION,
    "linux": LINUX_VERSION,
    "mac": MAC_VERSION,
    "ubuntu": UBUNTU_VERSION,
    "windows": WINDOWS_VERSION,
}


def generate_system(os: str, os_version: str, browser: str) -> str:
    """
    os:
        android
        linux
        mac
        ubuntu
        windows

    os_version:
        major.minor.patch
    """

    version_options = _version[os]
    version_function = find_best_function(os_version, version_options) or (lambda _: "")
    version_formated = version_function(os_version)

    system_options = _system[os][browser]
    best_option = find_best_option(os_version, system_options).format(
        os_version=version_formated
    )

    return best_option
