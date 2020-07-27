from pathlib import Path

import requests

import const
from script.obfuscate import BaseObfuscation
import re
import os
import qrcode
import socket

from script.obfuscate.obfs4 import ObfuscateOBFS4


class ObfuscationViaTOR(BaseObfuscation):

    def __init__(self, algorithm: BaseObfuscation):
        super().__init__(
            binary_name="tor"
        )
        self.algorithm = algorithm
        self.tor_data_dir = "/tmp/wg-manager-tor-proxy"
        self.tor_config_file = "/tmp/wg-manager-tor-proxy/torrc"
        self.tor_fingerprint_file = f"{self.tor_data_dir}/fingerprint"
        self.tor_bridge_file = f"{self.tor_data_dir}/pt_state/obfs4_bridgeline.txt"

        Path(self.tor_config_file).touch()
        os.makedirs(self.tor_data_dir, exist_ok=True)

    def __del__(self):
        pass

    def ensure_installed(self):
        super().ensure_installed()
        output, code = self.execute("--version")

        if re.match(f'Tor version .*', output) and code == 0:
            return True
        else:
            raise RuntimeError(f"Could not verify that {self.binary_name} is installed correctly.")

    def start(self):

        output, code = self.execute(
            "-f", self.tor_config_file,
            "--DataDirectory", self.tor_data_dir,
            "--RunAsDaemon", "1",
            "--ExitPolicy", "reject *:*",
            "--ORPort", str(const.OBFUSCATE_SOCKS_TOR_PORT),
            "--BridgeRelay", "1",
            "--PublishServerDescriptor", "0",
            "--ServerTransportPlugin", f"{self.algorithm.algorithm} exec {self.algorithm.binary_path}",
            "--ServerTransportListenAddr", f"{self.algorithm.algorithm} 0.0.0.0:{const.OBFUSCATE_TOR_LISTEN_ADDR}",
            "--ExtORPort", "auto",
            "--ContactInfo", "wg-manager@github.com",
            "--Nickname", "wgmanager",
            kill_first=True
        )

        print(output)

    def generate_bridge_line(self, local=False):

        if local:
            ip_address = socket.gethostbyname(socket.gethostname())
        else:
            ip_address = requests.get("https://api.ipify.org").text

        with open(self.tor_fingerprint_file, "r") as f:
            fingerprint = f.read().split(" ")
            assert len(fingerprint) == 2, "Could not load fingerprint correctly. " \
                                          "Should be a list of 2 items (name, fingerprint)"
            fingerprint = fingerprint[1]

        with open(self.tor_bridge_file, "r") as f:
            bridge_line_raw = f.read()

        bridge_line = re.search(r"^Bridge .*", bridge_line_raw, re.MULTILINE).group(0)
        bridge_line = bridge_line\
            .replace("<IP ADDRESS>", ip_address)\
            .replace("<PORT>", str(const.OBFUSCATE_TOR_LISTEN_ADDR))\
            .replace("<FINGERPRINT>", fingerprint)\
            .replace("Bridge ", "bridge://")\
            .replace("\n", "")
        #bridge_line = f"bridge://{self.algorithm.algorithm} {ip_address}:{const.OBFUSCATE_SOCKS_TOR_PORT} {fingerprint}"
        print(bridge_line)
        return bridge_line

    def output_qr(self, text, image=False):

        qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        if image:
            img = qr.make_image(fill_color="black", back_color="white")
            img.show()
        else:
            try:
                qr.print_tty()
            except:
                qr.print_ascii()


if __name__ == "__main__":

    x = ObfuscationViaTOR(
        algorithm=ObfuscateOBFS4()
    )
    x.ensure_installed()
    x.start()
    bridge_line = x.generate_bridge_line(local=False)
    x.output_qr(bridge_line, image=True)
    #x.generate_bridge_line(local=False)