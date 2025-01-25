import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from base64 import b64encode

from custom_components.spotcast.spotify.cryptography.diffie_hellman \
    import DiffieHellman
from custom_components.spotcast.spotify.cryptography.utils import (
    write_bytes,
    write_int,
    byte_list_to_int,
    Credentials,
    b64_to_int,
    int_to_bytes,
)


class BlobBuilder:

    def __init__(
            self,
            credentials: Credentials,
            device_id: str,
            remote_pubkey: str,
    ):
        self.credentials: Credentials = credentials
        self.device_id: bytes = bytes(device_id, 'ascii')
        self.remote_pubkey: str = remote_pubkey
        self.dh_keys = DiffieHellman()
        self._blob = b''
        self._encrypted_blob = b''

    def build(self):
        self._build()
        self._encrypt()
        return self._encrypted_blob.decode("ascii")

    def _build(self):  # -> bytes
        blob = bytearray()
        # 'I'
        write_int(0x49, blob)
        # username
        write_bytes(self.credentials.username, blob)
        # 'P'
        write_int(0x50, blob)
        # auth_type
        write_int(self.credentials.auth_type, blob)
        # 'Q'
        write_int(0x51, blob)
        # password
        write_bytes(self.credentials.token, blob)
        # Padding
        n_zeros = 16 - (len(blob) % 16) - 1
        blob.extend([0] * n_zeros)
        blob.append(n_zeros + 1)

        blen = len(blob)
        for i in range(blen - 0x11, -1, -1):
            blob[blen - i - 1] ^= blob[blen - i - 0x11]

        secret = hashlib.sha1(self.device_id).digest()

        keys = PBKDF2(secret, self.credentials.username, 20,
                      count=0x100, hmac_hash_module=SHA1)
        key = bytearray(hashlib.sha1(keys).digest()[:20])
        key.extend(bytearray([0x00, 0x00, 0x00, 0x14]))

        encrypted_blob = bytearray()
        cipher = AES.new(key, mode=AES.MODE_ECB)
        block_size = 16

        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        for chunk in chunker(blob, block_size):
            encrypted_blob.extend(cipher.encrypt(chunk))

        self._blob = b64encode(encrypted_blob)

    def _encrypt(self):
        remote_device_key = b64_to_int(self.remote_pubkey)
        shared_key = self.dh_keys.shared_secret(remote_device_key)

        b_shared_key = int_to_bytes(shared_key)
        base_key = hashlib.sha1(b_shared_key).digest()[:16]

        checksum_key = hmac.new(base_key, b'checksum', 'sha1').digest()
        encryption_key = hmac.new(base_key, b'encryption', 'sha1').digest()

        iv = [253, 81, 222, 19, 70, 203, 45, 89,
              141, 68, 210, 240, 93, 20, 76, 30]
        ctr_e = Counter.new(128, initial_value=byte_list_to_int(iv))
        cipher = AES.new(encryption_key[:16], AES.MODE_CTR, counter=ctr_e)
        encrypted_blob = cipher.encrypt(self._blob)

        checksum = hmac.new(checksum_key, encrypted_blob, 'sha1').digest()

        encrypted_signed_blob = bytearray(iv)
        encrypted_signed_blob.extend(encrypted_blob)
        encrypted_signed_blob.extend(checksum)

        self._encrypted_blob = b64encode(encrypted_signed_blob)
