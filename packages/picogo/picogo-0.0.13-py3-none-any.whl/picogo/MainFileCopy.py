def main_file_copy() :
    print( "main_file_copy" )

    file_exist = True
    file_name = "/main.py"
    
    try:
        f = open( file_name, "r" )
        f.close()
        # continue with the file.
    except OSError:  # open failed
        # handle the file open case
        file_exist = False
    pass
    
    if not file_exist :
        file = open( file_name, "w" )
        file_content = """
if __name__== '__main__' :

print( 'Hello PicoGo!' )
print( 'Running Bluetooth program ... ' )

from picogo import BlueTooth

BlueTooth.main()

print( 'Good bye!' )    
pass
        """
        file.write( file_content )
        file.close()
        
        print( "Done. main_file_copy" )
    pass
pass

main_file_copy()