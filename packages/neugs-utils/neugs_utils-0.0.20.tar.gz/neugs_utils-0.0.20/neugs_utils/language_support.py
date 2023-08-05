""" Adds additional language support to the testing library
"""
from typing import List, Tuple, Union, Dict
import os
import subprocess


def make(out_file:str, make_file: str = None, force:bool = False) -> Dict[str, str]:
    """Runs make on the input file and returns the stderr and stdout

    Args:
        out_file (str): the file to save out, used for checking for existence
        make_file (str, optional): the make file to use. Defaults to None (uses default makefile/location)
        force (bool, optional): Force recompile even if it already exists. Defaults to False.

    Returns:
        Dict[str, str]: a dictionary with the keys "stdout" and "stderr"
    """
    if not os.path.isfile(out_file) or force:
        if make_file:
            cmd = ["make", "-f", make_file]
        else:
            cmd = ["make"]
        compiled = subprocess.run(cmd, capture_output=True)
        return {"stdout": compiled.stdout.decode(), "stderr": compiled.stderr.decode()}
    else:
        return {"stdout": "", "stderr": ""}

def c_compile(c_files: List[str], out_file:str = '', force:bool = False, compiler="clang -Wall") -> str:
    """Compiles using the clang compiler by default. Will only compile if 
    the file doesn't already exist

    Args:
        c_files (List[str]): list of input files
        out_file (str, optional): _the file to save out. Defaults to ''(which will create a.out)
        force (bool, optional): Force recompile even if it already exists. Defaults to False.
        compiler (str, optional): the compiler to use with arguments. Defaults to clang -Wall
    Returns:
        str: A list of warnings and errors if they happen.
    """
    if not os.path.isfile(out_file) or force:
        if out_file:
            compile_command = compiler.split() + c_files + ["-o", out_file]
        else:
            compile_command = compiler.split() + c_files

        compiled = subprocess.run(compile_command, capture_output=True)
        if (compiled.stderr):
            return "Code failed to compile or had warnings\n{0}".format(compiled.stderr.decode())
    return ''


@DeprecationWarning
def run_range(file:str, start : int , end: int, capture_error: bool = True, timeout: int=120) -> str:
        """Runs subprocess passing in start and end as the first two parameters 
        
        Args:
            file (str): the file / program to run
            start (int): test id of the start test
            end (int): test id of the end test
            capture_error(bool, optional): capture stderr instead of stdout. Defaults to True
            timeout (int, optional): timeout for the subprocess. Defaults to 120.
        Returns:
            str: items printed to stderr
        """
        command = subprocess.run([file, str(start), str(end)], 
                                 capture_output=True, timeout=timeout)
        try:
            if capture_error:
                if command.stderr:
                    return command.stderr.decode()
            else:
                 if command.stdout:
                    return command.stdout.decode()
        except TimeoutError:
            return "Timeout Error"
        return ''


def _convert_to_str_list(args: List) -> List[str]:
    """Converts a list of arguments to a list of strings"""
    return [str(arg) for arg in args]


def c_run(file:str, args:List = [], timeout: int=120,  input: str = '') -> Union[Dict, str]:
        """Runs subprocess passing in start and end as the first two parameters 
        
        Args:
            file (str): the file / program to run
            start (int): test id of the start test
            end (int): test id of the end test
            timeout (int, optional): timeout for the subprocess. Defaults to 120.
        Returns:
            returns a dictionary of stdout and stderr
        """
        proc = subprocess.Popen([file] + _convert_to_str_list(args),  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            #command = subprocess.run([file] + _convert_to_str_list(args), input=input.encode("utf-8"),
            #                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,  timeout=timeout)
           
        
            #command.check_returncode()

            stdout, stderr = proc.communicate(timeout=timeout, input=input.encode("utf-8"))

            if proc.returncode != 0:
                return {"stderr": "Error (segfault or other) - " + str(proc.returncode)}

            return {"stdout": stdout.decode() if stdout else '', 
                    "stderr": stderr.decode() if stderr else ''}
        except TimeoutError:
            proc.kill()
            return {"stderr": "Timeout Error, check to make sure you don't have any infinite loops."}
        except subprocess.CalledProcessError as err:
            return {"stderr": "Error (segfault or other) - " + str(err.returncode)} 

        