def main_file_copy() :
    print( "main_file_copy" )

    file_exist = True
    file_path = "/main.py"
    
    try:
        f = open( file_path, "r" )
        f.close() 
    except Exception as e: 
        file_exist = False
    pass
    
    if not file_exist :
        file_read = None 
        try : 
            from picogo import main as mainFile
            import os        
            
            main_file_path = mainFile.__file__
            
            print( f"main file path = {main_file_path}" )
            
            file_read = open( os.path.abspath( main_file_path ), "r" )
        except Exception as e:
            file_read = None
        pass
    
        if file_read is None :
            print( "cannot file main file" )
            print( "Filed to copy main file." )
        elif file_read is not None :
            file = open( file_path, "w" ) 
            
            file.writeline( file_read.readlines() )
                        
            file_read.close()
            file.close()
            
            print( "Done. main file copy." )
        pass
    pass
pass

main_file_copy()