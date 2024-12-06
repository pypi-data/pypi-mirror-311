import time

import pywintypes
import win32file
import win32pipe


class PipeClient:
    def __init__(self, name: str) -> None:
        """
        Initialize a PipeClient object.

        :param name: The name of the named pipe to connect to.
        """
        self.pipe_name = rf"\\.\pipe\{name}"
        self.handle = None
        self.connected = False

    def connect(self, max_attempts: int = 5) -> None:
        """
        Connect to the named pipe server.

        :param max_attempts: Maximum number of attempts to connect.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                self.handle = win32file.CreateFile(
                    self.pipe_name,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None,
                )
                self.connected = True
                print(f"Connected to named pipe {self.pipe_name}.")
                return
            except pywintypes.error as e:
                if e.winerror == 2:  # ERROR_FILE_NOT_FOUND
                    # Pipe server not available yet, wait and retry
                    time.sleep(0.1)
                elif e.winerror == 231:  # ERROR_PIPE_BUSY
                    # All pipe instances are busy, wait and retry
                    if not win32pipe.WaitNamedPipe(self.pipe_name, 2000):
                        time.sleep(0.1)
                elif e.winerror == 5:  # ERROR_ACCESS_DENIED
                    # The pipe exists, but cannot open yet
                    time.sleep(0.1)
                else:
                    print(f"Failed to connect to pipe: {e}")
                    raise e
            attempts += 1
        raise Exception(
            f"Could not connect to named pipe {self.pipe_name} after {max_attempts} attempts."
        )

    def send(self, data: bytes) -> bool:
        """
        Send data to the pipe server.

        :param data: Data to send.
        :return: True if sent successfully, False otherwise.
        """
        if not self.connected or not self.handle:
            raise Exception("Pipe client is not connected to the server.")
        try:
            win32file.WriteFile(self.handle.handle, data)
            return True
        except pywintypes.error as e:
            print(f"Error writing to pipe: {e}")
            return False

    def recv(self, buffer_size: int) -> bytes:
        """
        Receive data from the pipe server.

        :return: Data received.
        """
        if not self.connected or not self.handle:
            raise Exception("Pipe client is not connected to the server.")
        try:
            _, data = win32file.ReadFile(self.handle.handle, buffer_size)
            return data  # type: ignore
        except pywintypes.error as e:
            print(f"Error reading from pipe: {e}")
            return b""
    
    def shutdown_server(self) -> None:
        pass

    def close(self) -> None:
        """
        Close the pipe handle.
        """
        if self.handle:
            win32file.CloseHandle(self.handle.handle)
            self.handle = None
            self.connected = False
            print("Named pipe client closed.")

    def __str__(self) -> str:
        return f"NamedPipeClient: {self.pipe_name}"
