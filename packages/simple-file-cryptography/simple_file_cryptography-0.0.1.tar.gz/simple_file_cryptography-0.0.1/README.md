# simple-file-cryptography

[![PyPI - Version](https://img.shields.io/pypi/v/simple-file-cryptography.svg)](https://pypi.org/project/simple-file-cryptography)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-file-cryptography.svg)](https://pypi.org/project/simple-file-cryptography)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Examples](#examples)

## Installation

```console
pip install simple-file-cryptography
```

## License

`simple-file-cryptography` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.


## Examples


Activate the GUI:
```sh
python -m "simple_file_cryptography" -g
```


Generate a key:
```sh
python -m "simple_file_cryptography" -kg
```


Encrypt a file:
```sh
python -m "simple_file_cryptography" -m encrypt -k "c2ebbce1532c050164ff9edc28fa4ee5" -i "some_file.txt" -o "some_file.txt.enc"
```

Encrypt a file with automatically generated key (key will be printed out):
```sh
python -m "simple_file_cryptography" -m encrypt -kg -i "some_file.txt" -o "some_file.txt.enc"
```


Decrypt a file:
```sh
python -m "simple_file_cryptography" -m decrypt -k "c2ebbce1532c050164ff9edc28fa4ee5" -i "some_file.txt.enc" -o "some_file.txt"
```

To encrypt or decrypt with Python code, use functions provided in `simple_file_cryptography.crypto_utility` module.
```py
from simple_file_cryptography.crypto_utility import decrypt_file, encrypt_file, generate_key

key = generate_key()
encrypt_file("in.txt", "in.txt.enc", key)
decrypt_file("in.txt.enc", "out.txt", key)
```