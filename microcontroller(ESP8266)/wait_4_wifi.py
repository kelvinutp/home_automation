#standby for a specific wireless network 
# when connected send a wazap message to specific contacts 
# when disconnected wait for wifi to restore

import machine
import network
import time

print(__name__)

#declare and reset wireless object
sta=network.WLAN(network.STA_IF)
sta.active(False)
sta.active(True)

#save lastest 5 connected network and password
#history={ssid:password}
history={}

def setup(ssid='',passw=''):
    '''
    Function sets ssid and password for connection
    '''
    av=[a[0].decode('utf-8') for a in sta.scan()]#get all available wifi network in range
    
    #try to connect to previously connected network
    for a in history.keys():
        if a in av:
            __conn2wifi(a,history[a])
        
        if sta.isconnected():
            break

    #if not previously connected network available
    while not(sta.isconnected()) or ssid=='':
        while ssid=='':

            #show all available networks            
            for a,b in enumerate(av):
                print('{}. {}'.format(a,b))
            
            c=int(input('Choose wifi network, if not available press -1: '))
            if c!=-1:
                ssid=av[c]
   
        passw=input('Enter your wifi password: ')
        __conn2wifi(ssid,passw)
 
    return
    
def __conn2wifi(ssid,passw):
    sta.connect(ssid,passw)
    # connecting to wifi
    #wait until wifi connection is stablished
    cu_time=time.time()#current time
    while sta.isconnected()==False and time.time()!=(cu_time+10):
        print(time.time())
        time.sleep(1)

    if not(sta.isconnected()):
        return
    
    #save wifi and password
    if ssid not in history:
        history[ssid]=passw
    
    #when connected print ip
    print(sta.ifconfig())

    return
 
def loop():
    # while True:
    for a in range(2):
        if not(sta.isconnected()):
            setup()

        #send message
        print('sending message',a)
        time.sleep(5)
        ###codigo para enviar mensaje por wazap/MQTT......
        print('message sent')
        time.sleep(10)

if __name__=='home':
    setup()
    loop()
    for a,b in history.items():
        print('ssid:{}\npassword:{}'.format(a,b))
