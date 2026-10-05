import subprocess
import sys


def main():
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "Home.py"],
        check=False,
    )


if __name__ == "__main__":
    main()