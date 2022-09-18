from pathlib import Path

def test_copy_res_file() -> None:
    from oooscript.build.copy_resource import CopyResource
    from oooscript.build.tmp_dir import tmpdir
    from oooscript.res.docs import __res_path_docs__
    file = Path(__res_path_docs__, "blank.odt")
    with tmpdir() as tmp:
        dest = Path(tmp, "blank.odt")
        cp = CopyResource(src=file, dst=dest, dst_is_file=True, src_is_res=True)
        cp.copy()
        assert dest.exists()

def test_copy_res_dir() -> None:
    from oooscript.build.copy_resource import CopyResource
    from oooscript.build.tmp_dir import tmpdir
    from oooscript.res.docs import __res_path_docs__
    file = Path(__res_path_docs__, "blank.odt")
    with tmpdir() as tmp:
        dest = Path(tmp)
        cp = CopyResource(src=file, dst=dest, dst_is_file=False, src_is_res=False)
        cp.copy()
        assert dest.exists()

def test_copy_res_file() -> None:
    from oooscript.build.copy_resource import CopyResource
    from oooscript.build.tmp_dir import tmpdir
    file = Path("docs", "blank.odt")
    with tmpdir() as tmp:
        dest = Path(tmp)
        cp = CopyResource(src=file, dst=dest, dst_is_file=False, src_is_res=True)
        cp.copy()
        assert dest.exists()