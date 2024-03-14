
from conversion import *
def calculate_inverse(bin):
    text = ""
    for bit in str(bin):
        if bit == '1':
            text += '0'
        else:
            text += '1'
    return text
    
def checksum(text):
    split = 8
    remainder = len(text) % split
    text = remainder * '0' + text
    wordlst = [text[i: i+split] for i in range(0, len(text), split)]
    sum = 0
    for word in wordlst:
        sum += btoi(word)
    while len(itob(sum)) > split:
        sum = (sum & btoi("1"*8)) + (sum >> 8)
    return calculate_inverse(itob(sum))
text = "1011010111110111"

def makeChecksumComplient(text):
    print("Generating checksum..")
    return text + checksum(text)
def checkValidChecksum(text):
    print("Validating checksum...")
    check = checksum(text)
    check = int(check)
    if check == 0:
        print("Valid checksum address")
        return 0
    else:
        print("Invalid checksum")
        return 1
