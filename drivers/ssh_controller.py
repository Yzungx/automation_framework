import paramiko
from scp import SCPClient
from typing import final

# TODO: update logger in here
@final
class SSHController:
    """
        SSHController provides methods to establish SSH connections, execute remote commands, 
        and transfer files using SCP.
    """
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self) -> None:
        """
            Establishes an SSH connection to the remote host using the provided credentials.
            If a connection already exists, it will not create a new one.

            Args:
                None

            Returns:
                None
        """
        if self.client is None or not self.client.get_transport().is_active():
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
        else:
            print("SSH connection already active.")

    def execCommand(self, command) -> tuple:
        """
            Executes a command on the remote server via SSH and returns its standard output.

            Args:
                command (str): The command to execute on the remote server.

            Returns:
                str: The standard output from the executed command, decoded as a string.
        """
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def scp(self, local_path, remote_path) -> None:
        """
            Transfers a file from the local machine to a remote host using SCP.

            Args:
                local_path (str): The path to the file on the local machine to be sent.
                remote_path (str): The destination path on the remote host where the file will be copied.

            Raises:
                SCPException: If the file transfer fails.
                SSHException: If the SSH connection cannot be established.
            Hint:
                # Upload a local file to remote server
                scp.put('local_file.txt', 'remote_file.txt')

                # Download a remote file to local server
                scp.get('remote_file.txt', 'local_file.txt')
        """
        self.connect()
        with SCPClient(self.client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def close(self):
        """
            Closes the SSH client connection if it is open and sets the client attribute to None.
        Args:
                None

            Returns:
                None
        """
        if self.client:
            self.client.close()
            self.client = None

    def disconnect(self) -> None:
        """
            Close the SSH connection if it is active.
        """
        if self.client and self.client.get_transport().is_active():
            self.client.close()
            self.client = None
            print("SSH connection closed.")
        else:
            print("No active SSH connection to close.")

    def __del__(self):
        """
            Destructor to ensure the SSH connection is closed when the object is destroyed.
        """
        self.disconnect()
