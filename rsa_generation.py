# RSA
import random
import subprocess
import os
from math import gcd

# --- large prime number generation and verification ---

def modulo_exp(a, e, n):
    result = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            result = (result * a) % n
        a = (a * a) % n
        e //= 2
    return result


def modulo_inv(a, n):
    n0, x0, x1 = n, 0, 1
    while a > 1:
        q = a // n
        n, a = a % n, n
        x0, x1 = x1 - q * x0, x0
    return x1 + n0 if x1 < 0 else x1


def is_prime(n, k=20):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits):
    while True:
        lower_bound = 2 ** (bits - 1)
        upper_bound = 2 ** bits
        num = random.randint(lower_bound, upper_bound)
        if is_prime(num):
            return num


def rsa_encrypt(m, e, n):
    return modulo_exp(m, e, n)


def rsa_decrypt(c, d, n):
    return modulo_exp(c, d, n)


def rsa_generate(key_length):
    pq_length = key_length // 2
    while True:
        p = generate_prime(pq_length)
        q = generate_prime(pq_length)
        if p == q:
            continue
        n = p * q
        if len(bin(n)) - 2 != key_length:
            continue
        phi_N = (p - 1) * (q - 1)
        while True:
            e = generate_prime(pq_length // 2 + 1)
            if gcd(phi_N, e) == 1:
                d = modulo_inv(e, phi_N)
                if d < (1 / 3) * (n ** (1 / 4)):
                    continue
                return {
                    'n': n,
                    'p': p,
                    'q': q,
                    'd': d,
                    'e': e
                }


class rsa_user:
    def __init__(self, *args):
        if len(args) == 1:
            key_length = args[0]
            keys = rsa_generate(key_length)
            self.n = keys['n']
            self.p = keys['p']
            self.q = keys['q']
            self.d = keys['d']
            self.e = keys['e']
        elif len(args) == 5:
            self.n, self.p, self.q, self.d, self.e = args
        else:
            raise ValueError('Incorrect argument.')

    def encrypt(self, message):
        return rsa_encrypt(message, self.e, self.n)

    def decrypt(self, ciphertext):
        return rsa_decrypt(ciphertext, self.d, self.n)


def save_user_keys(user, user_index):
    filename = f'user{user_index}_keys.txt'
    try:
        with open(filename, 'w') as f:
            f.write(f"N: {user.n}\n")
            f.write(f"p: {user.p}\n")
            f.write(f"q: {user.q}\n")
            f.write(f"d: {user.d}\n")
            f.write(f"e: {user.e}\n")
    except Exception as e:
        print(f"Error when saving parameters of user {user_index} : {e}")


def read_user_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].split(': ')[1].strip())
        p = int(lines[1].split(': ')[1].strip())
        q = int(lines[2].split(': ')[1].strip())
        d = int(lines[3].split(': ')[1].strip())
        e = int(lines[4].split(': ')[1].strip())
    phi = (p - 1) * (q - 1)
    d = modulo_inv(e, phi)
    return rsa_user(n, p, q, d, e)


def test_rsa_keys():
    try:
        # First dry-run: calculate x2 and verify ring signature, do NOT save x2.txt
        subprocess.run(["python", "calculate_x2.py"], check=True)
        result = subprocess.run(["python", "ring_signature.py"], capture_output=True, text=True, check=True)
        if "awesome" not in result.stdout:
            return False
        # If dry-run ok, rerun for real, now x2.txt will be saved
        subprocess.run(["python", "calculate_x2.py"], check=True)
        subprocess.run(["python", "ring_signature.py"], check=True)
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    key_length = 1024
    trial = 0
    while True:
        trial += 1
        print(f"Attempt {trial}: generating RSA keys...")
        for i in range(1, 4):
            user = rsa_user(key_length)
            save_user_keys(user, i)
        if test_rsa_keys():
            print("RSA group generated and validated successfully!")
            break
        else:
            print("RSA group invalid, regenerating...\n")
