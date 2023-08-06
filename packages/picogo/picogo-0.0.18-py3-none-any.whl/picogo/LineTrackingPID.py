from time import sleep

from .TRSensor import TRSensor
from .Motor import PicoGo

if __name__ == '__main__' :
    print("TRSensor Test Program ...")
    sleep(3)
    robot = PicoGo()

    trs = TRSensor()
    for i in range(100):
        if  25 < i <= 75:
            robot.setMotor( 30, -30, False )
        else:
            robot.setMotor(-30, 30, False )
        pass
    
        trs.calibrate()
    pass

    robot.stop()

    print( "calibratedMin = ", trs.calibratedMin )
    print( "calibratedMax = ", trs.calibratedMax )
    print( "calibrate done!")
    print()
    
    sleep(5)

    maximum = 20
    integral = 0
    last_proportional = 0

    while True:
        position, sensors = trs.readLine()
        
        print( "position = ", position, ", Sensors = ", sensors )        
        
        # The "proportional" term should be 0 when we are on the line.
        proportional = position - 2000

        # Compute the derivative (change) and integral (sum) of the position.
        derivative = proportional - last_proportional
        integral += proportional

        # Remember the last position.
        last_proportional = proportional
        
        '''
        // Compute the difference between the two motor power settings,
        // m1 - m2.  If this is a positive number the robot will turn
        // to the right.  If it is a negative number, the robot will
        // turn to the left, and the magnitude of the number determines
        // the sharpness of the turn.  You can adjust the constants by which
        // the proportional, integral, and derivative terms are multiplied to
        // improve performance.
        '''
        power_diff = proportional/30  + derivative*2;  

        power_diff = max( -maximum, min( power_diff, maximum ) )
        
        if power_diff < 0 :
            robot.setMotor(maximum + power_diff, maximum)
        else:
            robot.setMotor(maximum, maximum - power_diff)
        pass 

    pass

pass