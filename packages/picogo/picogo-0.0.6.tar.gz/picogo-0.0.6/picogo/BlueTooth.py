import machine
import ujson, utime

from .Robot import Robot

class BlueTooth :
    def __init__( self ):
        print( "Hello ... Bluetooth!" )
        
        self.robot = Robot()
        self.uart = self.robot.uart
        
        self.init_bluetooth()
    pass

    def init_bluetooth( self ) :
        robot = self.robot
        
        rgbLed = robot.rgbLed
        color = ( 0, 0, 0 )
        rgbLed.set_color( color )
                
    pass

    def send_reply( self, request_no, reply ) :
        uart = self.uart
        
        reply = f"{request_no}:{reply}\n"
        
        uart.write( reply )
        
        if not uart.txdone() :
            uart.flush()
        pass
        
        reply_len = len( reply )
        reply = reply.replace( "\n", "\\n" )
        
        print( f"send request_no: {request_no}, reply : '{reply}', len : {reply_len}" )
    pass

    def process_json_cmd( self, s, robot ) :
        reply = None
        
        try :
            reply = self.process_json_cmd_impl( s, robot )
        except Exception as e :
            print( e ) 
        pass
    
        return reply
    pass
    
    def process_json_cmd_impl( self, json, robot ) :
        reply = None
        
        uart = robot.uart
        
        motor = robot.motor
        rgbLed = robot.rgbLed
        buzzer = robot.buzzer
        led = robot.led
        
        speed = robot.speed
        
        cmd = json.get("Forward")
        
        if cmd != None:
            if cmd == "Down":
                motor.forward(speed, verbose=True)
                reply = "ok"
            elif cmd == "Up":
                motor.stop()
                reply = "ok"
            pass
        pass
                
        cmd = json.get("Backward")
        if cmd != None:
            if cmd == "Down":
                motor.backward(speed)
                reply = "ok"
            elif cmd == "Up":
                motor.stop()
                reply = "ok"
            pass
        pass
         
        cmd = json.get("Left")
        if cmd != None:
            if cmd == "Down":
                motor.left(20)
                reply = "ok"
            elif cmd == "Up":
                motor.stop()
                reply = "ok"
            pass
        pass
                 
        cmd = json.get("Right")
        if cmd != None:
            if cmd == "Down":
                motor.right(20)
                reply = "ok"
            elif cmd == "Up":
                motor.stop()
                reply = "ok"
            pass
        pass
      
        cmd = json.get("Low")
        if cmd == "Down":
            robot.speed = robot.low_speed
            reply = "ok"
        pass

        cmd = json.get("Medium")
        if cmd == "Down":
            robot.speed = robot.med_speed
            reply = "ok"
        pass

        cmd = json.get("High")
        if cmd == "Down":
            robot.speed = robot.high_speed
            reply = "ok"
        pass
        
        cmd = json.get("BZ")
        if cmd != None:
            if cmd == "on":
                buzzer.value(1)
                reply = "ok"
            elif cmd == "off":
                buzzer.value(0)
                reply = "ok"
            pass
        pass
        
        cmd = json.get("LED")
        if cmd != None:
            if cmd == "on":
                led.value(1)
                reply = "ok"
            elif cmd == "off":
                led.value(0)
                reply = "ok"
            pass
        pass
        
        cmd = json.get("RGB")
        if cmd != None:
            rgb = tuple( eval(cmd) )
            
            rgbLed.set_color( rgb )
            
            reply = "ok"
        pass
    
        if reply is None :
            reply = "bad"
        pass
    
        return reply
    pass

    def process_text_cmd( self, s, robot ) :
        reply = None
        
        try :
            reply = self.process_text_cmd_impl( s, robot )
        except Exception as e :
            print( e )
        pass
    
        return reply
    pass

    def process_text_cmd_impl( self, s, robot ) :
        reply = None
        
        if "hello" in s :
            reply = "ok"
        elif "send me pairing code" in s :
            print( f"processing pairing code" )
            
            pair_code = robot.lcd.disp_pairing_code( flush=True )
            
            print( f"pair code = {pair_code}" )
            
            reply = f"pair code: {pair_code}"  
        else :
            print( f"Unknown command = [{s}]" )
            
            reply = "Unknown code"
        pass
    
        return reply
    pass

    def read_bytes( self, uart, nbytes ) :
        byte_list = bytearray( nbytes )
            
        i = 0 
        while i < nbytes : 
            b = uart.read( 1 )
            if b :
                byte_list[ i ] = b[ 0 ]
                i += 1
            pass
        pass

        if nbytes == 1 :
            return byte_list[ 0 ]
        else :
            return byte_list
        pass
    pass
            
    def main( self ) :
        print( "Ready to accept!" )
        
        t = 0
        count = 0 

        robot = self.robot

        uart = robot.uart

        head_read_count = 0
        
        while True :
            debug = True
            
            data_type = 0
            data_len  = 0
                
            # read data type and data len
            while data_type == 0 :
                head_read_count += 1
                
                request_no = 0
                
                debug and print( f"[{head_read_count:04d}] reading sart of heading ..." )
                start_of_heading = self.read_bytes( uart, 1 )
                debug and print( f"[{head_read_count:04d}] start of heading = {start_of_heading}" )
                
                if start_of_heading != 1 :
                    data_type = 0
                    data_len  = 0
                elif start_of_heading == 1 : # start of heading
                    # read read request_no
                    if True : 
                        byte_list = self.read_bytes( uart, 2 )
                        
                        request_no = 0
                        for b in byte_list :
                            request_no = data_len*255 + b
                        pass
                    pass
                
                    # read data type
                    data_type = self.read_bytes( uart, 1 ) 
                    
                    # read data_len
                    if data_type : 
                        byte_list = self.read_bytes( uart, 2 )
                        
                        data_len = 0
                        for b in byte_list :
                            data_len = data_len*255 + b
                        pass
                    pass
                pass
            pass

            print( f"request_no = {request_no}, date_type = {data_type}, data_len = {data_len}" )

            # reate data
            data = None
            
            if data_len > 0 :
                data = self.read_bytes( uart, data_len )  
            else :
                data = None
            pass

            # read end of transmission
            if data != None : 
                end_of_transmission = self.read_bytes( uart, 1 )  
            
                if end_of_transmission != 4 : # End of Transmission
                    data = None
                pass 
            pass

            if data : 
                s = data.decode()
            pass
            
            if s != None :
                count += 1
                
                print( f"[{count:04d}] s = [{s}]" )                
                
                reply = None
                
                json = None
                    
                try : 
                    json = ujson.loads(s)
                except Exception as e:
                    #print( e )
                    pass
                pass
    
                if json != None :
                    print( "json =" , json )
    
                    reply = self.process_json_cmd( json, robot )
                elif s != None :
                    reply = self.process_text_cmd( s, robot )
                pass
            
                if reply is None :
                    reply = "Unknown code"
                pass
            
                if reply != None :
                    self.send_reply( request_no, reply )
                pass
            pass
            
            if s != None and (utime.ticks_ms() - t) > 3000 :
                showMsg = False
                if showMsg :
                    t = utime.ticks_ms()
                    
                    text = f"PicoGo\n{count}"
                    
                    robot.lcd.disp_full_text( text )
                    robot.lcd.show()
                pass
            pass

        pass
    pass

pass

def main() :
    blueTooth = BlueTooth()
    blueTooth.main()
pass

if __name__ == '__main__' :
    main()
pass
    