from lib.gettag import *
import json
from lib.get_password import *
import getpass
import os

# Asegurarse de que la carpeta config existe
config_folder = 'config'
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

def load_config(tag):
    try:
        with open(os.path.join(config_folder,f"{tag}_config.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_config(tag, config):
    with open(os.path.join(config_folder,f"{tag}_config.json"), "w") as file:
        json.dump(config, file)

def input_with_default(prompt, default=True):
    response = input(prompt)
    if response == "":
        return default
    else:
        try:
            return bool(int(response))
        except ValueError:
            return default

def update_config(config):
    for key in config:
        if key != "tag":
            if key == "use_chars":
                config[key] = {k: input_with_default(f"¿Incluir {k}? 0-No, 1-Sí (default=1): ") for k in config[key]}
            else:
                if key == "private_key":
                    masked_private_key = config[key][0] + "*" * (len(config[key]) - 3) + config[key][-2] + config[key][-1]
                    print(f"private_key actual es: {masked_private_key}")
                    change_key = getpass.getpass("¿Desea cambiarla? (y/n): ")
                    if change_key.lower() == "y":
                        config[key] = getpass.getpass("Nuevo valor para private_key: ")
                elif key == "password_length":
                    new_value = input(f"{key} actual es {config[key]}. ¿Nuevo valor? (Presione Enter para mantener): ")
                    if new_value:
                        config[key] = int(new_value)
                else:
                    new_value = input(f"{key} actual es {config[key]}. ¿Nuevo valor? (Presione Enter para mantener): ")
                    if new_value:
                        config[key] = new_value
    return config

def print_config_with_masked_private_key(config):
    config_for_display = config.copy()
    if "private_key" in config_for_display and len(config_for_display["private_key"]) > 2:
        config_for_display["private_key"] = config_for_display["private_key"][0] + "*" * (len(config_for_display["private_key"]) - 3) + config_for_display["private_key"][-2] + config_for_display["private_key"][-1]
    elif "private_key" in config_for_display:
        config_for_display["private_key"] = "*" * len(config_for_display["private_key"])
    print(json.dumps(config_for_display, indent=4))

if __name__ == "__main__":
    url = input("url : \n")
    tag = (get_urltag(url))
    print("tag:" , tag)
    #tag = input("Introduce el tag: ")
    config = load_config(tag)
    
    if config:
        print("Configuración encontrada. Cargando...")
        print_config_with_masked_private_key(config)
        change = input("¿Desea cambiar la configuración actual? (y/n): ")
        if change.lower() == "y":
            config = update_config(config)
            save_config(tag, config)
    else:
        print("No se encontró configuración. Creando una nueva.")
        private_key = getpass.getpass("Introduce la private_key: ")
        use_chars = {
            "lowercase": input_with_default("¿Incluir minúsculas? 0-No, 1-Sí (default=1): ", default=True),
            "uppercase": input_with_default("¿Incluir mayúsculas? 0-No, 1-Sí (default=1): ", default=True),
            "numbers": input_with_default("¿Incluir números? 0-No, 1-Sí (default=1): ", default=True),
            "symbols": input_with_default("¿Incluir símbolos? 0-No, 1-Sí (default=1): ", default=True)
        }
        password_length = int(input("Introduce la longitud de la contraseña: "))
        config = {
            "tag": tag,
            "private_key": private_key,
            "use_chars": use_chars,
            "password_length": password_length
        }
        save_config(tag, config)

    # Solicitar la master_key antes de generar la contraseña
    master_key = getpass.getpass("Introduce la master_key: ")
    password = get_password(tag, config["private_key"], master_key, config["use_chars"], config["password_length"])
    print(f"Contraseña generada: {password}")