#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Tuple
)

from .libs.base58 import (
    encode, decode
)
from .const import WIF_TYPES
from .crypto import double_sha256
from .utils import (
    get_bytes, integer_to_bytes, bytes_to_string
)

# Wallet import format prefix
WIF_PREFIX: int = 0x80
# Private key prefixes
UNCOMPRESSED_PRIVATE_KEY_PREFIX: int = 0x00
COMPRESSED_PRIVATE_KEY_PREFIX: int = 0x01
# Checksum byte length
CHECKSUM_BYTE_LENGTH: int = 4


def get_checksum(raw: bytes) -> bytes:
    return double_sha256(raw)[:CHECKSUM_BYTE_LENGTH]


def encode_wif(private_key: Union[str, bytes]) -> Tuple[str, str]:
    if len(get_bytes(private_key)) != 32:
        raise ValueError(f"Invalid private key length (expected 64, got {len(private_key)!r})")

    wif_payload: bytes = (
        integer_to_bytes(WIF_PREFIX) + get_bytes(private_key)
    )
    wif_compressed_payload: bytes = (
        integer_to_bytes(WIF_PREFIX) + get_bytes(private_key) + integer_to_bytes(COMPRESSED_PRIVATE_KEY_PREFIX)
    )
    return (
        encode(wif_payload + get_checksum(wif_payload)),
        encode(wif_compressed_payload + get_checksum(wif_compressed_payload))
    )


def decode_wif(wif: str) -> Tuple[bytes, str, bytes]:

    raw: bytes = decode(wif)
    if not raw.startswith(integer_to_bytes(0x80)):
        raise ValueError(f"Invalid wallet import format")

    prefix_length: int = len(integer_to_bytes(WIF_PREFIX))
    prefix_got: bytes = raw[:prefix_length]
    if integer_to_bytes(WIF_PREFIX) != prefix_got:
        raise ValueError(f"Invalid WIF prefix (expected {prefix_length!r}, got {prefix_got!r})")

    raw_without_prefix: bytes = raw[prefix_length:]

    checksum: bytes = raw_without_prefix[-1 * 4:]
    private_key: bytes = raw_without_prefix[:-1 * 4]
    wif_type: str = WIF_TYPES.WIF

    if len(private_key) not in [33, 32]:
        raise ValueError(f"Invalid wallet import format")
    elif len(private_key) == 33:
        private_key = private_key[:-len(integer_to_bytes(COMPRESSED_PRIVATE_KEY_PREFIX))]
        wif_type = WIF_TYPES.WIF_COMPRESSED

    return private_key, wif_type, checksum


def private_key_to_wif(private_key: Union[str, bytes], wif_type: str = WIF_TYPES.WIF_COMPRESSED) -> str:
    """
    Private key to Wallet Import Format (WIF) converter

    :param private_key: Private key
    :type private_key: Union[str, bytes]
    :param wif_type: Wallet Import Format (WIF) type, default to ``wif-compressed``
    :type wif_type: str

    :returns: str -- Wallet Import Format
    """

    # Getting uncompressed and compressed
    wif, wif_compressed = encode_wif(private_key=private_key)

    if wif_type == WIF_TYPES.WIF:
        return wif
    elif wif_type == WIF_TYPES.WIF_COMPRESSED:
        return wif_compressed
    else:
        raise ValueError("Invalid WIF type, choose only 'wif' or 'wif-compressed' types")


def wif_to_private_key(wif: str) -> str:
    """
    Wallet Import Format (WIF) to Private key converter

    :param wif: Wallet Import Format
    :type wif: str

    :returns: str -- Private key
    """

    return bytes_to_string(decode_wif(wif=wif)[0])


def get_wif_type(wif: str) -> str:
    """
    Get Wallet Import Format (WIF) type

    :param wif: Wallet Import Format
    :type wif: str

    :returns: str -- WFI type
    """

    return decode_wif(wif=wif)[1]


def get_wif_checksum(wif: str) -> str:
    """
    Get Wallet Import Format (WFI) checksum

    :param wif: Wallet Import Format
    :type wif: str

    :returns: str -- WFI checksum
    """

    return bytes_to_string(decode_wif(wif=wif)[2])
