import os
import platform
import stat

import requests

# Get OS and Architecture
SYSTEM = platform.system().lower()
ARCHITECTURE = platform.machine().lower()

# Base URL for TailwindCSS CLI download
BASE_URL = f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-{SYSTEM}"

# Adjust URL based on the architecture
if ARCHITECTURE in ["amd64", "x86_64"]:
    tailwindcss_url = f"{BASE_URL}-x64"
elif "arm" in ARCHITECTURE or "aarch" in ARCHITECTURE:
    tailwindcss_url = f"{BASE_URL}-arm64"
else:
    raise Exception(f"Unsupported architecture: {ARCHITECTURE}")

# Adjust for Windows executable
if SYSTEM == "windows":
    tailwindcss_url += ".exe"

# Output directory
OUTPUT_DIR = "./bin"

# Create bin directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Set the filename based on the OS
FILENAME = "tailwindcss" if SYSTEM != "windows" else "tailwindcss.exe"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, FILENAME)

# Download the TailwindCSS CLI standalone binary
print(f"Downloading TailwindCSS CLI from {tailwindcss_url}...")
response = requests.get(tailwindcss_url)

if response.status_code == 200:
    with open(OUTPUT_FILE, "wb") as file:
        file.write(response.content)
    print(f"Downloaded TailwindCSS CLI to {OUTPUT_FILE}")
else:
    raise Exception(
        f"Failed to download TailwindCSS CLI. Status code: {response.status_code}"
    )

# Make the downloaded file executable (not needed on Windows)
if SYSTEM != "windows":
    st = os.stat(OUTPUT_FILE)
    os.chmod(OUTPUT_FILE, st.st_mode | stat.S_IEXEC)

print("TailwindCSS CLI is ready to use!")
