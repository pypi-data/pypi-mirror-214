from simple_file_cryptography.crypto_utility import generate_key, decrypt_file, encrypt_file
import argparse
import simple_file_cryptography.gui as gui

def main():
    parser = argparse.ArgumentParser(
        prog='Simple file cryptography',
        description='Encrypts and decrypts files.')

    parser.add_argument(
        "-m",
        "--mode",
        choices=["encrypt", "decrypt"],
        help="Choose whether you want to encrypt or decrypt a file.")

    parser.add_argument(
        "-kg",
        "--keygen",
        help="Generate a key.",
        action='store_true',
    )
    parser.add_argument(
        "-k",
        "--key",
        help="Key used for encryption/decryption. Key should be in hexadecimal."
        + "String should be of length 32, 48 or 64 characters long " +
        "(representing 128, 192 and 256 bit key respectively).")
    parser.add_argument(
        "-i",
        "--input",
        help=
        "Program will do operation (encryption or decryption) on this file. " +
        "This file contains input for this program.")
    parser.add_argument(
        "-o",
        "--output",
        help=
        "Results of your operation (encryption or decryption) will be written to this file. "
        + "This file contains output of this program.")
    parser.add_argument("-g",
                        "--gui",
                        action='store_true',
                        help="Show graphical user interface instead.")

    args = parser.parse_args()

    if args.gui:
        gui.gui_procedure()
        return

    key = generate_key().hex() if args.keygen else args.key

    if args.keygen:
        print(key)

    if key == None:
        print("You must provide a key.")
        return

    if len(key) > 64 and len(key) < 32:
        print("Key must be 32, 48 or 64 characters long.")
        return

    if args.mode == "encrypt" and args.input != None and args.output != None:
        print("Encrypting")
        encrypt_file(args.input, args.output, key)

    if args.mode == "decrypt" and args.input != None and args.output != None:
        print("Decrypting")
        decrypt_file(args.input, args.output, key)


if __name__ == "__main__":
    main()
