<<<<<<< HEAD
"""Collect host facts over SSH."""

import paramiko

COMMANDS = {
    "hostname": "hostname",
    "kernel": "uname -r",
    "os": "cat /etc/os-release",
    "users": "cut -d: -f1 /etc/passwd",
    "processes": "ps -ef",
    "ports": "ss -tulpn",
    "services": "systemctl list-units --type=service --state=running",
}


class Discovery:
    """Runs a fixed set of read-only commands on a remote Linux host."""

    def __init__(self, host: str, user: str = "root", strict_host_keys: bool = False):
        self.host = host
        self.user = user
        # Auto-accepting unknown host keys is convenient in a lab but allows
        # man-in-the-middle attacks; enable strict checking anywhere else.
        self.strict_host_keys = strict_host_keys

    def _connect(self) -> paramiko.SSHClient:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        if not self.strict_host_keys:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.user)
        return ssh

    def collect(self) -> dict[str, str]:
        """Run every command over a single SSH connection."""
        ssh = self._connect()
        try:
            results = {}
            for name, command in COMMANDS.items():
                _, stdout, _ = ssh.exec_command(command)
                results[name] = stdout.read().decode()
            return results
        finally:
            ssh.close()
=======
import paramiko


class Discovery:

    def __init__(self, host, user="root"):
        self.host = host
        self.user = user

    def run(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(self.host, username=self.user)

        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        ssh.close()

        return output

    def collect(self):

        info = {
            "hostname": self.run("hostname"),
            "kernel": self.run("uname -r"),
            "os": self.run("cat /etc/os-release"),
            "users": self.run("cut -d: -f1 /etc/passwd"),
            "processes": self.run("ps -ef"),
            "ports": self.run("ss -tulpn"),
            "services": self.run("systemctl list-units --type=service --state=running")
        }

        return info
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
