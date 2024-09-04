import subprocess
import threading


def run_server():
    print("Starting Django development server...")
    global server_process
    server_process = subprocess.Popen("python manage.py runserver", shell=True)


def run_tailwind():
    print("Starting Tailwind CSS watcher...")
    global tailwind_process
    tailwind_process = subprocess.Popen(
        "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch",
        shell=True,
        stdout=subprocess.DEVNULL,  # Redirect standard output to DEVNULL
        stderr=subprocess.DEVNULL,  # Redirect standard error to DEVNULL
    )


def stop_processes():
    print("\nStopping processes...")
    if server_process:
        server_process.terminate()
        server_process.wait()
    if tailwind_process:
        tailwind_process.terminate()
        tailwind_process.wait()
    print("Processes stopped.")


try:
    threading.Thread(target=run_server).start()
    threading.Thread(target=run_tailwind).start()

    while True:
        pass  # Keep the main thread alive
except KeyboardInterrupt:
    stop_processes()
