class SS:
    codes = [
        '''
def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr((ord(char.lower()) - ord('a') + shift_amount) % 26 + ord('a'))
            encrypted_text += new_char.upper() if char.isupper() else new_char
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr((ord(char.lower()) - ord('a') - shift_amount) % 26 + ord('a'))
            decrypted_text += new_char.upper() if char.isupper() else new_char
        else:
            decrypted_text += char
    return decrypted_text

#message = "Hello World"
#shift_value = 3

message = input("Enter the message: ")
shift_value = int(input("Enter the shift value: "))

encrypted_message = encrypt(message, shift_value)
print(f"Encrypted Message: {encrypted_message}")

decrypted_message = decrypt(encrypted_message, shift_value)
print(f"Decrypted Message: {decrypted_message}")
        ''',
        '''
def create_matrix(key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    for char in key:
        if char not in used and char in alphabet:
            matrix.append(char)
            used.add(char)

    for char in alphabet:
        if char not in used:
            matrix.append(char)
            used.add(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def preprocess_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    result = []
    i = 0

    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                result.append(a + "X")
                i += 1
            else:
                result.append(a + b)
                i += 2
        else:
            result.append(a + "X")
            i += 1

    return result

def find_position(matrix, char):
    for row, line in enumerate(matrix):
        if char in line:
            return row, line.index(char)
    return None, None

def encrypt_digraph(matrix, digraph):
    a, b = digraph
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)

    if row_a == row_b:
        return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
    elif col_a == col_b:
        return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
    else:
        return matrix[row_a][col_b] + matrix[row_b][col_a]

def decrypt_digraph(matrix, digraph):
    a, b = digraph
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)

    if row_a == row_b:
        return matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
    elif col_a == col_b:
        return matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
    else:
        return matrix[row_a][col_b] + matrix[row_b][col_a]

def encrypt(plaintext, key):
    matrix = create_matrix(key)
    plaintext_digraphs = preprocess_text(plaintext)
    ciphertext = ""

    for digraph in plaintext_digraphs:
        ciphertext += encrypt_digraph(matrix, digraph)

    return ciphertext

def decrypt(ciphertext, key):
    matrix = create_matrix(key)
    ciphertext_digraphs = preprocess_text(ciphertext)
    plaintext = ""

    for digraph in ciphertext_digraphs:
        plaintext += decrypt_digraph(matrix, digraph)

    return plaintext


#key = "PLAYFAIR"
#plaintext = "HELLO WORLD"

key = input("Enter the key: ")
plaintext = input("Enter the plain text: ")


ciphertext = encrypt(plaintext, key)
decrypted_text = decrypt(ciphertext, key)

print(f"Key: {key}")
print(f"Plaintext: {plaintext}")
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted Text: {decrypted_text}")
        ''',
        '''
import numpy as np

def matrix_mod_inv(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)
    matrix_mod_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_mod_inv

def hill_cipher_encrypt(plain_text, key_matrix):
    plain_text = plain_text.replace(" ", "").upper()
    while len(plain_text) % key_matrix.shape[0] != 0:
        plain_text += "X"
    plain_nums = [ord(char) - ord("A") for char in plain_text]
    plain_matrix = np.array(plain_nums).reshape(-1, key_matrix.shape[0])
    cipher_matrix = np.dot(plain_matrix, key_matrix) % 26
    cipher_text = "".join([chr(num + ord("A")) for num in cipher_matrix.flatten()])
    return cipher_text

def hill_cipher_decrypt(cipher_text, key_matrix):
    cipher_text = cipher_text.replace(" ", "").upper()
    cipher_nums = [ord(char) - ord("A") for char in cipher_text]
    cipher_matrix = np.array(cipher_nums).reshape(-1, key_matrix.shape[0])
    key_matrix_inv = matrix_mod_inv(key_matrix, 26)
    plain_matrix = np.dot(cipher_matrix, key_matrix_inv) % 26
    plain_text = "".join([chr(int(num) + ord("A")) for num in plain_matrix.flatten()])
    return plain_text

key_matrix = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])

plain_text = input("Enter the plain text: ").strip()
cipher_text = hill_cipher_encrypt(plain_text, key_matrix)
print(f"Encrypted: {cipher_text}")

decrypted_text = hill_cipher_decrypt(cipher_text, key_matrix)
print(f"Decrypted: {decrypted_text}")
        ''',
        '''
def create_vigenere_matrix():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    matrix = []
    for i in range(26):
        row = alphabet[i:] + alphabet[:i]
        matrix.append(row)
    return matrix

def encrypt_vigenere(plain_text, keyword):
    plain_text = plain_text.upper().replace(" ", "")
    keyword = keyword.upper().replace(" ", "")
    repeated_keyword = []
    keyword_length = len(keyword)
    for i in range(len(plain_text)):
        repeated_keyword.append(keyword[i % keyword_length])
    matrix = create_vigenere_matrix()
    cipher_text = []
    for pt_char, kw_char in zip(plain_text, repeated_keyword):
        if pt_char.isalpha():
            row_index = ord(pt_char) - ord('A')
            col_index = ord(kw_char) - ord('A')
            cipher_char = matrix[row_index][col_index]
            cipher_text.append(cipher_char)
        else:
            cipher_text.append(pt_char)
    return "".join(cipher_text)

if __name__ == "__main__":
    plain_text = input("Enter the plaintext: ").strip()
    keyword = input("Enter the keyword: ").strip()
    encrypted_text = encrypt_vigenere(plain_text, keyword)
    print("Encrypted text:", encrypted_text)
        ''',
        '''
def power(a, b, p):
    if b == 1:
        return a % p
    else:
        return pow(a, b, p)
        
def main():
    P = 23
    print("The value of P:", P)

    G = 6
    print("The value of G:", G)

    a = 4 
    print("The private key a for Alice:", a)

    x = power(G, a, P)
    print("Alice's public key is:", x)

    b = 3 
    print("The private key b for Bob:", b)

    y = power(G, b, P)
    print("Bob's public key is:", y)
    
    ka = power(y, a, P) 
    kb = power(x, b, P) 
    print("Secret key for Alice is:", ka)
    print("Secret key for Bob is:", kb)
if _name_ == "_main_":
    main()
        ''',
        '''
import math

def gcd(a, h):
    temp = 0
    while(1):
        
        temp = a % h
        if (temp == 0):
            return h
        a = h
        h = temp
    return a

p = 3
q = 7
n = p * q 
e = 2
phi = (p - 1) * (q - 1)

while (e < phi):
    if gcd(e, phi) == 1:
         break
    else:
         e += 1

k = 2 
d = (1 + (k * phi))/e

msg = 12
print("Message data:", msg)

c = pow(msg, e, n)
c = math.fmod(c,n)
print("Encrypted data:", c)
  
m = pow(c, d) 
m = math.fmod(m,n)
print("Orignal Message Sent:", m)
        ''',
        '''
import hashlib

def md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

if __name__ == "__main__":
    user_input = input("Enter a string to hash with MD5: ")
    hash_result = md5_hash(user_input)
    print(f"MD5 hash of '{user_input}': {hash_result}")
        ''',
        '''
import hashlib

def sha1_hash(input_string):
    sha1 = hashlib.sha1()
    sha1.update(input_string.encode('utf-8'))
    return sha1.hexdigest()

if __name__ == "__main__":
    input_str = input("Enter a string to hash: ")
    hash_value = sha1_hash(input_str)
    print(f"SHA-1 hash of '{input_str}': {hash_value}")
        ''',
        '''
        from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Message to be signed
message = b"This is a secret message."

# Sign the message
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print(f"Signature: {signature.hex()}")

# Verify the signature
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature is valid.")
except Exception as e:
    print("Signature is invalid:", e)

        ''',
        '''
        # Function to find gcd of two numbers
def euclid(m, n):
    if n == 0:
        return m
    else:
        r = m % n
        return euclid(n, r)

# Program to find Multiplicative inverse
def exteuclid(a, b):
    r1 = a
    r2 = b
    s1 = int(1)
    s2 = int(0)
    t1 = int(0)
    t2 = int(1)
    while r2 > 0:
        q = r1 // r2
        r = r1 - q * r2
        r1 = r2
        r2 = r
        s = s1 - q * s2
        s1 = s2
        s2 = s
        t = t1 - q * t2
        t1 = t2
        t2 = t
    if t1 < 0:
        t1 = t1 % a
    return (r1, t1)

# Enter two large prime numbers p and q
p = 823
q = 953
n = p * q
Pn = (p - 1) * (q - 1)

# Generate encryption key in range 1 < e < Pn
key = []
for i in range(2, Pn):
    gcd = euclid(Pn, i)
    if gcd == 1:
        key.append(i)
# Select an encryption key from the above list
e = int(313)

# Obtain inverse of encryption key in Z_Pn
r, d = exteuclid(Pn, e)
if r == 1:
    d = int(d)
    print("Decryption key is: ", d)
else:
    print("Multiplicative inverse for the given encryption key does not exist. Choose a different encryption key.")

# Enter the message to be sent
M = 19070

# Signature is created by Alice
S = (M**d) % n

# Alice sends M and S both to Bob
# Bob generates message M1 using the signature S, Alice's public key e, and product n.
M1 = (S**e) % n

# If M = M1, only then Bob accepts the message sent by Alice.
if M == M1:
    print("As M = M1, Accept the message sent by Alice")
else:
    print("As M not equal to M1, Do not accept the message sent by Alice")

        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return SS.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(SS.codes)}."
