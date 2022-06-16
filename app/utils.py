from passlib.context import CryptContext


"""Password Context for Hashing"""
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")


def hashPassword(password:str) -> str:
    return pwd_context.hash(password)

def verifyPassword(plainPassword:str , hashedPassword:str) -> bool:
    return pwd_context.verify(plainPassword,hashedPassword)