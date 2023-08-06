from machine import Pin, SPI
from time import sleep
from random import randint
import framebuf, builtins

from .Battery import Battery
from .UltraSonic import UltraSonic
from .IRSensor import IRSensor
from .TRSensor import TRSensor
from .Motor import Motor
    
# ST7789
class LCD(framebuf.FrameBuffer):
    
    # RGC 565 Color Definition
    WHITE  = white  = 0xFFFF
    BLACK  = black  = 0x0000
    GREEN  = green  = 0x001F
    RED    = red    = 0x00F0
    BLUE   = blue   = 0xFF00
    GBLUE  = gblue  = 0X07FF
    YELLOW = yellow = 0xF0FF
    
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.bg = self.BLACK  # background color
        self.fg = self.WHITE  # foreground color
        
        self.texts = []
        self.text_idx = 0 
        
        self.inited_print = False
        
        self.rst = Pin(12,Pin.OUT)
        self.bl = Pin(13,Pin.OUT)
        self.bl(1)
        
        self.cs = Pin(9,Pin.OUT)
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(10),mosi=Pin(11),miso=None)
        self.dc = Pin(8,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        
        ## cod by sunabove ##
        self.init_display()
        
        self.fill( self.bg ) 
        
        x = 0
        y = 0
        rc = row_count = 6
        
        width = self.width
        height = self.height
        
        self.rect( x, y, width, height - 1, self.fg, False )
        
        m = 4
        
        rects = self.rects = []
        
        x = m
        w = width - 2*m
        h = int( (height - (rc + 2)*m - 1)/rc )
        
        for idx in range( rc ) :
            y = idx*h + (idx + 1)*m
            rect = [ x, y, w, h, m ]
            rects.append( rect )
        pass
        
        for r in rects :
            self.rect( r[0], r[1], r[2], r[3], self.fg, False )
        pass
    
    pass
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
    pass

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
    pass

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)
    pass

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    pass

    def flush( self ) :
        self.show()
    pass # flush

    def disp_text(self, text, x, y, fg=None, bg=None, flush=True) :
        if bg is None : bg = self.bg
        if fg is None : fg = self.fg
        
        width = self.width
        height = self.height
        
        self.rect( 2, 2, width -5, height -5, bg, True )
        
        for t in text.split( "\n" ) : 
            self.text( t, x, y, fg )
            y += 15
        pass
    
        flush and self.flush()
    pass # disp_text

    def print(self, *args, **kwargs) :
        width = self.width; height = self.height
        line_height = 15
        
        x = 0 ; y = 0
        
        m = 4
        w = width - 1
        h = int( (height - m - 1)/2 )
        y = h + m
        
        self.rect( x, y, w, h, self.bg, True )
        self.rect( x, y, w, h, self.fg, False )
        
        fg = None
        if "c" in kwargs :
            fg = kwargs.pop( "c" )
        elif "fg" in kwargs :
            fg = kwargs.pop( "fg" )
        else :
            fg = self.fg
        pass
    
        texts = "".join( args )
        
        for text in texts.split( "\n" ) :
            self.texts.append( [ text, fg, self.text_idx ] )
            self.text_idx += 1
        pass
    
        while len( self.texts ) > 8 :
            self.texts.pop( 0 )
        pass
    
        x = 10
        y += line_height 
        
        line_count = int( (height - y)/line_height )
        
        #print( f"line count = {line_count}" )
        
        for text in self.texts[ - line_count :  ] :
            t = text[ 0 ]
            fg = text[ 1 ]
            text_idx = text[ 2 ]
            
            t = f"[{text_idx + 1:2d}] {t}"
            self.text( t, x, y, fg )
            y += line_height
            
            #builtins.print( text )
        pass
        
        if False :
            builtins.print( "LCD : ", end="" )
            builtins.print( *args, **kwargs )
        pass
    pass # print

    def disp_init( self, flush=False ) :
        self.disp_battery()
        self.disp_ultra_sonic()
        self.disp_ir_sensor()
        self.disp_tr_sensor()
        self.disp_motor( flush=True )
    pass

    def disp_battery( self, values = [0, 0, 0], verbose=False, flush=False ) : # 배터리 잔량 표시 
        
        if isinstance( values , Battery ) :
            values = values.read()
        pass 
        
        temp, voltage, percent = values
        
        color = LCD.GREEN
        if percent < 33 :
            color = LCD.RED
        elif percent < 66 :
            color = LCD.BLUE
        else :
            color = LCD.GREEN
        pass
    
        fg = self.fg
        
        x, y, w, h, m = self.rects[0]
        
        self.rect( x, y, w, h, LCD.GBLUE, True )
        self.rect( x, y, int( w*percent/100 ), h, color, True )
        self.rect( x, y, w, h, fg, False )
        
        if False : self.text( f"{int(percent):3d} %", int(x + w/2 - 25), int( y + 5), LCD.WHITE )
        
        if flush : self.flush()
        
        if verbose : print( f"Temperature = {temp:.3f} °C, Voltage = {voltage:.3f} V, Percent = {percent:.2} %" )
        
    pass # disp_battery

    def disp_ultra_sonic( self, dist = 0 , verbose = 0, flush=0 ) :  # 초음파 센서 거리 표시 
        
        if isinstance( dist, UltraSonic ) :
            dist = dist.get_obstacle_distance()
        pass 
        
        color = LCD.GREEN
        
        max_dist = 40
        
        if dist <= 10 :
            color = 0xFFF0            
        elif dist <= 20 :
            color = LCD.RED
        elif dist <= 30 :
            color = LCD.BLUE
        else :
            color = LCD.GREEN
        pass
    
        fg = self.fg
        bg = self.bg
        
        x, y, w, h, m = self.rects[1]
        
        value_width = int( w*min(max_dist, dist)/max_dist )
        
        self.rect( x, y, w, h, LCD.GBLUE, True )
        
        if False :
            self.rect( x, y, value_width, h, color, True )
        else :
            cw = cell_width = int(w/10)
            
            for idx in range( int(value_width/cw + 0.5) ):
                c = color
                self.rect( x + idx*cw, y, cw - m, h, c, True )
            pass
        pass
        
        self.rect( x, y, w, h, fg, False )
        
        if flush : self.flush()
    
    pass # disp_ultra_sonic

    def disp_ir_sensor( self, blocks = [0, 0], flush = 0 ) :
        
        if isinstance( blocks, IRSensor ) :
            blocks = blocks.read_blocks()
        pass
        
        x, y, w, h, m = self.rects[2]
        
        bg = self.bg
        fg = self.fg
        
        self.rect( x, y, w, h, bg, True )
        self.rect( x, y, w, h, fg, False )
        
        x += m
        y += 1
        w = int( (w - 3*m)/2 )
        h = h - 2
        
        for idx, block in enumerate( blocks ) :
            c = LCD.RED if block else LCD.GREEN
            self.rect( x + idx*(w +m) , y, w, h, c, True )
            self.rect( x + idx*(w +m) , y, w, h, fg, False )
        pass
    
        if flush : self.flush()
        
    pass # disp_infrared_sensor

    def disp_tr_sensor( self, position = -1, sensors = [0]*5, flush = 0 ) :
        
        # draw sensor rectagnel 
        x, y, w, h, m = self.rects[3]
        h = 2*h + m
        
        bg = self.bg
        fg = self.fg
        
        self.rect( x, y, w, h, bg, True )
        self.rect( x, y, w, h, fg, False )
        
        sensors_len = len( sensors )
        
        w1 = (w - m*sensors_len - m)/sensors_len
        
        for idx, sensor in enumerate( sensors ) :
            sensor = min( sensor, 1_000 )
            sensor = max( sensor, 100 )
            
            h1 = (h - 2*m)*sensor/1_000
            x1 = x + idx*(w1 + m) + m
            y1 = y + m + (h - 2*m - h1)
            
            color = LCD.YELLOW
            
            self.rect( int(x1), int(y1), int(w1), int(h1), color, True )
            self.rect( int(x1), int(y + m), int(w1), int(h - 2*m), fg, False )
            
            #print( f"x1 = {x1}, y1 = {y1}, w1 = {w1}, h1 = {h1}" )
        pass
    
        # draw position circle
        we = h/4
        he = we
        
        xe = x + m + 3 + we/2
        
        pos = position
        
        if pos < 0 :
            xe = x + m + 3 + we/2
        elif pos > sensors_len - 1 : 
            xe = x + w - we - m - 4
        else :
            xe = x + w*(pos + 0.5)/sensors_len - we/2
        pass
    
        ye = y + h/2 
        
        self.ellipse( int(xe), int(ye), int(we), int(he), LCD.BLUE, True )
        self.ellipse( int(xe), int(ye), int(we), int(he), fg, False )
    
        if flush : self.flush()
    pass # disp_tr_sensor

    def disp_motor( self, speeds = [ 0, 0 ], flush=False ) :
        
        if isinstance( speeds, Motor ) :
            speeds = speeds.speeds
        pass
    
        x, y, w, h, m = self.rects[5]
        
        bg = self.bg
        fg = self.fg
        
        self.rect( int(x), int(y), int(w), int(h), bg, True )
        
        w_0 = (w - m)/2
        
        fg = self.green
        
        for idx, speed in enumerate( speeds ):
            c = self.green if speed > 0 else self.red
            x_0 = x + idx*(w_0 + m)
            
            w_1 = w_0*abs( speed )/100
            x_1 = x + idx*(w_0 + m)
            if idx ==0 :
                x_1 = x_1 + w_0 - w_1
            pass
            
            self.rect( int(x_1), int(y), int(w_1), int(h), c, True )
            self.rect( int(x_0), int(y), int(w_0), int(h), lcd.white, False )
        pass
        
        if flush : self.flush()
    pass # disp_motors

    def disp_full_text(self, text, fg=None, bg=None, flush=True) :
        if bg is None : bg = self.bg
        if fg is None : fg = self.fg
        
        width = self.width
        height = self.height
        
        m = 2
        
        self.rect( m, m, width - 2*m -1, height - 2*m -1, bg, True )
        
        if isinstance( text, str ) : 
            text = text.split( "\n" )
        pass
    
        text_len = len( text )
        
        x = 0
        y = height/2
        cw = ch = 8
        
        for i, t in enumerate( text ) :
            x = (width - cw*len(t))/2
            y = height/2 - 2*ch*( int(text_len/2) - i )
            
            self.text( t, int( x ), int( y), fg ) 
        pass
    
        flush and self.flush()
    pass # disp_full_text

    def color(self, R,G,B): # Convert RGB888 to RGB565
        return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)
    pass

    def disp_logo(self, fg=None, bg=None, flush=True) : 
        print( "disp_logo" )
        
        self.disp_logo_text( fg=fg, bg=bg, flush=flush)
    pass

    def disp_logo_text(self, fg=None, bg=None, flush=True) :
        from .LogoText import logo_text

        self.disp_full_text( logo_text, fg=fg, bg=bg, flush=flush )
    
        del logo_text
    pass        

    def disp_logo_image(self, logo_image, flush=True) : 
        
        bg = self.bg
        fg = self.fg 
        
        width = self.width
        height = self.height
        
        m = 0
        
        self.rect( m, m, width - 2*m -1, height - 2*m -1, bg, True )
        
        cw = 8
        ch = 16
        m = 2
        
        x0 = 2*m
        y0 = 2*m
        
        x = x0
        y = y0
        
        for t in logo_image :
            
            if t != '\n' :
                #print( f"x = {x}, y = {y}, t = {t}" )            
            
                if t == '∙' : t = ''
                self.text( t, int(x), int(y), fg )
                x += cw
            else :
                #print( f"new line encountered" );
                y += ch
                x = x0
            pass
        pass
    
        flush and self.flush() 
    pass

    def disp_full_number( self, number=0, fg=None, bg=None, flush=True) :
        debug = False
        
        from .TextNumber import numbers
        
        number = int(number)
        number = f"{number:d}"
        
        texts = numbers[0] 
        texts = texts.split( "\n" )
        
        if debug :
            for t in texts :
                print( f"***{t}***" )
            pass
        pass
    
        row = len( texts )        
        texts = [ '' ] * row
        
        debug and print( f"row = {row}" )
        
        c = len( number )
        if c >= 4 or c < 1 :
            c = 0
        else :
            c = 4 - c
        pass
    
        c = " " * c
        
        for n in number :
            n = int( n )
            
            debug and print( f"n = {n}" )
            
            n = numbers[ n ]
            n = n.split( "\n" )
            
            for i, (t1, t2) in enumerate( zip( texts, n ) ) :
                texts[i] = t1 + c + t2
            pass            
        pass
    
        if debug :
            for t in texts :
                print( f"***{t}***" )
            pass
        pass
    
        self.disp_full_text( texts, fg=fg, bg=bg, flush=flush)
    
        del numbers
    pass

    def disp_pairing_code( self, fg=None, bg=None, flush=True) :
        debug = False
        
        if bg is None : bg = self.black
        if fg is None : fg = self.yellow
        
        import random as my_random
        
        number = my_random.randint( 1000, 9999 )
        
        texts = f"{number}"
        
        self.disp_full_number( texts, fg=fg, bg=bg, flush=flush)
        
        del my_random
        
        return texts
    pass

