from LCD import LCD
from UltraSonic import UltraSonic
from time import sleep 
        
if __name__=='__main__': 
    
    lcd = LCD()
    ultraSonic = UltraSonic()
    
    lcd.disp_init()
    
    while 1 :
        dist = ultraSonic.obstacle_distance()
        lcd.disp_ultra_sonic( dist )
        lcd.show()
        
        print( f"Distance = {dist:6.2f} cm" )
        sleep( 0.1)
    pass
pass