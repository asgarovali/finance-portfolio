"""Run the whole project end to end:  python -m src.run

Only the download step exists so far; later steps get added here as they're built.
"""
from src.data import download_sec


def main() -> None:
    download_sec.main()


if __name__ == "__main__":
    main()
