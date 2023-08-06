if __name__== '__main__' :
    from time import sleep
    from machine import Pin

    led = Pin(25, Pin.OUT)

    print( "Hello ...." )

    for i in range( 100 ) :
        print( f"[{i}] LED blink" )
        led.toggle()
        sleep(0.5)
    pass

    print( "Goodbye" )
pass