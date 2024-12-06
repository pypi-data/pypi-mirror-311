import logging
from ssh_deployer.connection import SSHConnectionManager
from ssh_deployer.builder import RemoteBuilder
from ssh_deployer.executor import CommandExecutor


class DeploymentManager:
    """Orchestrates the entire deployment process."""

    def __init__(self, ssh_config):
        self.remote = RemoteBuilder(SSHConnectionManager(**ssh_config))

    def run(self, local_commands: list[str], remote_commands: list[str]):
        """Run the deployment process."""
        try:
            logging.info("Starting local build process...")
            for command in local_commands:
                CommandExecutor.execute_local_command(
                    command.split(),
                    f"Local build failed: {command}",
                )
            logging.info("Local build completed. Proceeding to deployment...")
            self.remote.run(remote_commands)
            logging.info("All processes completed successfully!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise
