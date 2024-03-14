from conversion import *
def pad(string, length, char):
    remainder = len(string) % length
    return char * remainder + string
def crc(binary, generator):
    og_generator = btoi(generator)
    binary = binary + '0' * (len(generator) -1)
    generator = generator + '0' * (len(binary) - len(generator))

    binary = btoi(binary)
    generator = btoi(generator)
    while(binary > og_generator):
        if len(itob(binary)) == len(itob(generator)):
            binary = binary ^ generator
        else:
            generator >>= 1
    remainder = itob(binary)
    return remainder
def generate_crc(binary, generator):

    print("Generating crc...")
    remainder = crc(binary, generator)
    return binary + pad(remainder, len(generator), '0')
def check_crc(binary, generator):
    print("Validating crc...")
    remainder = crc(binary, generator)
    if remainder == 0:
        print("No error!")
    else:
        print("Error detected")
# print(crc("10010", "11") )