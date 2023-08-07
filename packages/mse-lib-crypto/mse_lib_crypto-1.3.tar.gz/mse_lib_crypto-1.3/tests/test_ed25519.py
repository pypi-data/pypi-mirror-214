from mse_lib_crypto.ed25519 import sign, verify, ed25519_keygen


def test_ed25519():
    message: bytes = b"Hello World!"
    pk, seed, _ = ed25519_keygen()

    sig: bytes = sign(message, seed)
    assert verify(message, sig, pk) == message
