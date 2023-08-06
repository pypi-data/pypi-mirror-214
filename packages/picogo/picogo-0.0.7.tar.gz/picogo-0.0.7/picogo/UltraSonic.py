from machine import Pin
from time import sleep, sleep_us, ticks_us

class UltraSonic :
    
    def __init__( self ) :
        self.echo = Pin(15, Pin.IN)
        self.trig = Pin(14, Pin.OUT)
        
        self.trig.value(0)
        self.echo.value(0)
    pass

    def obstacle_distance( self ) :
        echo = self.echo
        trig = self.trig
        
        trig.value(1)
        sleep_us( 10 )
        trig.value(0)
        
        while echo.value() == 0 :
            pass
        
        then = ticks_us()
        
        while echo.value() == 1 :
            pass
        
        now = ticks_us()
        
        distance= (now - then)*0.017
        
        return distance
    pass

pass
