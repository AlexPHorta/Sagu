import datetime

basic = {
    "meta": {"title": "Document title", "creation_date": datetime.datetime(2024, 9, 22, 10, 27)},  # noqa: DTZ001
    "content": {"markdown": "Example text.\n"},
}


test_paths = {
    "about": {"applications": {}, "quotes": {}, "getting_started": {}},
    "downloads": {"all_releases": {}, "source_code": {}, "windows": {}, "mac_os": {}, "other_platforms": {}},
    "documentation": {"beginners_guide": {}, "developers_guide": {}, "faq": {}},
    "community": {"mailing_lists": {}, "forums": {}, "conferences": {}},
    "news": {},
}

test_flat_paths = {
    "about:applications": {},
    "about:quotes": {},
    "about:getting_started": {},
    "downloads:all_releases": {},
    "downloads:source_code": {},
    "downloads:windows": {},
    "downloads:mac_os": {},
    "downloads:other_platforms": {},
    "documentation:beginners_guide": {},
    "documentation:developers_guide": {},
    "documentation:faq": {},
    "community:mailing_lists": {},
    "community:forums": {},
    "community:conferences": {},
    "news": {},
}


test_basic_paths = ["about:applications", "about:getting_started"]

content_markdown = (
    "<p>Markdown is a <strong>lightweight markup language</strong> "
    "used to format plain text. It's simple to use and can be "
    "converted to HTML or other formats. Below are some key "
    "features of markdown:</p>\n<h3>1. Headers</h3>\n<p>You can "
    "create headers by using the <code>#</code> symbol:\n- "
    "<code>#</code> for a main header (H1)\n- <code>##</code> for "
    "a subheader (H2)\n- <code>###</code> for a smaller header "
    "(H3), and so on.</p>\n<p>Example:\n```markdown</p>\n<h1>This "
    "is an H1</h1>\n<h2>This is an H2</h2>"
)
