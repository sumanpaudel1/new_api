"""
Run script — Starts both FastAPI backend and Streamlit frontend.
Usage: python run.py
"""

import subprocess
import sys
import time
import os


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 60)
    print("  SportMonks News API Explorer")
    print("  Starting FastAPI backend + Streamlit frontend...")
    print("=" * 60)

    # Start FastAPI backend
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    print("\n✅ FastAPI backend starting on http://127.0.0.1:8000")
    print("   API Docs → http://127.0.0.1:8000/docs")
    time.sleep(2)

    # Start Streamlit frontend
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    print("✅ Streamlit frontend starting on http://localhost:8501\n")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Done.")


if __name__ == "__main__":
    main()
