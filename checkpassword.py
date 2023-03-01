import requests
import sys


password = sys.argv[1:]
url = 'https://api.pwnedpasswords.com/range/' + password[0]
res = requests.get(url)
print(res)