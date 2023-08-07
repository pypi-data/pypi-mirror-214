from mse_lib_crypto.x25519 import x25519_keygen
from mse_lib_crypto.seal_box import seal, unseal


def test_seal_box():
    message: bytes = b"Hello World!"
    pk, sk = x25519_keygen()

    ciphertext: bytes = seal(message, pk)
    cleartext: bytes = unseal(ciphertext, sk)

    assert message == cleartext
