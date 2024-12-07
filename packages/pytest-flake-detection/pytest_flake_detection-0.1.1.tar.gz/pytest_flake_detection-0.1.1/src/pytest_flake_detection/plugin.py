import pytest
from pathlib import Path
import argparse
import colorama


def pytest_addoption(parser):
    """"""
    group = parser.getgroup("flake-detection")
    group.addoption(
        "--foo",
        action="store",
        dest="dest_foo",
        default="2024",
        help='Set the value for the fixture "bar".',
    )

    parser.addini("HELLO", "Dummy pytest.ini setting")


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


class TestResultCollector:
    YLW = f"{colorama.Fore.YELLOW}"
    BRT = f"{colorama.Style.BRIGHT}"
    RESET = f"{colorama.Style.RESET_ALL}"

    def __init__(self, n_runs: int):
        self.passed: list[pytest.TestReport] = []
        self.failed: list[pytest.TestReport] = []
        self.n_runs = n_runs

    def __repr__(self):
        return f"TestResultCollector with {len(self.passing)} passing, {len(self.failing)} failing, and {len(self.flaky)} flaky tests."

    def pytest_runtest_logreport(self, report: pytest.TestReport):
        if report.when == "call":
            if report.passed:
                self.passed.append(report)
            else:
                self.failed.append(report)

    @property
    def flaky(self) -> set[str]:
        return set([f.nodeid for f in self.failed]) & set(
            [p.nodeid for p in self.passed]
        )

    @property
    def passing(self) -> set[str]:
        return set([p.nodeid for p in self.passed]) - self.flaky

    @property
    def failing(self) -> set[str]:
        return set([f.nodeid for f in self.failed]) - self.flaky

    def print_flaky(self):
        print(f"{self.BRT}{self.YLW}\n** FLAKY TESTS DETECTED **{self.RESET}")
        for report in self.flaky:
            print(f"{report}{self.report_starts(report)}")

    def report_starts(self, report: pytest.TestReport) -> str:
        """
        Return a string that looks like
        | Runs / 5 | Passed / 3 |  Passed(%) / 60% |
        """
        n_runs = self.n_runs
        n_passed = len([x for x in self.passed if x.nodeid == report])
        n_pass_pct = f"{n_passed / n_runs * 100:.0f}%"

        return f" || {n_runs} runs || {n_passed} Passed ({n_pass_pct})"


def main(argv: list[str] | None = None) -> int:
    """
    Entry point for the console script. This function is called when the command
    `pytest-flake-detect` is run from the command line.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "test_path",
        type=str,
        # nargs="+",
        help="Path to pass to pytest.",
        default="./tests",
    )

    parser.add_argument(
        "--max-runs",
        type=int,
        help="The maximum number of runs to perform.",
        default=99,
    )

    args = parser.parse_args(argv)
    test_path = Path(args.test_path)
    max_runs = args.max_runs

    print(
        f"About to run pytest-flake-detection on {str(test_path)} {max_runs} times.... "
    )

    collector = TestResultCollector(max_runs)
    for _ in range(max_runs):
        pytest.main(["-q", str(test_path)], plugins=[collector])

    if not collector.flaky:
        print("No flaky tests detected.")
        return 0

    collector.print_flaky()

    return 0
