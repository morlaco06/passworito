from cryptography.fernet import Fernet
import json
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode


config_folder = 'config'
def generar_clave(private_key, tag):
    """
    Deriva una clave de cifrado segura a partir de la private_key usando PBKDF2.
    """
    # Salt debería ser único para cada usuario, podría guardarse junto con el archivo de configuración o generarse de alguna manera relacionada con el usuario.
    salt = tag.encode()
    # Considera almacenar el salt para poder descifrar después, o generar de manera que se pueda recuperar o conocer de antemano.
    
    # Parámetros para PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Tamaño de la clave derivada en bytes. Fernet espera claves de 32 bytes.
        salt=salt,
        iterations=100000,  # Número de iteraciones. Ajusta según la seguridad requerida y la capacidad de cómputo.
        backend=default_backend()
    )
    
    # Derivar la clave
    clave = kdf.derive(private_key.encode())  # La private_key necesita ser bytes, por eso usamos .encode()
    
    # Fernet espera la clave en formato URL-safe base64 encoded, así que la convertimos
    clave_fernet = urlsafe_b64encode(clave)
    #print("clave_fernet: " ,clave_fernet)
    return clave_fernet    


def cargar_configuracion(tag, private_key):
    archivo_config = f'{tag}.cfg'
    try:
        with open(os.path.join(config_folder, archivo_config), 'rb') as file:
            datos_cifrados = file.read()
            fernet = Fernet(generar_clave(private_key,tag))
            #print(f'{fernet}')
            datos_descifrados = fernet.decrypt(datos_cifrados)
            #print("datos descifrados :" ,datos_descifrados)
            configuracion = json.loads(datos_descifrados)
            
            return configuracion

    except (FileNotFoundError, Exception):
        return None

def guardar_configuracion(tag, private_key, master_key, use_char, password_length):
    configuracion = {
        'tag': tag,   
        'private_key': private_key,
        'use_char': use_char,
        'password_length': password_length,
    }
    datos_cifrados = Fernet(generar_clave(private_key,tag)).encrypt(json.dumps(configuracion).encode())
    archivo_config = f'{tag}.cfg'
    with open(os.path.join(config_folder, archivo_config), 'wb') as file:
        file.write(datos_cifrados)