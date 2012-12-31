# author: chenzhao 10389417
# version: 1.0

import MySQLdb

def getUids():
    try:
        serverFile = open( "server.conf", "r" )
        values = serverFile.readlines()
        serverConf = []
        for value2 in values:
            serverConf.append( value2.strip() )
            
        conn = MySQLdb.connect( host=serverConf[ 0 ], user=serverConf[ 1 ], passwd=serverConf[ 2 ], db=serverConf[ 3 ], charset=serverConf[ 4 ] )
        cursor = conn.cursor()
        
        cursor.execute( 'select * from users' )
        uids = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return uids
    except:
        print "Please check your MySQL database settings."
