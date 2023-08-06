"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import os
import sys
from typing import Union


def trace_caller(return_trace: bool = False) -> Union[None, tuple]:
    """Log the method that made the call

    Args:
        return_trace (bool, optional): if true, the trace details\
              are returned as a tuple. Defaults to False.

    Returns:
        (None, tuple): prints the trace details or outputs the same as a tuple
    """
    try:
        raise Exception
    except Exception:
        frame = sys.exc_info()[2].tb_frame.f_back.f_back

        trace_str = (
            " >> invoked by:"
            f" {frame.f_code.co_name}\n\tFile:'{frame.f_code.co_filename}\n\tLine:"
            f" {frame.f_code.co_firstlineno}"
        )

        if return_trace:
            return (trace_str, frame.f_code.co_name)

        print(trace_str)


def importing_script():
    # get working directory
    dir = os.getcwd()
    # get script path as passed to python
    script = sys.argv[0]
    # if path is not absolute, then join with current dir
    importing_script = os.path.join(dir, script) if not os.path.isabs(script) else script

    return importing_script
