class SharedVariable:
    data = None
    PacketNumber = -1
    ACK = -1
# class dataSent:
#     def __init__(self, data, PacketNumber) -> None:
#         self.data = data
#         self.PacketNumber = PacketNumber

class Sender(SharedVariable):
    def send(self, PacketNumber, data):
        SharedVariable.data = data
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
            self.AllData[packetNumber] = data
            print(f"Received: {data}")
            #do checking here, send NACK if packet is corrupted
            
            print(f"Acknowledgment sent for sequence number: {packetNumber}")
            SharedVariable.ACK = packetNumber
import time
wait_time = 5
old_time = current_time = time.time()
packets_list = [
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
for packetnumber, data in packets_list:
    while(not(sent)):
        print(f"Sending packet number: {packetnumber}")
        sender.send(packetnumber, data)
        while(current_time - old_time < wait_time):
            reciever.recieve()
            time.sleep(0.1)
            if sender.ACK() == packetnumber:
                sent = True
                break
            current_time = old_time
            current_time = time.time()
        current_time = old_time = time.time()
    sent = False
print(reciever.AllData)