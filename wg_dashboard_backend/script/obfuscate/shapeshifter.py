import os
from threading import Thread

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
    MODES_SUPPORTED = ["server", "client"]
    ALGORITHMS_SUPPORTED = ["obfs4"]

    def __init__(self, mode, algorithm, wireguard_port=None, listen_port=None, client_replicant_port=None, client_options=None):
        super().__init__(
            binary_path=shapeshifter_binary,
            algorithm=algorithm
        )

        assert mode in ShapeShifterBase.MODES_SUPPORTED, "%s is not a supported mode. Supported: %s" % (
            mode, ShapeShifterBase.MODES_SUPPORTED
        )

        self._wireguard_port = wireguard_port
        self._listen_port = listen_port
        self._client_replicant_port = client_replicant_port
        self._mode = mode
        self._client_options = client_options

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

    def start(self):

        bind_command = "bindaddr" if self._mode == "server" else "proxylistenaddr"
        bind_port = self._listen_port if self._mode == "server" else self._client_replicant_port
        bind_value = f"127.0.0.1:{bind_port}"  # TODO
        if self._mode == "server":
            bind_value = self.algorithm + "-" + bind_value
        connect_command = "orport" if self._mode == "server" else "target"
        connect_port = self._wireguard_port if self._mode == "server" else self._listen_port

        cmd = [
            "-transparent",
            "-udp",
            f"-{self._mode}",
            "-state", f"state",
            f"-{connect_command}", f"127.0.0.1:{connect_port}",
            "-transports", self.algorithm,
            f"-{bind_command}", bind_value
        ]

        if self._mode == "client":
            cmd.extend([
                "-options", f"{self._client_options}"
            ])

        cmd.extend([
            "-logLevel", "DEBUG",
            "-enableLogging",
        ])
        print(*cmd)
        output, code = self.execute(*cmd, stream=True, prefix=self._mode)
        print(output, code)

    def start_threaded(self):
        t = Thread(target=self.start, args=())
        t.start()
        return t


if __name__ == "__main__":
    import time
    x = ShapeShifterBase(
        mode="server",
        algorithm="obfs2",
        wireguard_port=3333,
        listen_port=2222,
    )
    x.start_threaded()

    time.sleep(1)

    x = ShapeShifterBase(
        mode="client",
        algorithm="obfs2",
        listen_port=2222,
        client_replicant_port=1443,
        client_options='{"cert": "BWvGMVn3C8daXai2Xo+If23XS94eztZE9Kbtykvy9x5ADWc6YCHdGlWQfDh1fzu7AhuTIA", "iat-mode": "0"}'
    )
    x.start_threaded()



    while True:
        time.sleep(1)