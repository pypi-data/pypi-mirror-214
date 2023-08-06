import pathlib

from vomit import walker


def test_walker_is_ok(tmpdir):
    pathlib.Path(tmpdir, "vomit").mkdir()
    pathlib.Path(tmpdir, "vomit", "sub").mkdir()

    expected = {
        pathlib.Path(tmpdir, "vomit", "__init__.py"),
        pathlib.Path(tmpdir, "vomit", "__main__.py")
    }

    skip = {
        pathlib.Path(tmpdir, "vomit", "__main__.txt"),
        pathlib.Path(tmpdir, "vomit", "sub", "__main__.pyc")
    }

    all = expected | skip

    for f in all:
        f.touch()

    obtained = {pathlib.Path(f) for f in walker(tmpdir)}

    assert expected == obtained
