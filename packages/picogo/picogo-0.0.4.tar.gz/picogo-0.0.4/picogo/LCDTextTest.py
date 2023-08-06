from LCD import LCD 
        
if __name__=='__main__':
    lcd = LCD()
    
    lcd.fill( LCD.BLACK )
    
    lcd.text( "Raspberry Pi Pico", 10, 5, LCD.BLUE )
    lcd.text( "PicoGo", 10, 15, LCD.WHITE )
    lcd.text( "SkySLAM", 10, 25, 0x07E0 )
    
    lcd.show() 
pass