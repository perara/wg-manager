import os

from script.obfuscate import BaseObfuscation, NotInstalledError
import re
import pathlib
import shutil

current_dir = pathlib.Path(__file__).parent.absolute()
shapeshifter_path = current_dir.joinpath("binary/shapeshifter-dispatcher")
shapeshifter_binary = shapeshifter_path.joinpath("shapeshifter-dispatcher")


class GoNotFound(Exception):
    pass


class GoVersionIncompatible(Exception):
    pass


class GitNotInstalled(Exception):
    pass


class ShapeShifterBase(BaseObfuscation):

    def __init__(self):
        super().__init__(
            binary_path=shapeshifter_binary,
            algorithm="obfs4"
        )

        self._go_version_min = (1, 14, 0)

        self.ensure_installed()

    def _verify_go_installed(self):
        output, code = self.execute("version", override_command="go")

        try:
            match = re.findall("go([0-9]+.[0-9]+.[0-9]+)", output)
            match = match[0]
        except IndexError:
            raise GoNotFound("Go was not found on the system.")

        major, minor, patch = match.split(".")

        if int(major) < self._go_version_min[0] or int(minor) < self._go_version_min[1] or \
                int(patch) < self._go_version_min[2]:
            raise GoVersionIncompatible("Go version is incompatible. %s < %s" % (self._go_version_min, match))

    def _verify_git_installed(self):
        output, code = self.execute("version", override_command="git")
        if code == 0:
            return

        raise GitNotInstalled("Git does not seem to be installed. Code: %s, Output: %s" % (code, output))

    def _verify_shapeshifter_installed(self):
        output, code = self.execute("version", override_command=shapeshifter_binary)
        print(output, code)

    def _install_shapeshifter(self):

        if shapeshifter_path.is_dir():
            shutil.rmtree(shapeshifter_path)

        output, code = self.execute(
            "clone",
            "https://github.com/OperatorFoundation/shapeshifter-dispatcher.git",
            shapeshifter_path,
            override_command="git")

        assert code == 0, "Git exited with error. %s" % (output,)

        current_working_dir = os.getcwd()
        os.chdir(shapeshifter_path)

        output, code = self.execute("build", override_command="go")
        os.chdir(current_working_dir)

        assert code == 0, "Building shapeshifter failed with output: %s" % (output,)

    def ensure_installed(self):
        try:
            super().ensure_installed()
        except NotInstalledError:

            self._verify_go_installed()
            self._verify_git_installed()

            try:
                self._verify_shapeshifter_installed()
            except FileNotFoundError:
                self._install_shapeshifter()


if __name__ == "__main__":
    x = ShapeShifterBase()
