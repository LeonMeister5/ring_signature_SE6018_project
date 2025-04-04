# RSA
import random
from math import gcd


key_length = 1024





# large prime number generation: python random
# large prime number verification: miller_rabin
# RSA


def modulo_mul(a, b, n):
    return (a * b) % n


def modulo_exp(a, e, n):
    main = 1
    now = a
    # e to bin
    e_bin = bin(e)[2:]
    for bit in e_bin:
        if bit == '1':
            main = modulo_mul(main, now, n)
        now = modulo_mul(now, now, n)
    return main
    
def modulo_inv(a, n):
    # find inverse with extended euclidean algorithm
    n0, x0, x1 = n, 0, 1
    while a > 1:
        q = a // n
        n, a = a % n, n
        x0, x1 = x1 - q * x0, x0
    return x1 + n0 if x1 < 0 else x1

# miller_rabin
def is_prime(n, k = 20):
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
        lower_bound = 2**(bits - 1)
        upper_bound = 2**bits
        num = random.randint(lower_bound, upper_bound)
        if is_prime(num):
            return num


def rsa_generate(key_length):
    pq_length = key_length//2
    while True:
        # generate p
        p = generate_prime(pq_length)

        # generate q != p
        q = generate_prime(pq_length)

        if p == q:
            continue

        phi_N = (p - 1) * (q - 1)

        while True:
            e = generate_prime(pq_length//2 + 1) # can be insecure
            if gcd(phi_N, e) == 1:
                n = p * q
                d = modulo_inv(e, phi_N)
                if d < (1 / 3) * (n ** (1 / 4)):
                    continue
                # dmp1 = d % (p - 1)
                # dmq1 = d % (q - 1)
                # coeff = modulo_inv(q, p)
                return {
                    'n': n,
                    'p': p,
                    'q': q,
                    'd': d,
                    'e': e
                    # 'dmp1': dmp1,
                    # 'dmq1': dmq1,
                    # 'coeff': coeff
                }


def rsa_encrypt(m, e, n):
    return modulo_exp(m, e, n)


def rsa_decrypt(c, d, n):
    return modulo_exp(c, d, n)


class rsa_user:
    def __init__(self, *args):
        if len(args) == 1:
            # Consider argument as key_length, random
            key_length = args[0]
            keys = rsa_generate(key_length)
            self.n = keys['n']
            self.p = keys['p']
            self.q = keys['q']
            self.d = keys['d']
            self.e = keys['e']
        elif len(args) == 5:
            # Consider argument as n p q d e, and construct
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
            f.write(f"e: {user.e}\n")
    except Exception as e:
        print(f"Error when saving parameters of user {user_index} : {e}")

def read_user_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].split(': ')[1].strip())
        p = int(lines[1].split(': ')[1].strip())
        q = int(lines[2].split(': ')[1].strip())
        e = int(lines[3].split(': ')[1].strip())

    phi = (p - 1) * (q - 1)
    d = modulo_inv(e, phi)

    return rsa_user(n, p, q, d, e)





for i in range(1, 4):
    user = rsa_user(key_length)
    save_user_keys(user, i)
