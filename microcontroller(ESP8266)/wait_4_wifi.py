#standby for a specific wireless network 
# when connected send a wazap message to specific contacts 
# when disconnected wait for wifi to restore

import machine
import network
import time

print(__name__)

#declare wireless object
sta=network.WLAN(network.STA_IF)
sta.active(True)

def setup(ssid='',passw=''):
    '''
    Function sets ssid and password for connection
    '''
    
    if ssid=='':
        c=-1
        while c==-1:
            av=[a[0].decode('utf-8') for a in sta.scan()]#get all available wifi network in range
            for a,b in enumerate(av):
                print('{}. {}'.format(a,b))
            c=int(input('Choose wifi network, if not available press -1: '))
            if c!=-1:
                ssid=av[c]
        

    if passw=='':
        passw=input('Enter your wifi password: ')

    sta.connect(ssid,passw)
    
    return ssid,passw
 
def loop(ssid,passw):
    '''
    ssid= wifi name

    passd= wifi password
    '''
    while True:
        connected=True
        #wait until wifi connection is stablished
        cu_time=time.time()#current time

        while sta.isconnected()==False or time.time()!=(cu_time+10):
            print(time.time())
            time.sleep(0.5)
            connected=False


        if not(sta.isconnected()):
            setup()

        #when connected print ip
        print(sta.ifconfig())

        #send message
        if not(connected):
            print('sending message')
            time.sleep(5)
            ###codigo para enviar mensaje por wazap/MQTT......
            print('message sent')
        time.sleep(60)

if __name__=='home':
    a,b=setup()
    loop(a,b)

