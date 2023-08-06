import ipaddress
import logging
from queue import Empty, Full
import socket
import multiprocessing
from typing import ByteString, Optional
from durin import io
from durin.actuator import StreamOn
from durin.io.runnable import RunnableConsumer, RunnableProducer


def get_ip(ip):
    # Thanks to https://stackoverflow.com/a/28950776/999865
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect((ip, 1))
        ip_guess = s.getsockname()[0]
    except Exception:
        ip_guess = "127.0.0.1"
    finally:
        s.close()
    return ip_guess

def checksum(bs):
    checksum = bs[0]
    for b in bs[1:]:
        checksum = checksum ^ b
    return checksum


class TCPProducer(RunnableProducer):

    def produce(self, sock):
        try:
            header = sock.recv(3)
            size = int.from_bytes(header[1:], 'little')
            size = size & (0b0000111111111111) # Zero out meta-bits
            bs = sock.recv(size)
            check_actual = int.from_bytes(sock.recv(1), 'little')
            check_bytes = checksum(header + bs)
            if (check_actual == check_bytes):
                return bs
            else:
                logging.warning(f"Checksum failed: {check_actual} != {check_bytes}")
                return None

        except BlockingIOError:
            return None


class TCPConsumer(RunnableConsumer):

    def consume(self, event, sock):
        bs = b'*' + len(event).to_bytes(2, "little") + event
        bs = bs + checksum(bs).to_bytes(1, 'little')
        sock.send(bs)


class TCPLink:
    """ """

    def __init__(
        self,
        host: str,
        port: str,
        buffer_size_send: int = 50,
        buffer_size_receive: int = 2000,
    ):
        address = (host, int(port))
        context = multiprocessing.get_context("spawn")
        # Buffer towards Durin
        self.buffer_send = context.Queue(buffer_size_send)
        # Buffer receiving replies
        self.buffer_receive = context.Queue(buffer_size_receive)

        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(address)
            self.sock.setblocking(False)
        except (ConnectionRefusedError, OSError) as e:
            raise ConnectionRefusedError(f"Cannot reach Durin at {address}")

        # Create producer/consumer
        self.sender = TCPConsumer(self.buffer_send, self.sock)
        self.receiver = TCPProducer(self.buffer_receive, self.sock)

    def start(self):
        self.sender.start()
        self.receiver.start()

    def stop(self):
        self.sock.close()
        self.buffer_receive.close()
        self.buffer_send.close()
        self.sender.stop()
        self.receiver.stop()
        logging.debug(f"TCP control communication stopped")

    def send(self, command: ByteString, timeout: float) -> None:
        try:
            self.buffer_send.put(command, block=False, timeout=timeout)
        except Full:
            return None

    def read(self) -> Optional[ByteString]:
        try:
            return self.buffer_receive.get(block=False)
        except Empty:
            return None


class UDPLink(RunnableProducer):
    """
    An UDPBuffer that silently buffers messages received over UDP into a queue.
    """

    def __init__(
        self, host: str, ip: str, packet_size: int = 512, buffer_size: int = 100
    ):
        self.buffer_size = buffer_size
        self.packet_size = packet_size
        context = multiprocessing.get_context("spawn")
        self.buffer = context.Queue(self.buffer_size)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (host, ip)
        self.sock.bind(address)
        self.sock.setblocking(0)
        logging.debug(f"UDP control receiving on {address}")

        super().__init__(self.buffer, self.sock)

    def produce(self, sock):
        try:
            buffer = sock.recv(self.packet_size)
            size = int.from_bytes(buffer[1:3], "little")
            size = size & (0b0000111111111111) # Zero out meta-bits
            check_actual = int.from_bytes(buffer[3 + size : 4 + size], 'little')
            check_bytes = checksum(buffer[:3 + size])
            if (int(check_actual) == check_bytes):
                msg = io.decode(buffer[3 : 3 + size])
                return msg
            else:
                logging.warning(f"Checksum failed: {check_actual} != {check_bytes}")
                return None
        except BlockingIOError:
            return None

    def stop(self):
        super().stop()
        self.sock.close()
        self.buffer.close()
        logging.debug(f"UDP communication stopped")


# class DVSClient(TCPLink):
#     def __init__(self, host: str, port: int) -> None:
#         self.sock = None
#         self.address = (host, port)

#     def _init_connection(self):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.connect(self.address)
#         self.sock.setblocking(0)
#         logging.debug(f"UDP DVS communication sending to {self.address}")

#     def _send_message(self, message: bytes):
#         try:
#             self.sock.send(message)
#         except (BrokenPipeError, AttributeError) as e:
#             try:
#                 self._init_connection()
#             except ConnectionRefusedError as e:
#                 raise ConnectionRefusedError(
#                     f"Could not connect to DVS controller at {self.address}"
#                 )
#             self._send_message(message)

#     def start_stream(self, host: str, port: int):
#         # cmd = StreamOn(host, port, 1)
#         # self._send_message(cmd.encode())
#         data = bytearray([0] * 7)
#         data[0] = 0x0
#         data[1:5] = int(ipaddress.ip_address(host)).to_bytes(4, "little")
#         data[5:7] = port.to_bytes(2, "little")
#         self._send_message(data)

#     def stop_stream(self):
#         if self.sock is not None:
#             self._send_message(bytes([1]))
#             self.sock.close()
#             self.sock = None
