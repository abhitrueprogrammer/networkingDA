import time
from error_correction import *

#to act as a transmission medium
class SharedVariable:
    data = None
    PacketNumber = -1
    ACK = -1

class Sender(SharedVariable):
    def send(self, PacketNumber, data):
        #add error correction
        SharedVariable.data = add_parity(data)
        SharedVariable.PacketNumber = PacketNumber
        print(f"Sent: {data}")
    def ACK(self):            
        return SharedVariable.ACK

class Receiver(SharedVariable):
    AllData = {}
    def recieve(self):
        data = SharedVariable.data
        packetNumber = SharedVariable.PacketNumber
        if packetNumber not in self.AllData:
            print(data, check_parity(data))
            if(check_parity(data) == 0):
                remove_parity(data)
                self.AllData[packetNumber] = data
                print(f"Received: {data}")
                print(f"Acknowledgment sent for sequence number: {packetNumber}")
                SharedVariable.ACK = packetNumber
            else:
                #sending NACK if corrupted
                print(f"Data corrupted: {data}")
                SharedVariable.ACK = -packetNumber
                print(f"NACK sent for sequence number: {packetNumber}")

#main execution starts    
wait_time = 5
old_time = current_time = time.time()
packets_list = [
    [0, "If"],
    [1, "A"],
    [2, "Quick"],
    [3, "Brown"],
    [4, "Fox"],
    [5, "Jumps"],
    [6, "Over"],
    [7, "The"],
    [8, "Lazy"],
    [9, "Dog"]
]
sender = Sender()
reciever = Receiver()
sent = False
#sending & recieving packets
for packetnumber, data in packets_list:

    while(not(sent)):
        print(f"Sending packet number: {packetnumber}")
        sender.send(packetnumber, data)
        #waiting for ACK or NACK until timer times out
        while(current_time - old_time < wait_time):
            reciever.recieve()
            time.sleep(0.1)
            if sender.ACK() == packetnumber:
                sent = True
                break
            if sender.ACK() == -packetnumber:
                sender.send(packetnumber, data)
            current_time = old_time
            current_time = time.time()
        current_time = old_time = time.time() #reset the timer 
    sent = False
print(reciever.AllData)