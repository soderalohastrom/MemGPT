import subprocess
import platform


def ping_address(self, ip_address: str) -> str:
    """
    Pings the given IP address and returns the result as a string. Always set heartbeat = true.

    Args:
        ip_address (str): The IP address to ping.

    Returns:
        str: The result of the ping command.
    """
    try:
        # Determine the operating system
        os_type = platform.system()

        # Set the command based on the operating system
        # Uses '-c' option for Unix-based systems and '-n' option for Windows.
        if os_type == "Windows":
            cmd = ["ping", "-n", "4", ip_address]
        else:
            cmd = ["ping", "-c", "4", ip_address]

        # Running the ping command
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return response
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the error message
        return str(e.output)
