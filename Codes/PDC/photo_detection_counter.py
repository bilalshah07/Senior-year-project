from serial import *
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wgt
import os

def FindHeader(s):
    
    ''' We have inserted a random 35 bit long in the FPGA code. At the moment we
     are receiving 8 counts; after every session of these counts we ask the FPGA to
     this random long. We use this packet to mark the send and receive of an 8 count
     session. We find the packet first to make sure we are receiving the correct
     byte sequence.'''
    
    counter = 0
    byte = decto7bit(s.read(1)[0])
    # print(byte)
    
    ''' Data is being received in 7-bit packets, these five 7-bit packets make
    up the header that we are hoping to receive from the FPGA'''
    
    start = ["0001001", "1001100", "0100101", "0101010", "1011101"]

    trial = [] # Packets are received in reverse order aso we make a reverse array of these packets in this variable.
    for i in range(1, len(start)+1):
        trial.append(start[-i])

    while True: # Looking for the packet in this loop.

        counter += 1
        ans = ""

        if counter > 100:
            print("Couldn't find the packet.")
            break
            
        if byte != trial[0]:
            print("Returning from stage 1")
            byte = decto7bit(s.read(1)[0])
            print(byte)
            continue
        
        ans = byte + ans
        byte = decto7bit(s.read(1)[0])
        # print(byte)

        
        if byte != trial[1]:
            print("Returning from stage 2")
            byte = decto7bit(s.read(1)[0])
            print(byte)
            continue
        
        ans = byte + ans
        byte = decto7bit(s.read(1)[0])
        # print(byte)
        
        if byte != trial[2]:
            print("Returning from stage 3")
            byte = decto7bit(s.read(1)[0])
            print(byte)
            continue
        
        ans = byte + ans
        byte = decto7bit(s.read(1)[0])
        
        # print(byte)
        
        if byte != trial[3]:
            print("Returning from stage 4")
            byte = decto7bit(s.read(1)[0])
            print(byte)
            continue
        
        ans = byte + ans
        byte = decto7bit(s.read(1)[0])
        # print(byte)
        
        if byte != trial[4]:
            print("Returning from stage 5")
            byte = decto7bit(s.read(1)[0])
            print(byte)
            continue
        
        ans = byte + ans

        # print("Start Packet found =", ans)
        break
    
    return ans

def decto7bit(byte): # Simple function to convert the decimal representation of a number we receive from the FPGA into binary that we need to combine and read.
    
    bit = ""
    
    while byte >= 1:
        if byte%2 == 0:
            bit = "0" + bit
        elif byte%2 == 1:
            bit = "1" + bit
        byte = int(byte/2)
        
    if len(bit) < 7:
        for i in range(7-len(bit)):
            bit = "0" + bit
            
    return bit    

def bin2dec(data): # Converting a number from binary representation to decimal for us to read as output. 
    len_data = len(data)
    ans = 0
    for i in range(len_data):
        ans = ans + int(data[i])*(2**(len_data-1-i))
    return ans

def GetIndvCounts(s): # Every 1/10th of a second we receive a set of 8 counts. This function receives, processes, and returns one of those sets.
    
    data = s.read(51) # Receinig those 8 counts plus the header requires 46 bytes.

    temp = []
    for i in data:
        temp.append(decto7bit(i)) # dec27bit sends back a string.
    data = temp

    counts = []
    for i in range(9): # We are to receive a total of 9 counts
        temp = ""
        for j in range(5): # Each count is received in 5 7-bit long portions, we combine those portions here.
            temp = data[j+i*5] + temp
        counts.append(temp)

    ans = []
    for i in counts: # Here we convert the binary string representations into decimal counts.
        ans.append(bin2dec(i))
        
    return ans

def GetCounts(s):
    
    ''' This function checks if there are 51 bytes available to be read, and reads
    if there are. It repeats this 10 times and collects data for 1 second this way.
    It then returns the sum of counts for 1 whole second.'''
    
    num_iter = 0
    total_counts = []
    
    while True:

        if num_iter >= 10:
            return np.sum(total_counts, 0) # Returns an array of total counts received in 1 sec.

        if s.in_waiting > 51:
            total_counts.append(np.array(GetIndvCounts(s)))
            num_iter += 1

        sleep(0.03)
        