pass

if __name__== '__main__' :
    # LCDPrintTest.py
    print( "Hello..." )
    
    lcd = LCD()
    lcd.flush() 
    
    pair_code = lcd.disp_pairing_code( flush=True )
    
    print( f"pari code = {pair_code}" )
    
    sleep( 1 )
elif __name__== '__main__' :
    # LCDPrintTest.py
    print( "Hello..." )
    
    lcd = LCD()
    lcd.flush() 
    
    lcd.disp_full_number( 7890, flush=True )
    
    sleep( 1 )
elif __name__== '__main__' :
    # LCDPrintTest.py
    print( "Hello..." )
    
    lcd = LCD()
    lcd.flush()
    
    sleep( 1 )
    
    lcd.disp_logo( flush=True )
elif __name__== '__main__' :
    # display tr sensor
    motor = Motor() 
    lcd = LCD()
    trs = TRSensor()
    
    lcd.disp_init(flush=1)
    
    # calibration
    motor.stop()
    
    sleep(3)
    
    for i in range(100) :
        if  25 < i <= 75:
            motor.set_motor( 30, -30, False )
        else:
            motor.set_motor(-30, 30, False )
        pass
    
        lcd.disp_motor( motor, flush=True )
    
        trs.calibrate()
    pass

    motor.stop()
    
    idx = 0 
    while True:
        idx += 1
        
        position, sensors = trs.readLine()        
        lcd.disp_tr_sensor( position, sensors, flush=True )
        
        #speeds = [ randint( -100, 100 ), randint( -100, 100 ) ]
        
        lcd.disp_motor( motor, flush=True )
        
        print( f"[{idx:4d}] position = {position:+.2f}, sensors = {sensors}" )
    
        sleep( 1 )
    pass
    
