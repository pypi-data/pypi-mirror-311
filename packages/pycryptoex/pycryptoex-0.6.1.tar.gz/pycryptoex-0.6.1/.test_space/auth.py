from __future__ import annotations

import threading
import hmac
import hashlib
from base64 import b64encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union


def hmac_signature(
    key: str,
    msg: str,
    digest: str = "hex"
) -> Union[str, bytes]:
    hmac_obj = hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256
    )
    if digest == "hex":
        return hmac_obj.hexdigest()
    elif digest == "base64":
        return b64encode(hmac_obj.digest()).decode("utf-8")
    return hmac_obj.digest()


class HMACSignature:
    __slots__ = ("_key", "_hmac_obj", "_lock")

    def __init__(self, key: str) -> None:
        self._key = key
        self._hmac_obj: Optional[hmac.HMAC] = None
        self._lock = threading.Lock()

    def signature(
        self,
        msg: str,
        digest: str = "hex"
    ) -> Union[str, bytes]:
        with self._lock:
            msg_bytes = msg.encode("utf-8")
            if self._hmac_obj is None:
                self._hmac_obj = hmac.new(
                    self._key.encode("utf-8"),
                    msg_bytes,
                    hashlib.sha256
                )
            else:
                self._hmac_obj.update(msg_bytes)
            
            if digest == "hex":
                return self._hmac_obj.hexdigest()
            elif digest == "base64":
                return b64encode(self._hmac_obj.digest()).decode("utf-8")
            return self._hmac_obj.digest()


import timeit

print("HMACSignature ", timeit.timeit(
    setup="""
import threading
import hmac
import hashlib
from base64 import b64encode
from typing import Optional, Union

class HMACSignature:
    __slots__ = ("_key", "_hmac_obj", "_lock")

    def __init__(self, key: str) -> None:
        self._key = key
        self._hmac_obj: Optional[hmac.HMAC] = None
        self._lock = threading.Lock()

    def signature(
        self,
        msg: str,
        digest: str = "hex"
    ) -> Union[str, bytes]:
        with self._lock:
            msg_bytes = msg.encode("utf-8")
            if self._hmac_obj is None:
                self._hmac_obj = hmac.new(
                    self._key.encode("utf-8"),
                    msg_bytes,
                    hashlib.sha256
                )
            else:
                self._hmac_obj.update(msg_bytes)
            
            if digest == "hex":
                return self._hmac_obj.hexdigest()
            elif digest == "base64":
                return b64encode(self._hmac_obj.digest()).decode("utf-8")
            return self._hmac_obj.digest()
s = HMACSignature('XXXXXXXXXX')
    """,
    stmt="s.signature('1658384314791XXXXXXXXXX5000category=option&symbol=BTC-29JUL22-25000-C', 'base64')",
    number=10000
))

print("hmac_signature", timeit.timeit(
    setup="""
import hmac
import hashlib
from base64 import b64encode
from typing import Optional, Union

def hmac_signature(
    key: str,
    msg: str,
    digest: str = "hex"
) -> Union[str, bytes]:
    hmac_obj = hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256
    )
    if digest == "hex":
        return hmac_obj.hexdigest()
    elif digest == "base64":
        return b64encode(hmac_obj.digest()).decode("utf-8")
    return hmac_obj.digest()
    """,
    stmt="hmac_signature('XXXXXXXXXX', '1658384314791XXXXXXXXXX5000category=option&symbol=BTC-29JUL22-25000-C', 'base64')",
    number=10000
))
