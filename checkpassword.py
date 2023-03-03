import requests
import sys
import hashlib

def getUserInpur():
    password = sys.argv[1:]
    return password

def checkAllInputPasswords(passwordList):
    for password in passwordList:
        hashedPassword = hashPassword(password)
        hashedPasswordHead = getPasswordHead(hashedPassword)
        hashedPasswordTail = getPasswordTail(hashedPassword)
        serverResponse = requestApiData(hashedPasswordHead)
        passwordPwnedCount = getPasswordLeaksCount(serverResponse, hashedPasswordTail)
        printPasswordInfo(password, passwordPwnedCount)

def hashPassword(password):
    encodedPassword = password.encode('utf-8')
    sha1Password = hashlib.sha1(encodedPassword)
    hashedHexPassword = sha1Password.hexdigest().upper()
    
    return hashedHexPassword

def getPasswordHead(hashedHexPassword):
    return hashedHexPassword[:5]

def getPasswordTail(hashedHexPassword):
    return hashedHexPassword[5:]

def requestApiData(queryString):
    try:
        url = 'https://api.pwnedpasswords.com/range/' + queryString
        serverResponse = requests.get(url)
        if serverResponse.status_code != 200:
            raise RuntimeError(f'Error fetching: {serverResponse.status_code}')
        
        return serverResponse

    except ValueError as err:
        print('In Fucntion ' + requestApiData.__name__ + ' expected string as an argument') 

def getPasswordLeaksCount(serverHashList, referenceHashedPasswordTail):
    hashes = (line.split(':') for line in serverHashList.text.splitlines())
    for hashedPassword, pwnedCount in hashes:
        if hashedPassword == referenceHashedPasswordTail:
            return pwnedCount
    
    return 0

def printPasswordInfo(password, pwnedCount):
    if pwnedCount == 0:
        print(f"{password} hasn't been leaked. It's safe to use it.")
    else:
        print(f"{password} has been hacked {pwnedCount} times! You shoud consider changing your password.")

userInput = getUserInpur()
checkAllInputPasswords(userInput)