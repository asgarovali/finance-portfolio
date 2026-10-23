"""Run the whole project end to end:  python -m src.run

Later steps get added here as they're built.
"""
from src.analysis import history, reconcile
from src.data import clean_statements, download_market, download_policy, download_sec, extract_cap
from src.model import build_excel


def main() -> None:
    download_sec.main()
    download_policy.main()
    download_market.main()
    clean_statements.main()
    extract_cap.main()
    reconcile.main()
    history.main()
    build_excel.main()  # needs Excel installed for the recalculation


if __name__ == "__main__":
    main()
