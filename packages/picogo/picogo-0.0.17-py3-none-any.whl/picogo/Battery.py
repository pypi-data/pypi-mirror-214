from machine import Pin, ADC
from time import sleep

class Battery :
    def __init__( self ) : 
        self.batt = ADC(Pin(26))
        self.temp = ADC(4)
    pass

    def read( self ) :
        batt = self.batt
        temp = self.temp
        
        reading = temp.read_u16()*3.3/65535        
        temperature = 27 - (reading - 0.706)/0.001721
        
        voltage = batt.read_u16()*3.3/65535*2
        percent = (voltage - 3)*100/1.2
        
        percent = max( 0, min( 100, percent ) )
        
        return temperature, voltage, percent         
    pass

pass