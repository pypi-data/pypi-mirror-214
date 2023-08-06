def main_file_copy() :
    print( "main_file_copy" )

    file_path = "/main.py"
    
    file_read = None 
    try : 
        from picogo import main as mainFile
        import os        
        
        main_file_path = f"{mainFile.__file__}"
        
        print( f"main file path = {main_file_path}" )
        
        file_read = open( main_file_path, "r" )
    except Exception as e:
        file_read = None
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

main_file_copy()