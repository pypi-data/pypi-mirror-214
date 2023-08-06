from machine import Pin
from time import sleep_us

from .Motor import Motor

def getkey( irRemoteCon ):
        
    if irRemoteCon.value() == 0 :
        count = 0
        
        while (irRemoteCon.value() == 0) and (count < 100) : #9ms
            count += 1
            sleep_us(100)
        pass
        
        if(count < 10):
            return None
        pass
    
        count = 0
        
        while (irRemoteCon.value() == 1) and (count < 50) : #4.5ms
            count += 1
            sleep_us(100)
        pass
            
        idx = 0
        cnt = 0
        data = [0,0,0,0]
        
        for i in range(0,32) :
            count = 0
            while (irRemoteCon.value() == 0) and (count < 10) :    #0.56ms
                count += 1
                sleep_us(100)

            count = 0
            while (irRemoteCon.value() == 1) and (count < 20) :   #0: 0.56mx
                count += 1                                #1: 1.69ms
                sleep_us(100)

            if count > 7 :
                data[idx] |= 1<<cnt
            pass
        
            if cnt == 7 :
                cnt = 0
                idx += 1
            else:
                cnt += 1
            pass

        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF :  #check
            return data[2]
        else:
            return("repeat")
        pass
    
    pass

pass

if __name__=='__main__':
    
    motor = Motor()
    irRemoteCon = Pin(5, Pin.IN)
    speed = 20
    
    print( "Hello ... Remote Controller !" )
    
    while True:
        key = getkey( irRemoteCon )
        
        if(key != None):
            if key == 0x18:
                motor.forward(speed)
            elif key == 0x08:
                motor.left(20)
            elif key == 0x1c:
                motor.stop()
            elif key == 0x5a:
                motor.right(20)
            elif key == 0x52:
                motor.backward(speed)
            elif key == 0x09:
                speed = 50
                print(speed)
            elif key == 0x15:
                if(speed + 10 < 101):
                    speed += 10
                print(speed)
            elif key == 0x07:
                if(speed - 10 > -1):
                    speed -= 10
                print(speed)
            pass
        pass
    pass

pass
