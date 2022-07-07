"""Helper methods for testing."""
import json
from pathlib import Path
from typing import Any, Union


def load_json_fixture(fp: Union[str, Path]) -> Any:
    """Load a JSON fixture from the given file path.

    Args:
        fp: The file path of the fixture. If not absolute, it is relative
            to the tests/fixtures directory.

    Returns:
        The JSON fixture.
    """
    if not Path(fp).is_absolute():
        fp = Path(__file__).parent / 'fixtures' / fp

    with open(fp) as f:
        return json.load(f)
