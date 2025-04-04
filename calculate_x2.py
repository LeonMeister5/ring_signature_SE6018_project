import rsa_generation
import ring_signature

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
x3 = 3
iv = b'\x00' * 16

# hash input
hash_file_path = '1.pdf'
hash_result = ring_signature.calculate_shake128_128bit_digest(hash_file_path)

users = []
# Load users from saved key files
for i in range(1, 4):
    filename = f'user{i}_keys.txt'
    user = rsa_generation.read_user_from_file(filename)
    users.append(user)




# calculate forward
left = v ^ users[0].encrypt(x1)
left = ring_signature.aes_128_cbc_encrypt(left, hash_result, iv)



# calculate backward
right = ring_signature.aes_128_cbc_decrypt(v, hash_result, iv)
right = right ^ users[2].encrypt(x3)
right = ring_signature.aes_128_cbc_decrypt(right, hash_result, iv)

c2 = left ^ right
x2 = users[1].decrypt(c2)
with open("x2.txt", "w") as f:
    f.write(str(x2))
