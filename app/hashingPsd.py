from pwdlib import PasswordHash



password_hash = PasswordHash.recommended()  # telling hashing algo
#check documentation for how to use bcrypt

def hashedPassword(password:str)->str:
    return password_hash.hash(password)
    
def verifyPassword(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password, hashed_password)