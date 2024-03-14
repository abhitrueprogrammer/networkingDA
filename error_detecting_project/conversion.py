def itob(num):
    text = ""
    #Linus said back coding practise
    if num == 0:
        return '0'
    
    while(num != 0):
        text += str(num % 2)
        num = num // 2
    return text[::-1]
def btoi(binary):
    sum = 0
    for i in range(len(binary)-1,-1,-1):
        if binary[i] == '1':
            sum += 2**(len(binary)-i-1)
    return sum

def htob(hex):
    num = int(hex,16)
    return itob(num)