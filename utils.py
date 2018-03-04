import sys 

def debug(message , e):
    print message, '{}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e


