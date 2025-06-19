# import pytest
# import sys
# from typing import Dict

# class TestExecute:
#     @staticmethod
#     def _run_selected_tests(test_suites: Dict[str, dict]) -> int:
#         """
#             Run selected test suites or specific test cases using pytest.   
#             Args:
#                 test_suites (Dict[str, dict]): Dictionary mapping test file paths to selected test cases.
#                     Example:
#                     {
#                         "tests/test_math.py": {
#                             "selected_tests": ["test_addition", "test_subtract"]
#                         },
#                         "tests/test_utils.py": {
#                             "selected_tests": []
#                         }
#                     }   
#             Returns:
#                 int: Aggregated pytest exit code.
#         """

#         overall_exit_code = 0   
#         for test_path, config in test_suites.items():
#             selected_tests = config.get("selected_tests", [])   
#             if selected_tests:
#                 for func in selected_tests:
#                     print(f"Running: {test_path} -k {func}")
#                     exit_code = pytest.main([test_path, "-k", func])
#                     overall_exit_code |= exit_code
#             else:
#                 print(f"Running all tests in: {test_path}")
#                 exit_code = pytest.main([test_path])
#                 overall_exit_code |= exit_code
#         # if overall_exit_code != 0 -> fail
#         return overall_exit_code
    
#     @staticmethod
#     def run_test(test_suites: Dict[str, dict]) -> int:
#         exit_code = TestExecute._run_selected_tests(test_suites)
#         sys.exit(exit_code)

import pytest
import sys
from typing import Dict, List, Optional

class TestExecute:
    @staticmethod
    def _run_selected_tests(test_suites: Dict[str, dict], pytest_flags: Optional[List[str]] = None) -> int:
        """
        Run selected test suites or specific test cases using pytest.

        Args:
            test_suites (Dict[str, dict]): Mapping test files to selected test cases.
            pytest_flags (List[str], optional): Extra flags to pass to pytest, e.g., ['-s', '--tb=short']

        Returns:
            int: Aggregated pytest exit code.
        """
        overall_exit_code = 0
        pytest_flags = pytest_flags or []  # default to empty list

        for test_path, config in test_suites.items():
            selected_tests = config.get("selected_tests", [])

            if selected_tests:
                for func in selected_tests:
                    args = [test_path, "-k", func] + pytest_flags
                    print(f"Running: pytest {' '.join(args)}")
                    exit_code = pytest.main(args)
                    overall_exit_code |= exit_code
            else:
                args = [test_path] + pytest_flags
                print(f"Running: pytest {' '.join(args)}")
                exit_code = pytest.main(args)
                overall_exit_code |= exit_code

        return overall_exit_code

    @staticmethod
    def run_test(test_suites: Dict[str, dict], pytest_flags: Optional[List[str]] = None) -> int:
        exit_code = TestExecute._run_selected_tests(test_suites, pytest_flags)
        sys.exit(exit_code)
