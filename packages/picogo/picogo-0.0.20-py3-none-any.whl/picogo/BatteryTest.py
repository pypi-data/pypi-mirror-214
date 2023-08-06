from time import sleep

from .Battery import Battery
from .LCD import LCD

if __name__ == '__main__' :
    
    lcd = LCD()
    
    lcd.fill(0xF232)
    lcd.line(2,2,70,2,0xBB56)
    lcd.line(70,2,85,17,0xBB56)
    lcd.line(85,17,222,17,0xBB56)
    lcd.line(222,17,237,32,0xBB56)
    lcd.line(2,2,2,118,0xBB56)
    lcd.line(2,118,17,132,0xBB56)
    lcd.line(17,132,237,132,0xBB56)
    lcd.line(237,32,237,132,0xBB56)

    lcd.text("Raspberry Pi Pico", 90, 7, 0xFF00)
    lcd.text("PicoGo", 10, 7, 0x001F)
    lcd.text("Waveshare.com", 70, 120, 0x07E0)
    lcd.show()

    battery = Battery()
    
    count = 0
    while True :
        count += 1
        
        temperature, voltage, percent = battery.read()
        
        print( f"[{count:03d}] Temperature = {temperature:.3f} °C, Voltage = {voltage:.3f} V, Percent = {percent:.2} %" )
        
        y = 35
        lcd.fill_rect( 30, y, 160, 80, 0xF232 )
        
        lcd.text( f"count : {count}", 30, y, 0xFFFF ); y += 15
        lcd.text( f"temperature : {temperature:5.2f} °C", 30, y, 0xFFFF ); y += 15
        lcd.text( f"Voltage     : {voltage:5.2f} V", 30, y, 0xFFFF ); y += 15
        lcd.text( f"percent     : {percent:3.1f} %", 30, y, 0xFFFF ); y += 15

        lcd.show()
        sleep( 1 )
    pass

pass