from base64 import b64decode, b64encode

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import importKey


def encode_key(key):
    return b64encode(
        key.exportKey('PEM'),
    ).decode('utf-8')


def import_key(key):
    return importKey(
        b64decode(
            key.encode('utf-8'),
        ),
    )


def make_keys():
    class Keypair():
        pass
    private = RSA.generate(2048, Random.new().read)
    keypair = Keypair()
    keypair.private = encode_key(private)
    keypair.public = encode_key(private.publickey())
    return keypair


def encryptstring(publickey, string):
    encryptor = PKCS1_OAEP.new(import_key(publickey))
    encrypted_msg = encryptor.encrypt(string.encode('utf-8'))
    return b64encode(encrypted_msg).decode('utf-8')


def decrypthash(privatekey, encoded_hash):
    decoded_encrypted_msg = b64decode(encoded_hash.encode('utf-8'))
    decryptor = PKCS1_OAEP.new(import_key(privatekey))
    return decryptor.decrypt(decoded_encrypted_msg).decode('utf-8')
