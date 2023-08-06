from .LCD import LCD 
        
if __name__=='__main__':
    # LCDPrintTest.py
    
    lcd = LCD() 
    
    lcd.print( "Hello...." )
    lcd.print( "Raspberry Pi Pico", c=LCD.BLUE )
    lcd.print( "PicoGo", c=LCD.WHITE ) 
    
    lcd.print( "Hello...." )
    lcd.print( "Raspberry Pi Pico", c=LCD.BLUE )
    lcd.print( "PicoGo", c=LCD.WHITE )
    lcd.print( "Waveshare.com", c=LCD.RED ) 
    
    lcd.show()
pass