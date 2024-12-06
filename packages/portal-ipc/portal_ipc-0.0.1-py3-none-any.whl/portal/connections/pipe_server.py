import threading
import time
from typing import Callable

import pywintypes
import win32file
import win32pipe


class PipeServer:
    def __init__(self, name: str) -> None:
        """Initialize a NamedPipeServer object.

        Args:
            name (str): The name of the named pipe.
        """
        self.pipe_name = rf"\\.\pipe\{name}"
        self.is_connected = False

        self._handle = None
        self._stop_listening = threading.Event()

    def start(self) -> bool:
        """Start the pipe server and wait for client connection.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create the pipe with proper security attributes
            self._handle = win32pipe.CreateNamedPipe(
                self.pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES,  # Allow multiple instances
                65536,
                65536,  # Input/Output buffer sizes
                0,  # Default timeout
                None,  # Default security attributes # type: ignore
            )

            # Wait for client connection
            win32pipe.ConnectNamedPipe(self._handle, None)
            self.is_connected = True
            return True

        except Exception as e:
            print(f"Error starting pipe server: {e}")
            self.is_connected = False
            if self._handle:
                win32file.CloseHandle(self._handle)
                self._handle = None
            return False

    def send(self, data: bytes) -> bool:
        """Send data to the client.

        Args:
            data (bytes): The data to send.

        Returns:
            bool: True if the data was sent successfully, False otherwise.
        """
        if not self.is_connected or not self._handle:
            return False
        try:
            win32file.WriteFile(self._handle, data)  # type: ignore
            # Flush the pipe to ensure data is sent
            win32file.FlushFileBuffers(self._handle)
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            self.is_connected = False  # Mark as disconnected on error
            return False

    def recv(self, buffer_size: int) -> bytes:
        """Receive data from the client.

        Args:
            buffer_size (int): Size of the receive buffer

        Returns:
            bytes: The received data
        """
        if not self.is_connected or not self._handle:
            self.is_connected = False
            return b""

        try:
            _, data = win32file.ReadFile(self._handle, buffer_size)
            return data  # type: ignore
        except pywintypes.error as e:
            if e.winerror == 109:  # ERROR_BROKEN_PIPE
                self.is_connected = False
                self._handle = None
            elif e.winerror == 232:  # ERROR_NO_DATA
                return b""
            else:
                print(f"Error reading from pipe: {e}")
                self.is_connected = False
            return b""

    def listen(self, callback: Callable, buffer_size: int = 1024) -> None:
        """Start listening for incoming data in a separate thread.

        Args:
            callback: Function to call when data is received
            buffer_size (int): Size of the receive buffer
        """
        if not self.is_connected:
            print("Cannot start listening: Not connected")
            return

        def listen_loop():
            while True:  # Keep listening for new connections
                if not self.is_connected:
                    try:
                        # Wait for new connection
                        self.start()
                        if not self.is_connected:
                            time.sleep(1)  # Prevent busy waiting
                            continue
                    except Exception as e:
                        print(f"Connection error: {e}")
                        time.sleep(1)
                        continue

                try:
                    data = self.recv(buffer_size)
                    if data:
                        callback(data)
                except Exception as e:
                    print(f"Error in listen loop: {e}")
                    self._disconnect_client()
                    self.stop_listening()
                    continue  # Continue to accept new connections

        self._listening_thread = threading.Thread(target=listen_loop)
        self._listening_thread.daemon = True
        self._listening_thread.start()

    def _disconnect_client(self) -> None:
        """Disconnect current client but keep server running."""
        if self._handle:
            try:
                win32pipe.DisconnectNamedPipe(self._handle)
            except Exception as e:
                print(f"Error disconnecting client: {e}")
            finally:
                self.is_connected = False

    def stop_listening(self) -> None:
        """Stop the listening thread."""
        self._stop_listening.set()
        if hasattr(self, "_listening_thread") and self._listening_thread.is_alive():
            self._listening_thread.join(timeout=1.0)

    def close(self) -> None:
        """Close the pipe connection."""
        self.is_connected = False
        self.stop_listening()
        if self._handle:
            try:
                win32pipe.DisconnectNamedPipe(self._handle)
                win32file.CloseHandle(self._handle)
            except Exception as e:
                print(f"Error closing handle: {e}")
            finally:
                self._handle = None

    def __str__(self) -> str:
        return f"PipeServer: {self.pipe_name}"
