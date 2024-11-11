import subprocess
import threading
from pathlib import Path

import colorama

colorama.init()

BASE_DIR = Path(__file__).parent


def run_django_server():
    print(f"{colorama.Fore.GREEN}[django]{colorama.Style.RESET_ALL} Starting ...")
    global django_server_process
    django_server_process = subprocess.Popen("python manage.py runserver", shell=True)


def run_tailwind_watch():
    print(
        f"{colorama.Fore.CYAN}[tailwindcss]{colorama.Style.RESET_ALL} Starting ... \n"
    )
    global tailwind_process
    tailwindcli = BASE_DIR / "bin" / "tailwindcss"
    command = (
        f"{tailwindcli} -i ./static/css/base.css -o ./static/css/styles.css --watch"
    )
    tailwind_process = subprocess.Popen(command, shell=True)


def stop_processes():
    print(f"{colorama.Fore.RED}\nStopping processes...")

    if django_server_process:
        django_server_process.terminate()
        django_server_process.wait()
    if tailwind_process:
        tailwind_process.terminate()
        tailwind_process.wait()

    print(f"Processes stopped.{colorama.Style.RESET_ALL}")


try:
    threading.Thread(target=run_django_server).start()
    threading.Thread(target=run_tailwind_watch).start()
    while True:
        pass
except KeyboardInterrupt:
    stop_processes()
