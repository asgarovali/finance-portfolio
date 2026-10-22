"""Run the whole project end to end:  python -m src.run

Later steps get added here as they're built.
"""
from src.analysis import history, reconcile
from src.data import clean_statements, download_market, download_policy, download_sec


def main() -> None:
    download_sec.main()
    download_policy.main()
    download_market.main()
    clean_statements.main()
    reconcile.main()
    history.main()


if __name__ == "__main__":
    main()
