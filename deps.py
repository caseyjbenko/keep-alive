import subprocess
import sys

def check_and_install(package):
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    # List of required packages
    required_packages = ["wakeonlan"]

    for package in required_packages:
        check_and_install(package)

    print("All dependencies are installed.")

if __name__ == "__main__":
    main()

