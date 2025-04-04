'''sadly this part is not used, as the instructor allow us to use python libraries to do AES-128'''
# padding
# XOR
# CBC block cipher structure


def string_to_binary_padded(string, message_length = 1024):
    # string to binary
    binary_str = ''.join(format(ord(c), '08b') for c in string)

    # padding binary
    padding_length = message_length - len(binary_str)
    if padding_length > 0:
        binary_str = binary_str.ljust(message_length, '0')

    return binary_str

def binary_to_block_arr(binary_str, message_length = 1024, key_length = 128):
    num_blocks = message_length // key_length
    block_arr = []
    for i in range(num_blocks):
        start = i * key_length
        end = start + key_length
        block = binary_str[start:end]
        block_arr.append(block)
    return block_arr

def xor_binary(a_bin, b_bin, key_length):
    # binary to int
    a_int = int(a_bin, 2)
    b_int = int(b_bin, 2)

    # XOR
    result_int = a_int ^ b_int

    # int to binary
    result_binary = bin(result_int)[2:].zfill(key_length)
    return result_binary

def block_cipher_CBC_encryption(plain_block_arr, IV, f, key_length):
    digest = []
    prev_cipher_block = IV
    for block in plain_block_arr:
        xor_result = xor_binary(prev_cipher_block, block, key_length)
        cipher_block = f(xor_result)
        digest.append(cipher_block)
        prev_cipher_block = cipher_block
    return digest

def block_cipher_CBC_decryption(cipher_block_arr, f_inv, IV, key_length):
    plaintext_block_arr = []
    prev_cipher_block = IV
    for cipher_block in cipher_block_arr:
        decrypted_block = f_inv(cipher_block)
        plaintext_block = xor_binary(prev_cipher_block, decrypted_block, key_length)
        plaintext_block_arr.append(plaintext_block)
        prev_cipher_block = cipher_block
    return plaintext_block_arr