elif __name__== '__main__' :
    # display infrared sensor
    
    lcd = LCD()
    irSensor = IRSensor()
    
    lcd.disp_init() 
    
    idx = 0 
    while 1 :
        idx += 1
        blocks = irSensor.read_blocks()
        lcd.disp_ir_sensor( blocks, flush=True ) 
        
        print( f"[{idx:4d}] InfraRed LEFT: {blocks[0]}, RIGHT: {blocks[1]}" )
        
        sleep( 0.1)
    pass
elif __name__== '__main__' :
    # display ultra sonic
    
    lcd = LCD()
    ultraSonic = UltraSonic()
    
    lcd.disp_init()
    
    while 1 :
        dist = ultraSonic.obstacle_distance()
        lcd.disp_ultra_sonic( dist )
        lcd.flush()
        
        print( f"Distance = {dist:6.2f} cm" )
        sleep( 0.1)
    pass
elif __name__== '__main__' :
    # dispaly battery
    
    lcd = LCD()    
    battery = Battery()
    
    idx = 0
    while True :
        idx += 1
        
        values = [ temp, voltage, percent ] = battery.read()
        
        #values = [ temp,  voltage, randint( 0, 100 ) ] 
        
        lcd.disp_battery( values, 1 )
        lcd.flush()
        
        sleep( 1 )
    pass
pass

