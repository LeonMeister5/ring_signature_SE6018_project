#library

import rsa_generation

# SHA3
import hashlib

# AES-128
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad





# Get first 128 bits of shake128 hash digest of the pdf file


def calculate_shake128_128bit_digest(file_path):
    try:
        # open as binary
        with open(file_path, 'rb') as file:
            shake128 = hashlib.shake_128()
            for chunk in iter(lambda: file.read(4096), b""):
                shake128.update(chunk)
            # only obtain first 128 bits
            digest = shake128.digest(16)
            return digest
    except FileNotFoundError:
        print(f"Error: file {file_path} not found.")
        return None
    except Exception as e:
        print(f"Unknown error: {e}.")
        return None
    




# AES-128



def zero_pad(data, block_size): 
    pad_len = (block_size - (len(data) % block_size)) % block_size
    return b'\x00' * pad_len + data

def aes_128_cbc_encrypt(plaintext, key, iv):
    plaintext_bytes = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='big')
    plaintext_bytes = zero_pad(plaintext_bytes, AES.block_size)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext_bytes)
    return int.from_bytes(ciphertext, byteorder='big')

def aes_128_cbc_decrypt(ciphertext, key, iv):
    ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(ciphertext_bytes)
    
    return int.from_bytes(decrypted_text, byteorder='big')





# ring signature with 3 user


def bitwise_xor(a, b):
    return a ^ b

def ring_signature_compute_result(v, rsa_users, xs, f_add, f_syn_enc, key_sync, iv_sync):
    result = v
    for rsa_user, x in zip(rsa_users, xs):
        result = f_add(result, rsa_user.encrypt(x))
        result = f_syn_enc(result, key_sync, iv_sync)
    return result  # expected to be the same as v





if __name__ == "__main__":
    matrix_card = 'G2406344B'
    # treat it as ascii
    matrix_card_binary = ''.join(format(ord(char), '08b') for char in matrix_card)
    # binary to int
    matrix_card_int = int(matrix_card_binary, 2)





    # protocol parameter
    key_length = 1024

    # parameter
    binary_v = bin(matrix_card_int)[2:]
    missing_bits = key_length - len(binary_v)
    if missing_bits > 0:
        padded_binary_v = binary_v + '0' * missing_bits
    else:
        padded_binary_v = binary_v
    v = int(padded_binary_v, 2)

    x1 = 1
    with open('x2.txt', 'r') as file:
        x2 = int(file.read())
    x3 = 3
    iv = b'\x00' * 16

    # hash input
    hash_file_path = '1.pdf'
    hash_result = calculate_shake128_128bit_digest(hash_file_path)

    users = []
    # Load users from saved key files
    for i in range(1, 4):
        filename = f'user{i}_keys.txt'
        user = rsa_generation.read_user_from_file(filename)
        users.append(user)



    print(v)
    print('\n')
    xs = [x1, x2, x3]
    v_should_be_the_same_as_v = ring_signature_compute_result(v, users, xs, bitwise_xor, aes_128_cbc_encrypt, hash_result, iv)
    print(v_should_be_the_same_as_v)
    print('\n')
    if v == v_should_be_the_same_as_v:
        print('Yes this project is f****** awesome!')
    else:
        print('OMG something is wrong TAT!')
        