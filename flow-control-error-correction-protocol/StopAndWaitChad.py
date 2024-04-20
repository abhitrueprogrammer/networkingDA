import time
from error_correction import *  # Import for error correction functions (add_parity, check_parity, remove_parity)

"""
This code implements a simple reliable data transfer protocol using error correction 
and acknowledgments. It demonstrates the Sender and Receiver functionalities.

Error correction uses even parity. You'll need to implement the `error_correction.py` file 
with the necessary functions.
"""

class SharedVariable:
    """
    Shared variable class to hold data and control information between Sender and Receiver.
    """
    data = None  # Holds the data to be sent/received
    PacketNumber = -1  # Sequence number of the packet
    ACK = -1  # Acknowledgment value

# Class dataSent is commented out as it's not being used currently

class Sender(SharedVariable):
    """
    Sender class responsible for sending data packets with error correction and handling acknowledgments.
    """
    def send(self, PacketNumber, data):
        """
        Sends a data packet with error correction (even parity) and prints a message.

        Args:
            PacketNumber: Sequence number of the packet.
            data: The data to be sent.
        """
        SharedVariable.data = add_parity(data)  # Add error correction
        SharedVariable.PacketNumber = PacketNumber
        print(f"Sent: {data}")

    def ACK(self):
        """
        Returns the current acknowledgment value from the shared variable.

        Returns:
            The acknowledgment value (sequence number).
        """
        return SharedVariable.ACK


class Receiver(SharedVariable):
    """
    Receiver class responsible for receiving data packets, performing error correction, 
    and sending acknowledgments.
    """
    AllData = {}  # Dictionary to store received and assembled data

    def recieve(self):
        """
        Receives a data packet, checks for errors, processes it, and sends acknowledgments.

        Prints informative messages about received data, errors, and acknowledgments.
        """
        data = SharedVariable.data
        packetNumber = SharedVariable.PacketNumber
        if packetNumber not in self.AllData:
            print(data, check_parity(data))  # Print data and its parity check result
            if(check_parity(data) == 0):  # Check for errors using even parity
                remove_parity(data)  # Remove parity bits if no error detected
                self.AllData[packetNumber] = data  # Store received data
                print(f"Received: {data}")
                # Implement additional checks here (like checksum) and send NACK if needed
                print(f"Acknowledgment sent for sequence number: {packetNumber}")
                SharedVariable.ACK = packetNumber  # Send positive acknowledgment
            else:
                print(f"Data corrupted: {data}")
                SharedVariable.ACK = -packetNumber  # Send negative acknowledgment (NACK)
                print(f"NACK sent for sequence number: {packetNumber}")


wait_time = 5  # Timeout value in seconds
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

for packetnumber, data in packets_list:
    while(not(sent)):
        print(f"Sending packet number: {packetnumber}")
        sender.send(packetnumber, data)
        while(current_time - old_time < wait_time):
            reciever.recieve()
            time.sleep(0.1)  # Introduce a slight delay for simulation purposes
            if sender.ACK() == packetnumber:
                sent = True
                break
            if sender.ACK() == -packetnumber:  # Handle NACK (negative acknowledgment)
                sender.send(packetnumber, data)  # Resend the packet
            current_time = old_time = time.time()  # Reset timer for timeout
        current_time = old_time = time.time()  # Reset timer for next packet
    sent = False

print(reciever.AllData)  # Print the received and assembled data
