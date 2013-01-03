# author: chenzhao 10389417
# version: 1.0

import MySQLdb
import os
path = os.path.dirname(__file__)

def getUids():
    try:
        serverFile = open( path+"/server.conf", "r" )
        values = serverFile.readlines()
        serverConf = []
        for value2 in values:
            serverConf.append( value2.strip() )
            
        conn = MySQLdb.connect( host=serverConf[ 0 ], user=serverConf[ 1 ], passwd=serverConf[ 2 ], db=serverConf[ 3 ], charset=serverConf[ 4 ] )
        cursor = conn.cursor()
        
		
        cursor.execute("select * from request order by id DESC limit 1")
        ls = cursor.fetchall()
        keyword = ls[0][1]

        cursor.execute( "select * from users where keyword='"+keyword+"'" )
        uids = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return uids
    except:
        print "Please check your MySQL database settings."
