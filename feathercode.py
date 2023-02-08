# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

import struct
import storage
import board
import canio
import digitalio
import microcontroller
import json

def dbclookup(dataload,canbusid):
    for i in dataload['params']:
        if i['canId'] == canbusid:
            for x in i['signals']:
                output = [i['canId'],x['category'],x['name'],x['factor'],x['comment']]
                return(output)
                

canbusid = 1512

with open('msdash.json', 'r') as f:
    db = json.load(f)

z = dbclookup(db,canbusid)
#print(z)

# If the CAN transceiver has a standby pin, bring it out of standby mode
if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)

# If the CAN transceiver is powered by a boost converter, turn on its supply
if hasattr(board, 'BOOST_ENABLE'):
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)

# Use this line if your board has dedicated CAN pins. (Feather M4 CAN and Feather STM32F405)
can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=500_000, auto_restart=True)

#the listener is looking for a canid that you input. Here are a list of the MS2 canIDs in hex
# 0x5e8 = 1512, 0x5e9 = 1513, 0x5ea = 1514, 0x5eb = 1515 0x5ec = 1516
listener = can.listen(matches=[canio.Match(0x5e8)], timeout=.9)

    # Open the JSON file
#with open('msdash.json', 'r') as f:
  # Parse the JSON data directly from the file
  #db = json.load(f)
  #sig = db['params']

#for i in sig:
    #print(sig)


#length = len(sig)
#print(length)

  #print(sig[0])
  #print(f"---------------------")
  #print(sig[1])
  #print(f"---------------------")
  #print(sig[2])
  #print(f"---------------------")
  #print(sig[3])
  #print(f"---------------------")
  #print(sig[4])
  #print(f"---------------------")
  #for i in sig:
      #print(i)



#canidentifier = parsed_data['params']['canId']
# Access the data as a Python object
#print(parsed_data['params'])

old_bus_state = None
old_count = -1

while True:
    bus_state = can.state
    if bus_state != old_bus_state:
        print(f"Bus state changed to {bus_state}")
        old_bus_state = bus_state

    message = listener.receive()
    if message is None:
        print("No messsage received within timeout")
        continue

    data = message.data
    if len(data) != 8:
        print(f"Unusual message length {len(data)}")
        continue

    #print(f"--------------------")



    count, now_ms = struct.unpack("<II", data)
    gap = count - old_count
    old_count = count
    print(f"received message: id={message.id:x} data={data} count={count} now_ms={now_ms}")
    if gap != 1:
        print(f"gap: {gap}")

    #send can data acknowledge packet
    print("Sending ACK")
    can.send(canio.Message(id=0x5e9, data=struct.pack("<I", count)))

    #set canData equal to the bytes of data received on the can message
    canData = bytes(data)
    #optional* print out the 8 bytes of can data
    #print(canData)

    # each of the values in this can packet are 2 bytes each.
    # ">" means big-endian and the "h" is for 2 byte short integer
    MAP, RPM, CLT, TPS = struct.unpack('>hhhh', canData)

    #seperation line to make the CLI more readable
    #print(f"--------------------")

    # printing out each of the 2 byte values in the canid 1512 / 0x5e8
    # note some of the values need to be divided to give usable value
    print(f"RPM : {RPM}")
    print(f"Coolant Temperature : {(CLT *.1)}")
    print(f"Manifold Pressure : {(MAP *.1)} Kilopascals")
    print(f"Throttle Position : {(TPS *.1)}")
    print(z)
    

    #print arduino cpu temperature
    print(f"CPU Temperature : {(microcontroller.cpu.temperature * (9/5) + 32)} degrees f")




