"""One-command dashboard launcher for JobHunterX."""
from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DASHBOARD = ROOT / "jobbot" / "ui" / "dashboard.py"


def local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "your-mac-ip"


if __name__ == "__main__":
    print("\nJobHunterX is starting...")
    print("Mac:   http://localhost:8501")
    print(f"Phone: http://{local_ip()}:8501  (same Wi-Fi)\n")
    raise SystemExit(subprocess.call([
        sys.executable, "-m", "streamlit", "run", str(DASHBOARD),
        "--server.address", "0.0.0.0", "--server.port", "8501"
    ]))
