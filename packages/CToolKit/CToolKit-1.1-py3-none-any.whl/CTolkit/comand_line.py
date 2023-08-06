
from CToolKit.Errors.CopilationError import  CommandLineError
import subprocess


def compile_project_by_command(command: str, raise_errors: bool = True, raise_warnings:  bool = True):
    status_code,output = subprocess.getstatusoutput(command)

    if raise_errors and status_code != 0:
        raise CommandLineError(output, status_code)

    if raise_warnings and 'warning:' in output:
        raise CommandLineError(output, status_code)



'''
def copile_project(compiler:str,output:str,flags:list[str],raise_warnings:bool,raise_erros:bool):
    pass
'''