from werkzeug.security import generate_password_hash

usuario = "nico"
password = "UPTalpPBA26"

print(generate_password_hash(password))