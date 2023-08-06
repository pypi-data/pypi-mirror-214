from Motor import PicoGo
from UltraSonic import UltraSonic
from time import sleep

if __name__ == '__main__' :
    print( "Hello" )

    robot = PicoGo()
    ultraSonic = UltraSonic()
    
    duration = 0.02
    speed = 20
    max_dist = 18
    
    obstacle_cnt = 0 
    while True :
        dist = ultraSonic.obstacle_distance()
        
        print( f"distance = {dist:6.2f} cm" )
        
        if dist < max_dist :
            ostacle_cnt += 1
            
            if obstacle_cnt == 1 : 
                robot.stop()
                sleep( duration )
            
            robot.right( 2*speed )
        else:
            ostacle_cnt = 0 
            robot.forward( speed )
        pass
            
        sleep( duration )
    pass

    print( "Goodbye!" )
pass