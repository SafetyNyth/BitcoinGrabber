# Bitcoin Brute Forcer

An automated bitcoin wallet collider that brute forces random wallet addresses by checking their balance in real-time.

# Like This Project? Give It A Star or consider donating!

[![](https://img.shields.io/github/stars/DavidMGilbert/btc-hack.svg)](https://github.com/davidMGilbert/btc-hack)
Bitcoin Wallet Address: 1LKKJE62ygo2c9K2Xc8GxuGwpVDnvyRFRD

# Dependencies

<a href="https://www.python.org/downloads/">Python 3.6</a> or higher

btc-hack.py will try to automatically install the required modules if they are not present. Should that fail, you can find the required modules listed in the <a href="/requirements.txt">requirements.txt<a/>

Minimum <a href="#memory-consumption">RAM requirements</a>

# Installation

```
$ git clone https://github.com/DavidMGilbert/btc-hack.git btc-hack
```

# Quick Start

```
$ python3 btc-hack.py
```

# Proof Of Concept

A private key is a secret number that allows Bitcoins to be spent. If a wallet has Bitcoins in it, then the private key will allow a person to control the wallet and spend whatever balance the wallet has. So this program attempts to find Bitcoin private keys that correlate to wallets with positive balances. However, because it is impossible to know which private keys control wallets with money and which private keys control empty wallets, we have to randomly look at every possible private key that exists and hope to find one that has a balance.

This program is essentially a brute forcing algorithm. It continuously generates random Bitcoin private keys, converts the private keys into their respective wallet addresses, then checks the balance of the addresses. If a wallet with a balance is found, then the private key, public key and wallet address are saved to the text file `found.txt` on the user's hard drive. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence.

# How It Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys using the `starkbank-ecdsa` Python module. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii` and `hashlib` standard libraries.

The generated address is searched using an online api, and if it is found that the address has a balance, then the private key, public key and wallet address are saved to the text file `found.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `multiprocessing.Process()` function in order to make concurrent calculations. Sadly this is limited at present due to api restrictions of 300 queries per minute.

# Efficiency

It takes `0.0032457721` seconds for this progam to brute force a __single__ Bitcoin address.

However, through `multiprocessing.Process()` a concurrent process is created for every CPU your computer has. So this program can brute force addresses at a speed of `0.0032457721 ÷ cpu_count()` seconds.

# API FAQ

Currently, the program runs and queries the sochain.com api. As this api allows for upto 300 queries per minute for free, it seemed like a really good choice allowing you to test approximately 18,000 adresses per hour, 432,000 addresses per 24 hours or 3,000,000 addresses per week!

# Expected Output

Every time this program checks the balance of a generated address, it will print the result to the user. If an empty wallet is found, then the wallet address will be printed to the terminal. An example is:

>1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45 : 0.0

However, if a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `found.txt`. An example is:

>address: 1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45<br/>
>private key: 5A4F3F1CAB44848B2C2C515AE74E9CC487A9982C9DD695810230EA48B1DCEADD<br/>
>WIF private key: 5JW4RCAXDbocFLK9bxqw5cbQwuSn86fpbmz2HhT9nvKMTh68hjm<br/>
>public key: 04393B30BC950F358326062FF28D194A5B28751C1FF2562C02CA4DFB2A864DE63280CC140D0D540EA1A5711D1E519C842684F42445C41CB501B7EA00361699C320<br/>
>balance: 0.0001456<br/>

# Memory Consumption

This program uses approximately 2GB of RAM per CPU. Because this program can use multi-processing, some data gets shared between threads making it difficult to accurately measure RAM usage.

The memory consumption stack trace was made by using <a href="https://pypi.org/project/memory-profiler/">mprof</a> to monitor this program brute force 10,000 addresses on a 4 logical processor machine with 8GB of RAM. As a result, 4 child processes were created, each consuming 2100MiB of RAM (~2GB).

# TODO

- [X] Find a faster FREE API with greater allowances.


<a href="https://github.com/purpyl-media/btc-hack/issues">Create an issue</a> so I can add more stuff to improve