def SaveStop(val):
    plt.savefig("saved")
    
def Stop(val):
    os._exit(1)

def AcquireTrigger(val): # Function to run the whole program and return data for the asked
    global acquire    
    acquire = 1

def ContinuousCheck(): # Function to monitor counts for past 3 min
    
    acquisition_time = 10
    ack_reset = acquisition_time # This value needs to be changed once more 
    global acquire
    acquire = 0

    s = Serial("COM4", 19200)
    s.close()
    s.open()
    s.bytesize = 7
    s.stopbits = 2
    
    FindHeader(s)
    
    # plt.style.use('dark_background')
    # plt.style.use('seaborn-dark')
    
    plt.rcParams.update({
    "lines.color": "0.5",
    "patch.edgecolor": "0.5",
    "text.color": "0.95",
    "axes.facecolor": "0.5",
    "axes.edgecolor": "0.5",
    "axes.labelcolor": "0.5",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "0.1",
    "figure.edgecolor": "0.1",
    "savefig.facecolor": "0.1",
    "savefig.edgecolor": "0.1"})
    
    fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize = (10,6), sharex = True)
    
    b1ax = plt.axes([0.02, 0.93, 0.12, 0.045])
    save_stop_button = wgt.Button(b1ax, "Capture Screen", color="grey", hovercolor="#05b5fa")
    save_stop_button.on_clicked(SaveStop)
    
    b2ax = plt.axes([0.15, 0.93, 0.06, 0.045])
    stop_button = wgt.Button(b2ax, "Stop", color="grey", hovercolor="#05b5fa")
    stop_button.on_clicked(Stop)
    
    b3ax = plt.axes([0.22, 0.93, 0.14, 0.045])
    acquire_button = wgt.Button(b3ax, "Acquire data: "+str(ack_reset)+"s", color="grey", hovercolor="#05b5fa")
    acquire_button.on_clicked(AcquireTrigger)
    
    time = np.array([1])
    tic = 1
    counts = GetCounts(s)
    counts = np.array([GetCounts(s)])
    
    temp_data = []
    acquisition = 0
    
    for i in range(180):

        tic += 1
    
        time = np.append(time, tic)
    
        counts = np.append(counts, [GetCounts(s)], axis = 0)
    
        A = counts[:, 0]
        B = counts[:, 1]
        BP = counts[:, 2]
        AP = counts[:, 3]
        AB = counts[:, 4]
        ABP = counts[:, 5]
        APB = counts[:, 6]
        APBP = counts[:, 7]
        ABBP = counts[:, 8]
        
        
        if acquire == 1:
            
            print(".", end = " ")
            
            if ack_reset < 1:
                
                acquire = 0
                b4ax = plt.axes([0.37, 0.93, 0.16, 0.045])
                display = wgt.Button(b4ax, "  "+str(ack_reset)+"s | Acq "+str(acquisition)+" complete", color="0.2", hovercolor="0.2")
                print("Acquisition no.", acquisition, "completed.")
                np.savetxt("data"+str(acquisition)+".txt", temp_data)
                acquisition += 1
                ack_reset = acquisition_time # Restored to the original value, 120 in this case
                temp_data = []
            
            else:
                
                b4ax = plt.axes([0.37, 0.93, 0.04, 0.045])
                display = wgt.Button(b4ax, str(ack_reset)+"s", color="0.2", hovercolor="0.2")
                
                temp_data.append([A[-1], B[-1], BP[-1], AP[-1], AB[-1], ABP[-1], APB[-1], APBP[-1], ABBP[-1]])
                ack_reset -= 1
            
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        
        ax1.plot(time, A, color = "#45fc03", label = "A")
        ax1.plot(time, AP, color = "#05b5fa", label = "A'")
        ax1.text(time[-1], A[-1], A[-1])
        ax1.text(time[-1], AP[-1], AP[-1])
    
        ax2.plot(time, B, color = "#45fc03", label = "B")
        ax2.plot(time, BP, color = "#05b5fa", label = "B'")
        ax2.text(time[-1], B[-1], B[-1])
        ax2.text(time[-1], BP[-1], BP[-1])
    
        ax3.plot(time, AB, color = "#701c8c", label = "AB")
        ax3.plot(time, ABP, color = "#FFD700", label = "AB'")
        ax3.text(time[-1], AB[-1], AB[-1])
        ax3.text(time[-1], ABP[-1], ABP[-1])
    
        ax4.plot(time, APB, color = "#701c8c", label = "A'B")
        ax4.plot(time, APBP, color = "#FFD700", label = "A'B'")
        ax4.plot(time, ABBP, color = "#FD0E35", label = "ABB'")        
        ax4.text(time[-1], APB[-1], APB[-1])
        ax4.text(time[-1], APBP[-1], APBP[-1])
        
        ax1.legend(loc = 'upper left')
        ax1.set_title("Counts against time")
        ax1.set_ylabel("Counts")
    
        ax2.legend(loc = 'upper left')
        ax2.set_title("Counts against time")
    
        ax3.legend(loc = 'upper left')
        ax3.set_xlabel("Time(s)")
        ax3.set_ylabel("Counts")
    
        ax4.legend(loc = 'upper left')
        ax4.set_xlabel("Time(s)")
        
        plt.pause(0.001)
        
    while True:
        
        tic += 1
        
        time = np.delete(time, 0)
        time = np.append(time, tic)
        
        counts = np.delete(counts, 0, axis = 0)
        counts = np.append(counts, [GetCounts(s)], axis = 0)
    
        A = counts[:, 0]
        B = counts[:, 1]
        BP = counts[:, 2]
        AP = counts[:, 3]
        AB = counts[:, 4]
        ABP = counts[:, 5]
        APB = counts[:, 6]
        APBP = counts[:, 7]
        ABBP = counts[:, 8]
        
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        
        if acquire == 1:
            
            print(".", end = " ")
            
            if ack_reset < 1:
                acquire = 0
                print("Acquisition no.", acquisition, "completed.")
                np.savetxt("data"+str(acquisition)+".txt", temp_data)
                acquisition += 1
                ack_reset = acquisition_time # Restored to the original value, 120 in this case
                temp_data = []
                
            temp_data.append([A[-1], B[-1], BP[-1], AP[-1], AB[-1], ABP[-1], APB[-1], APBP[-1], ABBP[-1]])
            ack_reset -= 1
        
        ax1.plot(time, A, color = "#45fc03", label = "A")
        ax1.plot(time, AP, color = "#05b5fa", label = "A'")
        ax1.text(time[-1], A[-1], A[-1])
        ax1.text(time[-1], AP[-1], AP[-1])
    
        ax2.plot(time, B, color = "#45fc03", label = "B")
        ax2.plot(time, BP, color = "#05b5fa", label = "B'")
        ax2.text(time[-1], B[-1], B[-1])
        ax2.text(time[-1], BP[-1], BP[-1])
    
        ax3.plot(time, AB, color = "#701c8c", label = "AB")
        ax3.plot(time, ABP, color = "#FFD700", label = "AB'")
        ax3.text(time[-1], AB[-1], AB[-1])
        ax3.text(time[-1], ABP[-1], ABP[-1])
    
        ax4.plot(time, APB, color = "#701c8c", label = "A'B")
        ax4.plot(time, APBP, color = "#FFD700", label = "A'B'")
        ax4.plot(time, ABBP, color = "#FD0E35", label = "ABB'")        
        ax4.text(time[-1], APB[-1], APB[-1])
        ax4.text(time[-1], APBP[-1], APBP[-1])   
        
        ax1.legend(loc = 'upper left')
        ax1.set_title("Counts against time")
        ax1.set_ylabel("Counts")
    
        ax2.legend(loc = 'upper left')
        ax2.set_title("Counts against time")
    
        ax3.legend(loc = 'upper left')
        ax3.set_xlabel("Time(s)")
        ax3.set_ylabel("Counts")
    
        ax4.legend(loc = 'upper left')
        ax4.set_xlabel("Time(s)")
        
        plt.pause(0.001)
    
    plt.show()
    
    s.close()
    
ContinuousCheck()