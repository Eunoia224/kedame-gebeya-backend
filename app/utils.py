from passlib.context import CryptContext 

# telling passlib what hashing algorithm it should use
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

def hash(password: str):
    """hash the password the user provides.

    Args:
        password (str): the string the user provides to be their password.
    """
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    """Verify the user provided password matches with the one stored in our db.

    Args:
        plain_password (_type_): the user provided password.
        hashed_password (bool): the hashed password stored in the db.
    """
    return pwd_context.verify(plain_password, hashed_password)