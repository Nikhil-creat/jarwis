"""Run generated code in a throwaway, locked-down Docker container."""
import subprocess, tempfile, pathlib
def run_python(code: str, timeout: int = 20) -> dict:
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, "main.py").write_text(code)
        cmd = ["docker", "run", "--rm", "--network", "none", "--memory", "256m", "--cpus", "0.5", "--pids-limit", "64",
               "--read-only", "--cap-drop", "ALL", "-v", f"{d}:/work:ro", "-w", "/work", "python:3.12-slim", "python", "main.py"]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {"ok": p.returncode == 0, "out": p.stdout[-4000:], "err": p.stderr[-4000:]}
        except subprocess.TimeoutExpired:
            return {"ok": False, "out": "", "err": "timeout"}
