from machine import Pin
from time import sleep

from .Motor import Motor
from .UltraSonic import UltraSonic

if __name__ == '__main__' :

    motor = Motor()
    ultraSonic = UltraSonic()
    
    dsr = Pin(2, Pin.IN)
    dsl = Pin(3, Pin.IN)
    
    duration = 0.02
    speed = 20
    max_dist = 18
    
    left_block = False
    right_block = False 
    obstacle_cnt = 0
        
    while True:
        dist = ultraSonic.obstacle_distance()
        
        left_block = ( dsr.value() == 0 )
        right_block = ( dsl.value()== 0 )
        
        if dist < max_dist or left_block or right_block == 0 :
            obstacle_cnt += 1
        pass
    
        if obstacle_cnt == 1 :
            motor.stop()
            sleep( duration)
        pass
    
        if left_block and right_block : # 양쪽에 장애물이 있을 때, 좌회전
            motor.left( speed )
            sleep( 5*duration )
        elif left_block :   # 좌측 장애물시, 우회전
            motor.right( speed )
            sleep( 5*duration )
        elif right_block :  # 우측 장애물시, 좌회전
            motor.left( speed )
            sleep( 5*duration )
        if dist < max_dist : # 전방 장애물 있을 경우, 좌회전 
            motor.left( speed )
            sleep( 5*duration )        
        else :              # 장매물이 없으면, 전진
            obstacle_cnt = 0 
            motor.forward( speed )
            sleep( duration )
        pass
    pass

pass
