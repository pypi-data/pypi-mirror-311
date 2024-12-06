import paramiko
import sshtunnel
import os
import logging
from contextlib import contextmanager

class SSHConnectionManager:
    """Utility class to manage SSH connection."""

    def __init__(self, ssh_host, ssh_port, ssh_username, ssh_key):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_key = os.path.expanduser(ssh_key)
        self.tunnel = None
        self.client = None

    @contextmanager
    def establish_tunnel(self, remote_bind_address=None):
        """Establish an SSH tunnel."""
        if remote_bind_address is None:
            remote_bind_address = (self.ssh_host, self.ssh_port)

        self.tunnel = sshtunnel.open_tunnel(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_username,
            ssh_pkey=self.ssh_key,
            remote_bind_address=remote_bind_address,
        )
        self.tunnel.start()
        logging.info(
            f"SSH tunnel established to {self.ssh_host}:{self.ssh_port}")
        try:
            yield
        finally:
            self.tunnel.stop()
            logging.info("SSH tunnel closed")

    @contextmanager
    def establish_ssh(self):
        """Establish an SSH connection."""
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(
                "127.0.0.1",
                self.tunnel.local_bind_port,
                username=self.ssh_username,
            )
            logging.info("SSH connection established")
            yield self.client
        finally:
            self.client.close()
            logging.info("SSH connection closed")
