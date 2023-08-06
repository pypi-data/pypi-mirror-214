from time import sleep, sleep_ms

from .Motor import PicoGo
from .TRSensor import TRSensor
from .LCD import LCD

if __name__ == '__main__':

    print( "TRSensor Test ... \n" )
    
    lcd = LCD()
    lcd.disp_init(flush=1)
    
    trs = TRSensor()
    
    print( "center position = ", trs.center_position() )
    
    if True :
        sleep(3) 
        
        robot = PicoGo()
        
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
        print( "calibrate done! \n" ) 
    else :
        trs.calibrate()
    pass
    
    idx = 0 
    while True:
        idx += 1
        position, sensors = trs.readLine()
        
        lcd.disp_tr_sensor( position, sensors, flush=1 ) 
        
        print( f"[{idx:4d}] position = {position:+.2f}, sensors = {sensors}" )            
        
    
        sleep( 1 )
    pass

pass 