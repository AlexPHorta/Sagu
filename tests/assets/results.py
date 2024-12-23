import datetime

test_paths = {
    "about": {"applications": {}, "quotes": {}, "getting_started": {}},
    "downloads": {"all_releases": {}, "source_code": {}, "windows": {}, "mac_os": {}, "other_platforms": {}},
    "documentation": {"beginners_guide": {}, "developers_guide": {}, "faq": {}},
    "community": {"mailing_lists": {}, "forums": {}, "conferences": {}},
    "news": {},
}

test_flat_paths = {
    "about": {},
    "about:applications": {},
    "about:quotes": {},
    "about:getting_started": {},
    "downloads": {},
    "downloads:all_releases": {},
    "downloads:all_releases:yearly": {},
    "downloads:source_code": {},
    "downloads:windows": {},
    "downloads:mac_os": {},
    "downloads:other_platforms": {},
    "documentation": {},
    "documentation:beginners_guide": {},
    "documentation:developers_guide": {},
    "documentation:faq": {},
    "community": {},
    "community:mailing_lists": {},
    "community:forums": {},
    "community:conferences": {},
    "news": {},
}


test_basic_paths = ["about:applications", "about:getting_started"]
