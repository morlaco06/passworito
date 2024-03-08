import hashlib

def generar_hash(tag, private_key, master_key):
    combinacion = f"{tag}{private_key}{master_key}".encode()
    return hashlib.sha3_512(combinacion).hexdigest()
