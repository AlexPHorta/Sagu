import pytest

from src.sagu import builder, library, post

from .utils_for_testing import asset


class TestBuilder:

    @pytest.fixture
    def mock_settings(self):
        settings = {"SITENAME": "Default Project",
                    "SITEAUTHOR": "TestAuthor",
                    "SITELANGUAGE": "en",
                    "SITEURL": "www.test.com",
                    "SITETIMEZONE": "Europe/Rome",
                    "THEME": "sagu",
                    "BASETEMPLATE": "index.jinja",
                    "THEME_STATIC": "static",
                    "MENUITEMS": [
                        { "href": "animals/dogs/the-noble-akita.html",
                          "title": "Akita" },
                        { "href": "animals/cats/kurilian-bobtail-has-a-bobbed-tail.html",
                          "title": "Kurilian Bobtail" },
                        { "href": "animals/cats/donskoy.html",
                          "title": "Donskoy" },
                        { "href": "animals/dogs/the-colossal-mastiff.html",
                          "title": "Mastiff" }]
                    }
        return settings

    @pytest.fixture
    def basic_mock_settings(self, mock_settings):
        mock_settings["BASETEMPLATE"] = "basic.jinja"
        return mock_settings

    @pytest.fixture
    def full_mock_settings(self, mock_settings):
        mock_settings["SITENAME"] = "Cats and Dogs"
        mock_settings["BASETEMPLATE"] = "full.jinja"
        return mock_settings


    def test_builder(self, capsys, basic_mock_settings):
        """The builder will manage the mixing of posts and templates."""
        _builder = builder.Builder(asset("TestBuilder/"), basic_mock_settings)
        template = _builder.template
        assert template.render(name="Test") == "Hello, Test!\n"

    def test_builder_autoescape_on(self, mock_settings):
        """The builder will have autoescape turned on by default."""
        _builder = builder.Builder(asset("TestBuilder/"), mock_settings)
        assert _builder.env.autoescape is True

    def test_builder_build_post(self, mock_settings):
        _library = library.Library(asset("basic_paths.toml"))
        _post = post.Post(asset("TestBuilder/index.toml"), website_path=_library.flat_tree)
        _library.add_post(_post)
        _builder = builder.Builder(asset("TestBuilder/"), mock_settings)
        template = _builder.template
        with open(asset("TestBuilder/index.html")) as f:
            test_builder_post = _library.get_post_by_id(_post.id)
            assert template.render(test_builder_post.get_contents()) == f.read()
    
    def test_builder_build_post_complete(self, full_mock_settings):
        _library = library.Library(asset("TestBuilder/full/paths.toml"))
        _post = post.Post(asset("TestBuilder/full/full.toml"), website_path=_library.flat_tree)
        _library.add_post(_post)
        _builder = builder.Builder(asset("TestBuilder/full/"), full_mock_settings)
        template = _builder.template
        with open(asset("TestBuilder/full/full.html")) as f:
            test_builder_post = _library.get_post_by_id(_post.id)
            assert template.render(test_builder_post.get_contents()) == f.read()
