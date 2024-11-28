import filecmp
import io
import pathlib
import shutil
import tempfile
from contextlib import contextmanager, redirect_stdout


def asset(asset_name):
    assets = pathlib.Path(pathlib.Path(__file__).parent, "assets")
    return pathlib.Path(assets, asset_name).resolve(strict=True)


# Stolen from https://getpelican.com
@contextmanager
def temporary_folder():
    """creates a temporary folder, return it and delete it afterwards.

    This allows to do something like this in tests:

        >>> with temporary_folder() as d:
            # do whatever you want
    """
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def equal_dirs(dir1, dir2, **kwargs):  # filecmp.dircmp
    compare = filecmp.dircmp(dir1, dir2, ignore=kwargs.get("ignore"))
    with redirect_stdout(io.StringIO()) as f:
        compare.report_full_closure()
    s = f.getvalue()
    print(s)  # noqa: T201
    return not (any(("Only in" in s, "Differing" in s, "Trouble with" in s, "funny" in s)))
