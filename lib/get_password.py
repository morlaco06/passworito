import hashlib
import random

import hashlib
import random

def get_password(tag, private_key, master_key, use_chars, password_length):
    # Concatenar los valores
    concatenated_values = f"{tag}{private_key}{master_key}"
    
    # Crear el hash SHA3-512
    hash_object = hashlib.sha3_512(concatenated_values.encode())
    hash_hex = hash_object.hexdigest()
    
    # Definir los conjuntos de caracteres posibles
    char_sets = {
        "lowercase": "abcdefghijklmnopqrstuvwxyz",
        "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "numbers": "0123456789",
        "symbols": "!@#$%^&*()"
    }
    
    # Construir el conjunto de caracteres a usar basado en el argumento use_chars
    characters = ""
    for char_type, should_use in use_chars.items():
        if should_use:
            characters += char_sets.get(char_type, "")
    
    if not characters:
        raise ValueError("Debe seleccionar al menos un tipo de caracter para generar la contraseña.")
    
    # Usar el hash como semilla
    random.seed(hash_hex)
    
    # Inicializar la contraseña
    password = ''
    
    # Intentar generar una contraseña que cumpla con los requisitos
    while True:
        password = ''.join(random.choice(characters) for _ in range(password_length))
        
        # Verificar si la contraseña tiene al menos un número
        if any(char.isdigit() for char in password):
            break  # La contraseña es válida
        else:
            # Sustituir el primer carácter (o cualquier otro) por un número aleatorio
            random_number = random.choice(char_sets["numbers"])
            # Aquí se elige sustituir el primer carácter, pero se puede cambiar
            password = random_number + password[1:]
            break  # Asumimos que con esta modificación, la contraseña es válida
    
    return password

# Ejemplo de uso
if __name__ == "__main__":
    tag = "exampleTag"
    private_key = "privateKey123"
    master_key = "masterKey456"
    use_chars = {
        "lowercase": True,
        "uppercase": True,
        "numbers": True,  # Aunque se indique True, esta comprobación asegura que siempre habrá un número
        "symbols": True
    }
    password_length = 16  # Longitud deseada de la contraseña
    
    password = get_password(tag, private_key, master_key, use_chars, password_length)
    print(f"Generated Password: {password}")