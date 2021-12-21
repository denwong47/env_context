import os, sys
import unittest
from typing import Union, Iterable, Callable

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from env_context import EnvironmentContext

class TestCaseFileIOError(IOError):
    def __bool__(self):
        return False
    __nonzero__ = __bool__

class TestCasePickleCorrupted(RuntimeError):
    def __bool__(self):
        return False
    __nonzero__ = __bool__


def read_file(
    path:str,
    output:type=str,
)->Union[str, bytes]:
    try:
        with open(path, f"r{'b' if output is bytes else ''}") as _fHnd:
            _return = _fHnd.read()
    except Exception as e:
        _return = TestCaseFileIOError(str(e))

    return _return

_test_data = None

def setUpModule() -> None:
    global _test_data
    
    _file_names = [
    ]

    _test_data = {
        _file_name: \
            read_file(
                TestEnvContext.get_testdata_path(f"{_file_name}"),
                output=bytes if (os.path.splitext(_file_name)[1] in [".pickle",]) else str,
            ) for _file_name in _file_names
    }


class TestEnvContext(unittest.TestCase):

    @classmethod
    def get_testcase_pickle_name(cls, function_name, testcase_id=1):
        return f"testcase_test_{function_name:s}_{testcase_id:02d}"

    @classmethod
    def get_testdata_path(cls, filename:str)->str:
        return os.path.join(cls.get_testdata_dir(), filename)

    @classmethod
    def get_testdata_dir(cls):
        return os.path.join(
            os.path.dirname(sys.argv[0]),
            "data/"
            )

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def setUp(self):
        self.maxDiff=None
        pass

    def tearDown(self):
        pass

    def conduct_tests(
        self,
        func,
        tests:Iterable[dict[str:any]],
        ):

        for _test in tests:
            if (issubclass(_test["answer"], Exception) if (isinstance(_test["answer"], type)) else False):
                with self.assertRaises(Exception) as context:
                    _return = func(
                        **_test["args"]
                    )
                    if (isinstance(_return, Exception)):
                        raise _return

                self.assertTrue(isinstance(context.exception, _test["answer"]))
            elif (isinstance(_test["answer"], type)):
                self.assertTrue(isinstance(func(**_test["args"]), _test["answer"]))
            elif (isinstance(_test["answer"], np.ndarray)):
                if (_test["answer"].dtype in (
                    np.float_,
                    np.float16,
                    np.float32,
                    np.float64,
                    np.float128,
                    np.longfloat,
                    np.half,
                    np.single,
                    np.double,
                    np.longdouble,
                )):
                    _assertion = np.testing.assert_allclose
                else:
                    _assertion = np.testing.assert_array_equal

                _assertion(
                    func(
                        **_test["args"]
                    ),
                    _test["answer"],
                )
            elif (isinstance(_test["answer"], pd.DataFrame)):
                _assertion = assert_frame_equal

                _assertion(
                    func(
                        **_test["args"]
                    ),
                    _test["answer"],
                )
            else:
                self.assertEqual(
                    func(
                        **_test["args"]
                    ),
                    _test["answer"],
                )

    def conduct_tests_on_context_manager(
            self,
            context_manager:type,
            func:Callable,
            *args,
            tests_enter:Union[Iterable[dict], None]=None,
            tests_exit:Union[Iterable[dict], None]=None,
            **kwargs,
        ):
            for _test_enter, _test_exit in zip(tests_enter, tests_exit):
                _construct_test = lambda answer: [
                    {
                        "args":{
                            "context_manager":context_manager,
                            **kwargs,
                        },
                        "answer":answer
                    }
                ]

                with context_manager(**_test_enter.get("args",{})) as _context:
                    # __enter__() test
                    if (_test_enter):
                        self.conduct_tests(
                            func=func,
                            tests=_construct_test(_test_enter.get("answer", None)),
                        )

                # __exit__() test
                if (_test_exit):
                    self.conduct_tests(
                        func=func,
                        tests=_construct_test(_test_exit.get("answer", None)),
                    )

    def test_EnvironmentContext(self):
        _old_environment = dict(os.environ)

        _test_envs = {
            "SAMPLE_ENVVAR1":"Testing Temporary System Variable 1",
            "SAMPLE_ENVVAR2":"Testing Temporary System Variable 2",
            "SAMPLE_ENVVAR3":"Testing Temporary System Variable 3",
        }

        _tests_enter = [
            {
                # These are args for the context manager, not the tests
                "args":{
                    # Just update the variables
                    "update":_test_envs,
                },
                "answer":{
                    **_old_environment,
                    **_test_envs,
                },
            },
            {
                # These are args for the context manager, not the tests
                "args":{
                    # Replace the variables altogether
                    "replace":_test_envs,
                },
                "answer":{
                    **_test_envs,
                },
            }
        ]

        # The exit test should always be the old_environment
        _tests_exit = [
            {
                "args":{
                    # This is ignored
                },
                "answer":_old_environment,
            } for _ in _tests_enter
        ]


        def _test(context_manager:type, *args, **kwargs):
            # The test is literally just the current set of Environment Variables
            return dict(os.environ)

        self.conduct_tests_on_context_manager(
            context_manager = EnvironmentContext,
            func = _test,
            tests_enter=_tests_enter,
            tests_exit=_tests_exit,
        )


if __name__ == "__main__":
    unittest.main()