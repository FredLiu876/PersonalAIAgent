import shlex
import subprocess

def run_bash_command(command: str) -> str:
    """
    Executes a bash command as a subprocess and returns the output if successful

    PARAMETERS DESCRIPTION:
    command -> the bash command to execute
    """

    try:
        result = subprocess.run(shlex.split(command), shell=True, check=True, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(e.stderr)
