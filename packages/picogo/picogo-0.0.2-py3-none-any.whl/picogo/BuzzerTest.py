from machine import Pin
from time import sleep

if __name__ == '__main__' :
    
    buzzer = Pin(4, Pin.OUT)

    buzzer.value( 1 )
    sleep( 2 )
    buzzer.value( 0 )
    
pass