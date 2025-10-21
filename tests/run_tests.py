from unittest.suite import TestSuite
from unittest.result import TestResult

from tests.board_tests import BoardTests, SigmarFieldTests
from tests.solver_tests import SmallSigmarGameTest


def flatten(list_: list[list]) -> list:
    out = []
    for li_ in list_: out.extend(li_)
    return out


def main_t_runner():
    result = TestResult()
    all_tests = [
        [UnittestClass(t_name) for t_name in [t_name for t_name in dir(UnittestClass) if t_name.startswith("test")]]
        for UnittestClass in [
            BoardTests, SigmarFieldTests, SmallSigmarGameTest
        ]
    ]
    t_suite = TestSuite(flatten(all_tests))
    t_suite.run(result)
    print(result)


if __name__ == '__main__':
    main_t_runner()
