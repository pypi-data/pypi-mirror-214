def copy() :
    print( "main_file_copy" )

    file_path = "/main.py"
    
    file_read = None 
    
    try : 
        main_file_path = "/lib/picogo/main.py" 
        
        print( f"main file path = {main_file_path}" )
        
        file_read = open( main_file_path, "r" )
    except Exception as e:
        print( f"cannot find main file : {main_file_path}" )
        
        file_read = None
    pass

    if file_read is None :
        try : 
            main_file_path = "/picogo/main.py" 
            
            print( f"main file path = {main_file_path}" )
            
            file_read = open( main_file_path, "r" )
        except Exception as e:
            print( f"cannot find main file : {main_file_path}" )
            
            file_read = None
        pass
    pass

    if file_read is None :
        print( "cannot find main file" )
        print( "Filed to copy main file." )
    elif file_read is not None :
        file = open( file_path, "w" ) 
        
        for line in file_read.readlines() :
            file.write( line )
        pass
                    
        file_read.close()
        file.close()
        
        print( "Success main file copy" )
    pass
pass

copy()