import subprocess
import threading


def run_server():
    print("Starting Django development server...\n")
    subprocess.run("python manage.py runserver", shell=True)


def run_tailwind():
    print("Starting Tailwind CSS watcher...\n")
    subprocess.run(
        "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch",
        shell=True,
    )


threading.Thread(target=run_server).start()
threading.Thread(target=run_tailwind).start()
