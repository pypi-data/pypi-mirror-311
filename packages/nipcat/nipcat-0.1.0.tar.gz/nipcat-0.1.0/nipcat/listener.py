import socket
import argparse
import sys
from typing import Optional

class NetcatListener:
    def __init__(self, port: int, host: str = '0.0.0.0'):
        self._validate_port(port)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow port reuse
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @staticmethod
    def _validate_port(port: int) -> None:
        """Validate if port number is within valid range"""
        if not isinstance(port, int):
            raise ValueError("Port must be an integer")
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        if port < 1024 and os.geteuid() != 0:
            raise PermissionError("Ports below 1024 require root privileges")

    def listen(self) -> None:
        """Start listening on specified port"""
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"Listening on {self.host}:{self.port}", file=sys.stderr)

            while True:
                conn, addr = self.sock.accept()
                print(f"Connection from {addr[0]}:{addr[1]}", file=sys.stderr)

                try:
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        # Write to stdout like netcat
                        sys.stdout.buffer.write(data)
                        sys.stdout.buffer.flush()
                except ConnectionResetError:
                    print("Connection reset by peer", file=sys.stderr)
                finally:
                    conn.close()

        except KeyboardInterrupt:
            print("\nReceived interrupt, closing...", file=sys.stderr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            raise
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources"""
        if self.sock:
            self.sock.close()

# def main():
#     parser = argparse.ArgumentParser(description='Python Netcat Listener')
#     parser.add_argument('-p', '--port', type=int, required=True,
#                       help='Port to listen on')
#     parser.add_argument('-H', '--host', default='0.0.0.0',
#                       help='Host interface to listen on (default: 0.0.0.0)')

#     args = parser.parse_args()

#     try:
#         listener = NetcatListener(args.port, args.host)
#         listener.listen()
#     except (ValueError, PermissionError) as e:
#         print(f"Error: {e}", file=sys.stderr)
#         sys.exit(1)

# if __name__ == "__main__":
#     main()
