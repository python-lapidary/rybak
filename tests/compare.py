from pathlib import Path


def cmp_dirs(expected: Path, actual: Path) -> None:
    expected_children = set(expected.iterdir())
    actual_children = set(expected.iterdir())

    assert actual_children == expected_children

    for name in expected_children:
        if (expected / name).is_dir():
            assert (actual / name).is_dir()

            cmp_dirs(expected / name, actual / name)
        elif (expected / name).is_file():
            assert (actual / name).is_file()

            expected_text = (expected / name).read_text()
            actual_text = (actual / name).read_text()

            assert expected_text == actual_text
