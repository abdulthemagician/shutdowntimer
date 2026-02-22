"""
main.py
-------
Entry point for Shutdown Timer.
Run this file directly:
    python main.py
"""

from app import ShutdownTimerApp


def main() -> None:
    app = ShutdownTimerApp()
    app.run()


if __name__ == "__main__":
    main()