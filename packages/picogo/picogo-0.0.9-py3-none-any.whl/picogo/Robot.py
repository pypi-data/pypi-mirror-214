import machine
from machine import Pin, Timer
import ujson, utime
from time import sleep

from .Motor import Motor
from .RGBLed import RGBLed
from .LCD import LCD

class Robot :
    
    VERSION = 1000
    
    low_speed  = 30
    med_speed  = 50
    high_speed = 80
    
    def __init__(self):
        self.speed = self.low_speed
        
        self.rgbLed = RGBLed()
        
        self.buzzer = machine.Pin(4, Pin.OUT)
        self.led = machine.Pin(25, Pin.OUT)
        
        self.battery = machine.ADC(Pin(26))
        self.temperature = machine.ADC(4)
                
        self.lcd = LCD()
        self.motor = Motor()
        
        self.uart = machine.UART(0, 115200)
        
        self.init_robot()
    pass

    def init_robot( self ):
        print( "init_robot")
        
        lcd = self.lcd
        
        duration = 1
        
        lcd.disp_logo()        
        self.beepOnOff( repeat = 1, period = 1.2 )        
        sleep( duration )
        
        lcd.disp_full_number( self.VERSION, flush=True )        
        sleep( duration )
        
        lcd.disp_logo()        
        sleep( duration )
        
        if False :
            lcd.disp_full_text( "PicoRun\nSkySLAM\nVer 1.0", flush=True )    
            sleep( duration )
        pass
        
        print( "done init robot." )
    pass

    def beepOnOff(self, repeat = 1, period = 0.5 ) :
        print( "beepOnOff" )
        
        buzzer = self.buzzer
        
        repeat = max( 1, repeat )
        
        for i in range( repeat*2 ) :
            buzzer.value( (i+1) % 2 )
            sleep( period )
        pass
    
        print( "done. beepOnOff" )
    pass 

pass

if __name__ == '__main__' :
    robot = Robot()
pass