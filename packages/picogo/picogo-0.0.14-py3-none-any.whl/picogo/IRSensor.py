from machine import Pin

class IRSensor :
    
    def __init__( self ) :
        self.dsr = Pin(2, Pin.IN)
        self.dsl = Pin(3, Pin.IN)
    pass

    def read_blocks( self ) :
        return [ self.dsl.value() == 0, self.dsr.value() == 0 ]   # left_block, right_block
    pass

pass