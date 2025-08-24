
import json, os, subprocess, sys, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
main_mod = BASE / "src" / "main.py"

def test_cli_runs():
    # just ensure the CLI runs without crashing
    out = subprocess.check_output([sys.executable, str(main_mod)])
    data = json.loads(out.decode("utf-8"))
    assert "suggestions" in data
    assert any(s["for"]=="initiator" for s in data["suggestions"])
