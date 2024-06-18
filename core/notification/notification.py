import paramiko


class Notification:
    def __init__(self, ssh_host, ssh_port, ssh_username, ssh_password):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.ssh_client.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                password=self.ssh_password
            )
            print(f"[ssh] SSH connection to {self.ssh_host} established.")
        except Exception as e:
            print(f"[ssh] Error connecting via SSH: {e}")

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            print(f"[ssh] Command '{command}' executed successfully.")
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            if output:
                print(f"[ssh] Output:\n{output}")
            if error:
                print(f"[ssh] Error:\n{error}")
        except Exception as e:
            print(f"Error executing command '{command}': {e}")

    def close(self):
        self.ssh_client.close()
        print(f"[ssh] SSH connection to {self.ssh_host} closed.")
