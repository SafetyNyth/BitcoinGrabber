# BTC hack v2
# Made by David Gilbert
# https://github.com/davidmgilbert/btc-hack
# https://www.davidmgilbert.com

#!/usr/bin/python3

import hashlib
import os
import hashlib
import binascii
import requests
import ecdsa
import base58
import webbrowser
import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path
import json

def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def private_key_to_WIF(private_key):
    var80 = "80" + str(private_key) 
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')

def private_key_to_public_key(private_key):
    sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve = ecdsa.SECP256k1)
    return ('04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))

def public_key_to_address(public_key):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0; val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod (n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])

def get_balance(address):
    #time.sleep(0.2) #This is to avoid over-using the API and keep the program running indefinately. (Un-comment if exceeding requests)
    try:
        response = requests.get("https://sochain.com/api/v2/address/BTC/" + str(address))
        return float(response.json()['data']['balance']) 
    except:
        return -1

SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'theme': sg.theme()}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'theme': '-THEME-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window


def create_main_window(settings):
    sg.theme(settings['theme'])

    menu_def = [['&Menu', ['&Settings', 'E&xit']]]

    layout = [[sg.Menu(menu_def)],
              [sg.Text('Number of addresses tried so far ... ', size=(30,1), font=('Comic sans ms', 10)),
               sg.Text('', size=(30,1), font=('Comic sans ms', 10), key='_TRIES_')],
              [sg.Text('Number of positive balances ... ', size=(30,1), font=('Comic sans ms', 10)),
               sg.Text('', size=(30,1), font=('Comic sans ms', 10), key='_WINS_')],
              [sg.Text('')],
              [sg.Output(size=(87, 20), font=('Comic sans ms', 8), key='out')],
              [sg.Button('Start/Stop',  font=('Comic sans ms', 10))]]

    return sg.Window('BTC Hack v2',
                     layout=layout,
                     default_element_size=(9,1))



def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    process = False
    attempts = 0
    successes = 0
    while True:
        if window is None:
            window = create_main_window(settings)
        event, values = window.Read(timeout=10)
        window.Element('_TRIES_').Update(str(attempts))
        window.Element('_WINS_').Update(str(successes))
        if event in (None, 'Exit'):
            break
        elif event == 'Start/Stop':
            process = not process
            attempts = attempts + 1
        if process:
            private_key = generate_private_key()
            public_key = private_key_to_public_key(private_key)
            address = public_key_to_address(public_key)
            data = (private_key, address)
            balance = get_balance(data[1])
            attempts = attempts + 1
            private_key = data[0]
            address = data[1]
            if (balance == 0.00000000):
                print("Address: " + "{:<34}".format(str(address)) + "\n" +
                   "Private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "Public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "Balance: " + str(balance) + "\n\n")
            elif (balance > 0.00000000):
                successes = successes + 1
                file = open("found.txt","a")
                file.write("Address: " + str(address) + "\n" +
                   "Private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "Public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "Balance: " + str(balance) + "\n\n")
                file.close()
                print("Address: " + "{:<34}".format(str(address)) + "\n" +
                   "Private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "Public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "Balance: " + str(balance) + "\n\n")
            
        elif event == 'Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)

    
    window.Close()
    
main()


