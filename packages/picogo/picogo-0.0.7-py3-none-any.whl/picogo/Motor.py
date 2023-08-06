from machine import Pin, PWM

class Motor(object):
    
    def __init__(self):
        self.PWMA = PWM(Pin(16))
        self.PWMA.freq(1000)
        self.PWMB = PWM(Pin(21))
        self.PWMB.freq(1000)
        
        self.AIN2 = Pin(17, Pin.OUT)
        self.AIN1 = Pin(18, Pin.OUT)
        self.BIN1 = Pin(19, Pin.OUT)
        self.BIN2 = Pin(20, Pin.OUT)        
        
        self.stop_cnt = 0
        self.speeds = [ 0, 0 ]
        self.stop()
    pass
            
    def forward(self, speed, verbose=False ):
        if 0 <= speed <= 100 :
            if verbose : print( f"forward: speed = {speed}" )
            self.set_motor( speed, speed )
        pass
    pass
        
    def backward(self, speed, verbose=False):
        if 0 <= speed <= 100 :
            if verbose : print( f"backward: speed = {speed}" )
            self.set_motor( -speed, -speed )
        pass
    pass

    def left(self,speed, verbose=False):
        if 0 <= speed <= 100 :
            if verbose : print( f"left: speed = {speed}" )
            self.set_motor( -speed, speed )
        pass
    pass
        
    def right(self, speed, verbose=False):
        if 0 <= speed <= 100 :
            if verbose: print( f"right: speed = {speed}" )
            self.set_motor( speed, -speed )
        pass
    pass
        
    def stop(self, verbose=False):
        if self.stop_cnt :
            if verbose : print( f"stop: speed = {0}" )
        pass
    
        self.stop_cnt += 1
        
        self.PWMA.duty_u16(0)
        self.PWMB.duty_u16(0)
        
        self.AIN2.value(0)
        self.AIN1.value(0)
        
        self.BIN2.value(0)
        self.BIN1.value(0)
    pass

    def move(self, left, right, verbose=True):
        self.set_motor( left, right, verbose )
    pass

    def set_motor(self, left, right, verbose=False):
        if verbose: print( f"set_motor: left = {left}, right = {right}" )
        
        self.speeds = [ left, right ]
        
        if 0 <= left <= 100 :
            self.AIN1.value(0)
            self.AIN2.value(1)
            self.PWMA.duty_u16(int(left*0xFFFF/100))
        elif -100 <= left <= 0 :
            self.AIN1.value(1)
            self.AIN2.value(0)
            self.PWMA.duty_u16(-int(left*0xFFFF/100))
        pass
    
        if 0 <= right <= 100 :
            self.BIN2.value(1)
            self.BIN1.value(0)
            self.PWMB.duty_u16(int(right*0xFFFF/100))
        elif -100 <= right <= 0 :
            self.BIN2.value(0)
            self.BIN1.value(1)
            self.PWMB.duty_u16(-int(right*0xFFFF/100))
        pass
    pass

pass