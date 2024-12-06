import logging
from ssh_deployer.connection import SSHConnectionManager
from ssh_deployer.executor import CommandExecutor

class RemoteBuilder:
    """Handles remote deployment via SSH."""

    def __init__(self, ssh_manager: SSHConnectionManager):
        self.ssh_manager = ssh_manager

    def run(self, commands: list[str]):
        """Deploy the application."""
        with self.ssh_manager.establish_tunnel():
            with self.ssh_manager.establish_ssh() as client:
                logging.info("Starting deployment...")
                command = " && ".join(commands)
                CommandExecutor.execute_remote_command(client, command)
                logging.info("Deployment completed successfully!")
