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

if _name_ == "_main_":
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

if _name_ == "_main_":
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

if _name_ == "_main_":
    input_str = input("Enter a string to hash: ")
    hash_value = sha1_hash(input_str)
    print(f"SHA-1 hash of '{input_str}': {hash_value}")
        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return SS.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(SS.codes)}."
