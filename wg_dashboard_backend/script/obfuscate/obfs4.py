from script.obfuscate import BaseObfuscation
import re


class ObfuscateOBFS4(BaseObfuscation):

    def __init__(self):
        super().__init__(
            binary_name="obfs4proxy",
            binary_path="/usr/bin/obfs4proxy",
            algorithm="obfs4"
        )

        self.ensure_installed()

    def ensure_installed(self):
        super().ensure_installed()

        output, code = self.execute("-version")

        if re.match(f'{self.binary_name}-[0-9]+.[0-9]+.[0-9]+', output) and code == 0:
            return True
        else:
            raise RuntimeError(f"Could not verify that {self.binary_name} is installed correctly.")


if __name__ == "__main__":

    x = ObfuscateOBFS4()
    x.ensure_installed()