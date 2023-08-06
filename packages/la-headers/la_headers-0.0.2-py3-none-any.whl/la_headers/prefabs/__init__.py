from copy import deepcopy

from la_headers.options.browser.chrome import CHROME_VERSION
from la_headers.options.browser.firefox import FIREFOX_VERSION
from la_headers.options.operating_system.android import ANDROID_VERSION

_prefabs: list[dict] = [
    {
        "os": ["linux"],
        "os_version": ["23.04", "22.10", "22.04"],
        "browser": ["chrome"],
        "version": CHROME_VERSION[:10],
        "device": ["desktop"],
        "context": ["default"],
    },
    {
        "os": ["linux"],
        "os_version": ["23.04", "22.10", "22.04"],
        "browser": ["firefox"],
        "version": FIREFOX_VERSION[:10],
        "device": ["desktop"],
        "context": ["default"],
    },
    {
        "os": ["windows"],
        "os_version": ["10", "11"],
        "browser": ["chrome"],
        "version": CHROME_VERSION[:10],
        "device": ["desktop"],
        "context": ["default"],
    },
    {
        "os": ["windows"],
        "os_version": ["10", "11"],
        "browser": ["firefox"],
        "version": FIREFOX_VERSION[:10],
        "device": ["desktop"],
        "context": ["default"],
    },
    {
        "os": ["android"],
        "os_version": ANDROID_VERSION[:10],
        "browser": ["chrome"],
        "version": CHROME_VERSION[:10],
        "device": ["mobile"],
        "context": ["default"],
    },
    {
        "os": ["android"],
        "os_version": ANDROID_VERSION[:10],
        "browser": ["firefox"],
        "version": FIREFOX_VERSION[:10],
        "device": ["mobile"],
        "context": ["default"],
    },
]


def get_prefabs(**kwargs) -> dict:
    prefabs = deepcopy(_prefabs)

    for field, options in kwargs.items():
        if not options:
            continue

        for prefab in prefabs[:]:
            prefab[field] = [o for o in prefab[field] if o in options]

            if len(prefab[field]) == 0:
                prefabs.remove(prefab)

    return prefabs
