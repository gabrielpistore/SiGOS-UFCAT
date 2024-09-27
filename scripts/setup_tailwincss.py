import os
import platform
import stat
import sys
from pathlib import Path

import django
import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Add project dir to the Python path
sys.path.append(str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django
django.setup()

# Import BASE_DIR from settings
from config.settings import BASE_DIR

# Get OS and Architecture
system = platform.system().lower()
machine = platform.machine().lower()

# Base URL for TailwindCSS CLI download
base_url = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-{system}"

# Adjust URL based on the architecture
if machine in ["amd64", "x86_64"]:
    tailwindcss_url = f"{base_url}-x64"
elif "arm" in machine or "aarch" in machine:
    tailwindcss_url = f"{base_url}-arm64"
else:
    raise Exception(f"Unsupported architecture: {machine}")

# Adjust for Windows executable
if system == "windows":
    tailwindcss_url += ".exe"

# Output directory
output_dir = "./bin"

# Create bin directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the filename based on the OS
filename = "tailwindcss" if system != "windows" else "tailwindcss.exe"
output_file = BASE_DIR / output_dir / filename

# Download the TailwindCSS CLI standalone binary
print(f"Downloading TailwindCSS CLI from {tailwindcss_url}...")
response = requests.get(tailwindcss_url)

if response.status_code == 200:
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"Downloaded TailwindCSS CLI to {output_file}")
else:
    raise Exception(
        f"Failed to download TailwindCSS CLI. Status code: {response.status_code}"
    )

# Make the downloaded file executable (not needed on Windows)
if system != "windows":
    st = os.stat(output_file)
    os.chmod(output_file, st.st_mode | stat.S_IEXEC)

print("TailwindCSS CLI is ready to use!")
