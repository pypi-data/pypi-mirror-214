from random import randint

from .LCD import LCD
from .Battery import Battery
from .time import sleep
        
if __name__=='__main__': 
    
    lcd = LCD()
    battery = Battery()
    
    lcd.disp_init()
    
    while True :
        
        lcd.disp_battery( battery )
        lcd.show()
        
        sleep( 1 )
    pass 
pass