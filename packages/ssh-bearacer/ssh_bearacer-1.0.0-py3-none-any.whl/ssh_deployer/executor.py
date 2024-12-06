import logging
import subprocess
import paramiko

class CommandExecutor:
    """Executes commands locally or remotely."""

    @staticmethod
    def execute_remote_command(client: paramiko.SSHClient, command: str) -> str:
        """Execute a command on the remote server."""
        logging.info(f"Executing remote command: {command}")
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)

        output = stdout.read().decode(errors="replace")
        error_message = stderr.read().decode(errors="replace")

        if stdout.channel.recv_exit_status() != 0:
            logging.error(f"Command failed: {error_message}")
            raise RuntimeError(
                f"Command `{command}` failed with error: {error_message}")

        logging.info(f"Command output: {output}")
        return output

    @staticmethod
    def execute_local_command(command: list, error_message: str):
        """Execute a local command."""
        try:
            logging.info(f"Executing local command: {' '.join(command)}")
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            if result.stdout:
                logging.info(result.stdout.decode(errors="replace"))
            if result.stderr:
                logging.warning(result.stderr.decode(errors="replace"))
        except subprocess.CalledProcessError as e:
            logging.error(f"{error_message}: {
                          e.stderr.decode(errors='replace')}")
            raise
