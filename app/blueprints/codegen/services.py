"""
Code Generator Service — generate crypto implementation code in Python, JS, C++.
"""

TEMPLATES = {
    "caesar": {
        "name": "Caesar Cipher",
        "python": '''# Caesar Cipher — Python Implementation
def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Enkripsi teks menggunakan Caesar Cipher."""
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Dekripsi teks menggunakan Caesar Cipher."""
    return caesar_encrypt(ciphertext, -shift)

# Contoh penggunaan:
plaintext = "HELLO WORLD"
shift = 3
encrypted = caesar_encrypt(plaintext, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"Plaintext : {plaintext}")
print(f"Encrypted : {encrypted}")
print(f"Decrypted : {decrypted}")
''',
        "javascript": '''// Caesar Cipher — JavaScript Implementation
function caesarEncrypt(plaintext, shift) {
    return plaintext.split('').map(ch => {
        if (/[a-zA-Z]/.test(ch)) {
            const base = ch === ch.toUpperCase() ? 65 : 97;
            return String.fromCharCode((ch.charCodeAt(0) - base + shift) % 26 + base);
        }
        return ch;
    }).join('');
}

function caesarDecrypt(ciphertext, shift) {
    return caesarEncrypt(ciphertext, 26 - (shift % 26));
}

// Contoh penggunaan:
const plaintext = "HELLO WORLD";
const shift = 3;
const encrypted = caesarEncrypt(plaintext, shift);
const decrypted = caesarDecrypt(encrypted, shift);
console.log(`Plaintext : ${plaintext}`);
console.log(`Encrypted : ${encrypted}`);
console.log(`Decrypted : ${decrypted}`);
''',
        "cpp": '''// Caesar Cipher — C++ Implementation
#include <iostream>
#include <string>
using namespace std;

string caesarEncrypt(const string& plaintext, int shift) {
    string result = plaintext;
    for (char& ch : result) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            ch = (ch - base + shift) % 26 + base;
        }
    }
    return result;
}

string caesarDecrypt(const string& ciphertext, int shift) {
    return caesarEncrypt(ciphertext, 26 - (shift % 26));
}

int main() {
    string plaintext = "HELLO WORLD";
    int shift = 3;
    string encrypted = caesarEncrypt(plaintext, shift);
    string decrypted = caesarDecrypt(encrypted, shift);
    cout << "Plaintext : " << plaintext << endl;
    cout << "Encrypted : " << encrypted << endl;
    cout << "Decrypted : " << decrypted << endl;
    return 0;
}
'''
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "python": '''# Vigenère Cipher — Python Implementation
def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Enkripsi teks menggunakan Vigenère Cipher."""
    key = key.upper()
    result = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Dekripsi teks menggunakan Vigenère Cipher."""
    key = key.upper()
    result = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('A')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)

# Contoh penggunaan:
plaintext = "HELLO WORLD"
key = "SECRET"
encrypted = vigenere_encrypt(plaintext, key)
decrypted = vigenere_decrypt(encrypted, key)
print(f"Plaintext : {plaintext}")
print(f"Key       : {key}")
print(f"Encrypted : {encrypted}")
print(f"Decrypted : {decrypted}")
''',
        "javascript": '''// Vigenère Cipher — JavaScript Implementation
function vigenereEncrypt(plaintext, key) {
    key = key.toUpperCase();
    let ki = 0;
    return plaintext.split('').map(ch => {
        if (/[a-zA-Z]/.test(ch)) {
            const base = ch === ch.toUpperCase() ? 65 : 97;
            const shift = key.charCodeAt(ki % key.length) - 65;
            ki++;
            return String.fromCharCode((ch.charCodeAt(0) - base + shift) % 26 + base);
        }
        return ch;
    }).join('');
}

function vigenereDecrypt(ciphertext, key) {
    key = key.toUpperCase();
    let ki = 0;
    return ciphertext.split('').map(ch => {
        if (/[a-zA-Z]/.test(ch)) {
            const base = ch === ch.toUpperCase() ? 65 : 97;
            const shift = key.charCodeAt(ki % key.length) - 65;
            ki++;
            return String.fromCharCode((ch.charCodeAt(0) - base - shift + 26) % 26 + base);
        }
        return ch;
    }).join('');
}

// Contoh penggunaan:
const plaintext = "HELLO WORLD";
const key = "SECRET";
console.log("Encrypted:", vigenereEncrypt(plaintext, key));
console.log("Decrypted:", vigenereDecrypt(vigenereEncrypt(plaintext, key), key));
''',
        "cpp": '''// Vigenère Cipher — C++ Implementation
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

string vigenereEncrypt(const string& plaintext, const string& key) {
    string result;
    int ki = 0;
    for (char ch : plaintext) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            int shift = toupper(key[ki % key.size()]) - 'A';
            result += (ch - base + shift) % 26 + base;
            ki++;
        } else {
            result += ch;
        }
    }
    return result;
}

string vigenereDecrypt(const string& ciphertext, const string& key) {
    string result;
    int ki = 0;
    for (char ch : ciphertext) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            int shift = toupper(key[ki % key.size()]) - 'A';
            result += (ch - base - shift + 26) % 26 + base;
            ki++;
        } else {
            result += ch;
        }
    }
    return result;
}

int main() {
    string text = "HELLO WORLD", key = "SECRET";
    string enc = vigenereEncrypt(text, key);
    cout << "Encrypted: " << enc << endl;
    cout << "Decrypted: " << vigenereDecrypt(enc, key) << endl;
    return 0;
}
'''
    },
    "aes": {
        "name": "AES Encryption",
        "python": '''# AES Encryption — Python Implementation (menggunakan library cryptography)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def aes_encrypt(plaintext: bytes, key: bytes) -> tuple:
    """Enkripsi data menggunakan AES-CBC."""
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv, ciphertext

def aes_decrypt(iv: bytes, ciphertext: bytes, key: bytes) -> bytes:
    """Dekripsi data menggunakan AES-CBC."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()

# Contoh penggunaan:
key = os.urandom(32)  # AES-256
plaintext = b"Hello, World! Ini adalah pesan rahasia."
iv, encrypted = aes_encrypt(plaintext, key)
decrypted = aes_decrypt(iv, encrypted, key)
print(f"Plaintext  : {plaintext}")
print(f"Key (hex)  : {key.hex()}")
print(f"IV (hex)   : {iv.hex()}")
print(f"Encrypted  : {encrypted.hex()}")
print(f"Decrypted  : {decrypted}")
''',
        "javascript": '''// AES Encryption — JavaScript (Web Crypto API)
async function aesEncrypt(plaintext, key) {
    const enc = new TextEncoder();
    const iv = crypto.getRandomValues(new Uint8Array(12));

    const cryptoKey = await crypto.subtle.importKey(
        'raw', key, { name: 'AES-GCM' }, false, ['encrypt']
    );

    const ciphertext = await crypto.subtle.encrypt(
        { name: 'AES-GCM', iv }, cryptoKey, enc.encode(plaintext)
    );

    return { iv, ciphertext: new Uint8Array(ciphertext) };
}

async function aesDecrypt(iv, ciphertext, key) {
    const cryptoKey = await crypto.subtle.importKey(
        'raw', key, { name: 'AES-GCM' }, false, ['decrypt']
    );

    const decrypted = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv }, cryptoKey, ciphertext
    );

    return new TextDecoder().decode(decrypted);
}

// Contoh penggunaan:
(async () => {
    const key = crypto.getRandomValues(new Uint8Array(32)); // AES-256
    const plaintext = "Hello, World!";
    const { iv, ciphertext } = await aesEncrypt(plaintext, key);
    const decrypted = await aesDecrypt(iv, ciphertext, key);
    console.log("Decrypted:", decrypted);
})();
''',
        "cpp": '''// AES Encryption — C++ (menggunakan OpenSSL)
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

vector<unsigned char> aesEncrypt(
    const vector<unsigned char>& plaintext,
    const vector<unsigned char>& key,
    vector<unsigned char>& iv
) {
    iv.resize(16);
    RAND_bytes(iv.data(), 16);

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key.data(), iv.data());

    vector<unsigned char> ciphertext(plaintext.size() + 16);
    int len, ciphertext_len;

    EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size());
    ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len);
    ciphertext_len += len;
    ciphertext.resize(ciphertext_len);

    EVP_CIPHER_CTX_free(ctx);
    return ciphertext;
}

int main() {
    vector<unsigned char> key(32);
    RAND_bytes(key.data(), 32);

    string msg = "Hello, World!";
    vector<unsigned char> plaintext(msg.begin(), msg.end());
    vector<unsigned char> iv;

    auto encrypted = aesEncrypt(plaintext, key, iv);
    cout << "Encrypted " << encrypted.size() << " bytes" << endl;
    return 0;
}
'''
    },
    "rsa": {
        "name": "RSA Encryption",
        "python": '''# RSA — Python Implementation (educational)
import math
import random

def is_prime(n, k=20):
    """Miller-Rabin primality test."""
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def generate_prime(bits=32):
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if is_prime(n): return n

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def rsa_keygen(bits=32):
    p, q = generate_prime(bits), generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    return (e, n), (d, n), p, q

def rsa_encrypt(message: str, e: int, n: int) -> list:
    return [pow(ord(ch), e, n) for ch in message]

def rsa_decrypt(ciphertext: list, d: int, n: int) -> str:
    return ''.join(chr(pow(c, d, n)) for c in ciphertext)

# Contoh penggunaan:
pub, priv, p, q = rsa_keygen(16)
msg = "HELLO"
enc = rsa_encrypt(msg, *pub)
dec = rsa_decrypt(enc, *priv)
print(f"Public Key : e={pub[0]}, n={pub[1]}")
print(f"Private Key: d={priv[0]}, n={priv[1]}")
print(f"Encrypted  : {enc}")
print(f"Decrypted  : {dec}")
''',
        "javascript": '''// RSA — JavaScript Implementation (educational, small keys)
function modPow(base, exp, mod) {
    let result = 1n;
    base = BigInt(base) % BigInt(mod);
    exp = BigInt(exp);
    mod = BigInt(mod);
    while (exp > 0n) {
        if (exp % 2n === 1n) result = (result * base) % mod;
        exp /= 2n;
        base = (base * base) % mod;
    }
    return Number(result);
}

function rsaEncrypt(message, e, n) {
    return [...message].map(ch => modPow(ch.charCodeAt(0), e, n));
}

function rsaDecrypt(ciphertext, d, n) {
    return ciphertext.map(c => String.fromCharCode(modPow(c, d, n))).join('');
}

// Contoh penggunaan (dengan kunci kecil untuk demo):
const e = 65537, n = 3233, d = 2753;
const msg = "HI";
const enc = rsaEncrypt(msg, e, n);
const dec = rsaDecrypt(enc, d, n);
console.log("Encrypted:", enc);
console.log("Decrypted:", dec);
''',
        "cpp": '''// RSA — C++ Implementation (educational)
#include <iostream>
#include <vector>
#include <string>
using namespace std;

long long modPow(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = (__int128)result * base % mod;
        exp >>= 1;
        base = (__int128)base * base % mod;
    }
    return result;
}

vector<long long> rsaEncrypt(const string& msg, long long e, long long n) {
    vector<long long> cipher;
    for (char ch : msg)
        cipher.push_back(modPow(ch, e, n));
    return cipher;
}

string rsaDecrypt(const vector<long long>& cipher, long long d, long long n) {
    string result;
    for (long long c : cipher)
        result += (char)modPow(c, d, n);
    return result;
}

int main() {
    long long e = 65537, n = 3233, d = 2753;
    string msg = "HI";
    auto enc = rsaEncrypt(msg, e, n);
    auto dec = rsaDecrypt(enc, d, n);
    cout << "Decrypted: " << dec << endl;
    return 0;
}
'''
    },
    "sha256": {
        "name": "SHA-256 Hash",
        "python": '''# SHA-256 — Python Implementation
import hashlib

def sha256_hash(message: str) -> str:
    """Hitung hash SHA-256 dari string."""
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

# Contoh penggunaan:
messages = ["Hello, World!", "CipherLab", "password123"]
for msg in messages:
    digest = sha256_hash(msg)
    print(f"SHA-256(\\"{msg}\\") = {digest}")
''',
        "javascript": '''// SHA-256 — JavaScript (Web Crypto API)
async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Contoh penggunaan:
(async () => {
    const messages = ["Hello, World!", "CipherLab", "password123"];
    for (const msg of messages) {
        const hash = await sha256(msg);
        console.log(`SHA-256("${msg}") = ${hash}`);
    }
})();
''',
        "cpp": '''// SHA-256 — C++ (menggunakan OpenSSL)
#include <openssl/sha.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
using namespace std;

string sha256(const string& input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)input.c_str(), input.size(), hash);
    stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
        ss << hex << setfill('0') << setw(2) << (int)hash[i];
    return ss.str();
}

int main() {
    string messages[] = {"Hello, World!", "CipherLab", "password123"};
    for (const auto& msg : messages)
        cout << "SHA-256(\\"" << msg << "\\") = " << sha256(msg) << endl;
    return 0;
}
'''
    },
    "affine": {
        "name": "Affine Cipher",
        "python": '''# Affine Cipher — Python Implementation
import math

def mod_inverse(a: int, m: int) -> int:
    """Menghitung invers modular menggunakan Extended Euclidean."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1: raise ValueError(f"{a} tidak memiliki invers mod {m}")
    return x % m

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """E(x) = (ax + b) mod 26"""
    if math.gcd(a, 26) != 1:
        raise ValueError(f"a={a} harus koprima dengan 26")
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch) - base
            result.append(chr((a * x + b) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """D(y) = a_inv * (y - b) mod 26"""
    a_inv = mod_inverse(a, 26)
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            y = ord(ch) - base
            result.append(chr((a_inv * (y - b)) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

# Contoh penggunaan:
text = "HELLO WORLD"
a, b = 5, 8
enc = affine_encrypt(text, a, b)
dec = affine_decrypt(enc, a, b)
print(f"E(x) = ({a}x + {b}) mod 26")
print(f"Encrypted: {enc}")
print(f"Decrypted: {dec}")
''',
        "javascript": '''// Affine Cipher — JavaScript Implementation
function modInverse(a, m) {
    let [old_r, r] = [a, m], [old_s, s] = [1, 0];
    while (r !== 0) {
        const q = Math.floor(old_r / r);
        [old_r, r] = [r, old_r - q * r];
        [old_s, s] = [s, old_s - q * s];
    }
    return ((old_s % m) + m) % m;
}

function affineEncrypt(text, a, b) {
    return text.split('').map(ch => {
        if (/[a-zA-Z]/.test(ch)) {
            const base = ch === ch.toUpperCase() ? 65 : 97;
            const x = ch.charCodeAt(0) - base;
            return String.fromCharCode((a * x + b) % 26 + base);
        }
        return ch;
    }).join('');
}

function affineDecrypt(text, a, b) {
    const aInv = modInverse(a, 26);
    return text.split('').map(ch => {
        if (/[a-zA-Z]/.test(ch)) {
            const base = ch === ch.toUpperCase() ? 65 : 97;
            const y = ch.charCodeAt(0) - base;
            return String.fromCharCode(((aInv * (y - b)) % 26 + 26) % 26 + base);
        }
        return ch;
    }).join('');
}

const text = "HELLO WORLD";
console.log("Encrypted:", affineEncrypt(text, 5, 8));
console.log("Decrypted:", affineDecrypt(affineEncrypt(text, 5, 8), 5, 8));
''',
        "cpp": '''// Affine Cipher — C++ Implementation
#include <iostream>
#include <string>
using namespace std;

int modInverse(int a, int m) {
    int g = m, x = 0, y = 1;
    int a0 = a;
    while (a0 != 0) {
        int q = g / a0;
        int t = g - q * a0; g = a0; a0 = t;
        t = x - q * y; x = y; y = t;
    }
    return (x % m + m) % m;
}

string affineEncrypt(const string& text, int a, int b) {
    string result;
    for (char ch : text) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            result += (a * (ch - base) + b) % 26 + base;
        } else result += ch;
    }
    return result;
}

string affineDecrypt(const string& text, int a, int b) {
    int aInv = modInverse(a, 26);
    string result;
    for (char ch : text) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            result += ((aInv * ((ch - base) - b + 26)) % 26 + 26) % 26 + base;
        } else result += ch;
    }
    return result;
}

int main() {
    string text = "HELLO WORLD";
    cout << "Encrypted: " << affineEncrypt(text, 5, 8) << endl;
    cout << "Decrypted: " << affineDecrypt(affineEncrypt(text, 5, 8), 5, 8) << endl;
    return 0;
}
'''
    }
}


def get_available_algorithms() -> list:
    return [{"id": k, "name": v["name"]} for k, v in TEMPLATES.items()]


def generate_code(algorithm: str, language: str) -> dict:
    """Generate code for a specific algorithm and language."""
    if algorithm not in TEMPLATES:
        return {"error": f"Algoritma '{algorithm}' tidak tersedia."}

    template = TEMPLATES[algorithm]
    lang_map = {"python": "python", "javascript": "javascript", "cpp": "cpp"}
    lang_key = lang_map.get(language.lower())

    if not lang_key or lang_key not in template:
        return {"error": f"Bahasa '{language}' tidak tersedia untuk {template['name']}."}

    return {
        "algorithm": template["name"],
        "language": language,
        "code": template[lang_key],
        "available_languages": list(lang_map.keys())
    }
