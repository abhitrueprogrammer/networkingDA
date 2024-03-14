import checksum, crc, hamming
from conversion import *

print("Enter the check you want to perform:")
detectionMethod = int(input("checksum(0)/crc(1)/hamming(2): "))
print("Enter you want to perform the check for sender or reciever: ")
reciever = int(input("sender(0)/reciever(1): "))
sender = not(reciever)
hex = int(input(("Enter if message is in binary(0) or hex(1):")))
message = input("Enter your message: ")
if hex:
    message = htob(message)

match detectionMethod:
    case 0:
        if sender:
            print("checksum: ", checksum.makeChecksumComplient(message))
        else:
            checksum.checkValidChecksum(message)
    case 1:
        generator = input("Enter the generator in binary: ")
        if sender:
            print(crc.generate_crc(message,generator))
        else:
            crc.check_crc(message,generator)
    case 2:
        if sender:
            print("required hamming code: ", hamming.hamming_generate(message))
        else:
            hamming.hammingCorrect(message)
