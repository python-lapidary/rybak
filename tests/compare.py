from pathlib import Path


def cmp_dirs(expected: Path, actual: Path) -> None:
    expected_children = {path.name for path in expected.iterdir()}
    actual_children = {path.name for path in actual.iterdir()}

    assert actual_children == expected_children, \
        ', '.join(str(p) for p in expected_children.symmetric_difference(actual_children))

    for name in expected_children:
        expected_path = (expected / name)
        actual_path = (actual / name)
        if expected_path.is_dir():
            assert actual_path.is_dir(), f'Expected {actual_path} to be a directory'

            cmp_dirs(expected_path, actual_path)
        elif expected_path.is_file():
            assert actual_path.is_file(), actual_path

            expected_text = expected_path.read_text()
            actual_text = actual_path.read_text()

            assert expected_text == actual_text, f'"{expected_text}" != "{actual_text}"'
        else:
            raise TypeError('Neither a file nor a directory', expected_path)
