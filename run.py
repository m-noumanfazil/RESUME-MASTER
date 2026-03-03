import subprocess
import os
import signal
import sys

BACKEND_DIR = "backend"
FRONTEND_DIR = "frontend"

UVICORN_PATH = os.path.join("venv", "bin", "uvicorn")

processes = []

def start():
    print("[+] Starting Backend...")
    backend = subprocess.Popen(
        [UVICORN_PATH, "backend_api:app", "--reload"],
        cwd=BACKEND_DIR
    )
    processes.append(backend)

    print("[+] Starting Frontend...")
    frontend = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR
    )
    processes.append(frontend)


def shutdown(signum, frame):
    print("\n[!] Terminating all services...")
    for p in processes:
        if p.poll() is None:
            p.terminate()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGTSTP, shutdown)  # Handles Ctrl+Z


    start()

    for p in processes:
        p.wait()