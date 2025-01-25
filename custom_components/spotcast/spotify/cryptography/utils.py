from base64 import b64decode, b64encode


def write_int(i: int, out: bytearray):
    if i < 0x80:
        out.append(i)
    else:
        out.append(0x80 | (i & 0x7f))
        out.append((i >> 7))


def write_bytes(b: bytes, out: bytearray):
    write_int(len(b), out)
    out.extend(b)


def byte_list_to_int(byte_list):
    return int.from_bytes(bytes(byte_list), 'big')


def int_to_bytes(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')


def int_to_b64str(i: int):
    return b64encode(int_to_bytes(i)).decode('ascii')


def b64_to_int(b64: str):
    return int.from_bytes(b64decode(b64), 'big')


class Credentials:
    def __init__(self, username: str, token: str, auth_type: int = 0x04):
        self.username: bytes = bytes(username, 'ascii')
        self.token: bytes = bytes(token, 'ascii')
        self.auth_type: int = 0x03
