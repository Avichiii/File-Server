import string

def rotReverse(psw: str):
    lenpass = len(psw)

    decryptedPass = ''

    for i in range(lenpass):
        if psw[i] in string.ascii_lowercase:
            index = string.ascii_lowercase.index(psw[i])
            decryptedPass += string.ascii_lowercase[(index-13)%26]
        elif psw[i] in string.ascii_uppercase:
            index = string.ascii_uppercase.index(psw[i])
            decryptedPass += string.ascii_uppercase[(index-13)%26]
        else:
            decryptedPass += i
        
    if decryptedPass == 'secretpass':
        return True
    else:
        return False
