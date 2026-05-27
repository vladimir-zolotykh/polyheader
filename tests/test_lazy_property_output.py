# tests/test_lazy_property_output.py
import subprocess
import sys
from pathlib import Path


def test_script_output():
    script = Path(__file__).parent.parent / "lazyproperty.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=True,
    )

    expected = """calculating area
467.59465056030473
calculating circumference
76.65486074759094
returning var_area
467.59465056030473
returning var_circumference
76.65486074759094
returning var_area
467.59465056030473
returning var_circumference
76.65486074759094
returning var_area
467.59465056030473
returning var_circumference
76.65486074759094
returning var_area
467.59465056030473
returning var_circumference
76.65486074759094
"""

    assert result.stdout == expected
