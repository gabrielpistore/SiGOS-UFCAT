import os
import platform
import stat
from pathlib import Path

import colorama
import requests

# Initialize colorama
colorama.init(autoreset=True)

VERSION = "3.4.17"

# Base URL and paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Get OS and Architecture
SYSTEM = platform.system().lower()
MACHINE = platform.machine().lower()

# Base URL for TailwindCSS binary
BASE_URL = f"https://github.com/tailwindlabs/tailwindcss/releases/download/v{VERSION}/tailwindcss-{SYSTEM}"

# Determine the appropriate download URL based on the architecture
if MACHINE in ["amd64", "x86_64"]:
    tailwindcss_url = f"{BASE_URL}-x64"
elif "arm" in MACHINE or "aarch" in MACHINE:
    tailwindcss_url = f"{BASE_URL}-arm64"
else:
    raise Exception(
        f"{colorama.Fore.RED}Unsupported architecture: {MACHINE}{colorama.Style.RESET_ALL}"
    )

# Output directory
output_dir = BASE_DIR / "bin"

# Create bin directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the filename based on the OS
filename = "tailwindcss"

output_file = BASE_DIR / output_dir / filename

# Download the TailwindCSS CLI standalone binary
print(f"{colorama.Fore.GREEN}Downloading TailwindCSS CLI from {tailwindcss_url}...")
response = requests.get(tailwindcss_url)

if response.status_code == 200:
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(
        f"{colorama.Fore.GREEN}Downloaded TailwindCSS CLI to {output_file}{colorama.Style.RESET_ALL}"
    )
else:
    raise Exception(
        f"{colorama.Fore.RED}Failed to download TailwindCSS CLI. Status code: {response.status_code}{colorama.Style.RESET_ALL}"
    )

# Make the downloaded file executable (not needed on Windows)
if SYSTEM != "windows":
    st = os.stat(output_file)
    os.chmod(output_file, st.st_mode | stat.S_IEXEC)

print(
    f"{colorama.Fore.GREEN}TailwindCSS CLI is ready to use!{colorama.Style.RESET_ALL}"
)
