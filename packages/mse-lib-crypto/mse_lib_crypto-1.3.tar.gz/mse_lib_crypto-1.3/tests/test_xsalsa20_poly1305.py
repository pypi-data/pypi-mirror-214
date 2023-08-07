from pathlib import Path
from mse_lib_crypto.xsalsa20_poly1305 import (
    encrypt,
    decrypt,
    encrypt_directory,
    decrypt_directory,
    random_key,
    KEY_LENGTH,
    NONCE_LENGTH,
)


def test_xsalsa20_poly1305():
    message: bytes = b"Hello World!"
    key: bytes = random_key()

    assert len(key) == KEY_LENGTH

    ciphertext: bytes = encrypt(message, key)
    cleartext: bytes = decrypt(ciphertext, key)

    assert message == cleartext


def test_xsalsa20_poly1305_directory(tmp_path):
    plaindir = tmp_path / "plain"
    plaindir.mkdir()
    dir1 = plaindir / "dir1"
    dir1.mkdir()
    encdir = tmp_path / "encrypted"
    enc_dir1 = encdir / "dir1"

    f1 = dir1 / "file1.txt"
    f2 = dir1 / "file2.txt"

    f1.write_bytes(b"Hello from file1!")
    f2.write_bytes(b"Hello from file2!")

    key: bytes = random_key()

    nonce_map = encrypt_directory(dir1, "*.txt", key, None, [], [], enc_dir1)
    enc_f1 = enc_dir1 / "file1.txt.enc"
    enc_f2 = enc_dir1 / "file2.txt.enc"
    expected_f1 = enc_dir1 / "file1.txt"
    expected_f2 = enc_dir1 / "file2.txt"
    assert enc_f1.read_bytes()[:NONCE_LENGTH] == nonce_map[expected_f1.name]
    assert enc_f2.read_bytes()[:NONCE_LENGTH] == nonce_map[expected_f2.name]

    # test to encrypt with specific nonce_map
    enc_dir1_test = encdir / "test-dir1"
    expected_enc_f1 = enc_dir1_test / "file1.txt.enc"
    expected_enc_f2 = enc_dir1_test / "file2.txt.enc"
    encrypt_directory(dir1, "*.txt", key, nonce_map, [], [], enc_dir1_test)
    assert enc_f1.read_bytes() == expected_enc_f1.read_bytes()
    assert enc_f2.read_bytes() == expected_enc_f2.read_bytes()

    decrypt_directory(enc_dir1, key)
    assert expected_f1.read_bytes() == f1.read_bytes()
    assert expected_f2.read_bytes() == f2.read_bytes()
