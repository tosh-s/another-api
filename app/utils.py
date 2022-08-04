from passlib.context import CryptContext

# this utils file is created to reduce the size of the main file and move some funtions over here.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)