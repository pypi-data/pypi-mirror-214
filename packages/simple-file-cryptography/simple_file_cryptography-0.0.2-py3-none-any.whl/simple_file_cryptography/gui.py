import PySimpleGUI as sg
from simple_file_cryptography.mode import Mode
from simple_file_cryptography.crypto_utility import decrypt_file, encrypt_file, generate_key
from os.path import basename, dirname, abspath, join


def select_mode() -> Mode:
    layout = [[sg.Text("Select mode")],
              [
                  sg.Radio('Encrypt', "mode1", key="encrypt"),
                  sg.Radio('Decrypt', "mode1", key="decrypt", default=True)
              ], [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window('Simple file cryptography', layout)
    result = window.read()
    if result != None:
        _, values = result
        window.close()
        return Mode.ENCRYPT if values['encrypt'] else Mode.DECRYPT

    return Mode.DECRYPT


def get_input_file(mode: Mode) -> str:
    layout = [[sg.Text(f"Select which file to {mode}:")],
              [sg.Input(key='input'), sg.FileBrowse()],
              [sg.Button('Ok'), sg.Button('Cancel')]]
    window = sg.Window(f'Which file to {mode}', layout)
    result = window.read()
    if result != None:
        _, values = result
        return values['input']
    return ""


def encrypt_gui(key: str, input_file_path: str, output_file_path: str):
    layout = [[sg.Text("Enter the key (in hexadecimal):")],
              [sg.Input(key='key', default_text=key)],
              [sg.Text("Select where to save encrypted file:")],
              [
                  sg.Input(key='output', default_text=output_file_path),
                  sg.FileSaveAs()
              ], [sg.Button('Ok'), sg.Button('Cancel')]]
    window = sg.Window('Encrypt a file', layout)
    result = window.read()
    if result != None:
        _, values = result
        encrypt_file(input_file_path, values['output'], values['key'])


def key_input() -> str:
    layout = [[sg.Text("Do you want to automatically generate a key?")],
              [
                  sg.Radio('Yes', "mode1", key="yes", default=True),
                  sg.Radio('No', "mode1", key="no"),
              ], [sg.Button('Ok'), sg.Button('Cancel')]]
    window = sg.Window('Generate a key', layout)
    result = window.read()
    if result != None:
        _, values = result
        window.close()
        if values['yes']:
            return generate_key().hex()
    return ""


def decrypt_gui(input_file_path: str, output_file_path: str):
    layout = [[sg.Text("Enter the key (in hexadecimal):")],
              [sg.Input(key='key')],
              [sg.Text("Select where to save decrypted file:")],
              [
                  sg.Input(key='output', default_text=output_file_path),
                  sg.FileSaveAs()
              ], [sg.Button('Ok'), sg.Button('Cancel')]]
    window = sg.Window('Encrypt a file', layout)
    result = window.read()
    if result != None:
        _, values = result
        window.close()
        decrypt_file(input_file_path, values['output'], values['key'])


def gui_procedure():
    mode = select_mode()
    if mode == Mode.ENCRYPT:
        key_result = key_input()
        input_file_path = get_input_file(mode)
        directory = dirname(input_file_path)
        file_name = basename(input_file_path)

        encrypt_gui(key_result, input_file_path,
                    join(abspath(directory), f"{file_name}.enc"))
    else:
        input_file_path = get_input_file(mode)
        directory = dirname(input_file_path)
        file_name = basename(input_file_path)[0:-4]

        decrypt_gui(input_file_path, join(abspath(directory), file_name))
