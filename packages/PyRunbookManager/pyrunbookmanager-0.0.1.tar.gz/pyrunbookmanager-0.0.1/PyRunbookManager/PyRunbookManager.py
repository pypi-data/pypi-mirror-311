import sys
import subprocess

class modulemamanger:
    def install(module_name):
        try:
            print(f"[PyRunbookManager] Attempting to install {module_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {module_name}: {e}")
            sys.exit(1)