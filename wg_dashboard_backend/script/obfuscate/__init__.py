import abc
from pathlib import Path
import subprocess
import shlex


class BaseObfuscation(abc.ABC):

    def __init__(self, binary_name=None, binary_path=None, algorithm=None):

        assert binary_name is not None or binary_path is not None
        self.binary_name = binary_name if binary_name is not None else Path(self.binary_path).name
        self.binary_path = binary_path if binary_path else ""
        self.algorithm = algorithm

    def ensure_installed(self):

        # Attempt to find process by path
        binary = Path(self.binary_path)
        if not binary.is_file():
            # Did not find by path, attempt to find using which
            proc_which = subprocess.Popen(["which", self.binary_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = [x.decode().strip() for x in proc_which.communicate() if x != b''][0]

            if proc_which.returncode != 0:
                raise RuntimeError("Could not find binary '%s'" % data)

            self.binary_path = data

    def execute(self, *args, kill_first=False, override_command=None):

        if kill_first:
            # TODO try to delete by full name as we dont want to kill other processes.
            pattern = self.binary_name
            self.execute(*[pattern], override_command="pkill")
            #pattern = self.binary_path + " " + ' '.join(args)
            #print(pattern)
            #kill_output, kill_code = self.execute(*[pattern], override_command="pkill")

        command = override_command if override_command is not None else self.binary_path
        print(shlex.join([command] + list(args)))
        proc_which = subprocess.Popen([command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw_data = proc_which.communicate()

        data = [x.decode().strip() for x in raw_data if x != b'']
        if len(data) == 0:
            data = ""
        else:
            data = data[0]
        return data, proc_which.returncode






