from time import sleep 

from .Motor import Motor

if __name__== '__main__' :
    motor = Motor()
    
    duration = 1
    
    motor.forward(30)
    sleep(duration)
    
    motor.backward(30)
    sleep(duration)
    
    motor.left(30)
    sleep(duration)
    
    motor.right(30)
    sleep(duration)
    
    motor.stop()
    sleep(duration)
pass