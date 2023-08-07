from mse_lib_crypto.x25519 import x25519_keygen, x25519


def test_x25519():
    pk1, sk1 = x25519_keygen()
    pk2, sk2 = x25519_keygen()

    assert x25519(sk2, pk1) == x25519(sk1, pk2)
