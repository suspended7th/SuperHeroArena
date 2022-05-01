from passlib.hash import bcrypt

hasher = bcrypt.using(rounds=30)

def authenticate(user, password):
    return hasher.verify(password + user.salt, user.password)

def generate_hashed_password(user, password):
    user.salt = bcrypt.gensalt()
    password += user.salt
    user.password = hasher.hash(password)
    