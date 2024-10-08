import os
import platform
import stat
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent

# Get OS and Architecture
system = platform.system().lower()
machine = platform.machine().lower()

# Base URL
base_url = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-{system}"

if machine in ["amd64", "x86_64"]:
    tailwindcss_url = f"{base_url}-x64"
elif "arm" in machine or "aarch" in machine:
    tailwindcss_url = f"{base_url}-arm64"
else:
    raise Exception(f"Unsupported architecture: {machine}")

if system == "windows":
    tailwindcss_url += ".exe"

# Output directory
output_dir = BASE_DIR / "bin"

# Create bin directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the filename based on the OS
filename = "tailwindcss"

if system == "windows":
    filename = "tailwindcss.exe"

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
