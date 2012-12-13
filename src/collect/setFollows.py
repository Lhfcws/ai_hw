# author: chenzhao 10389417
# version: 1.0

import MySQLdb

def setFollows( user, key ):
    try:
        serverFile = open( "server.conf", "r" )
        values = serverFile.readlines()
        serverConf = []
        for value2 in values:
            serverConf.append( value2.strip() )
            
        conn = MySQLdb.connect( host=serverConf[ 0 ], user=serverConf[ 1 ], passwd=serverConf[ 2 ], db=serverConf[ 3 ], charset=serverConf[ 4 ] )
        cursor = conn.cursor()

        value = [ user[ 'id' ], user[ 'screen_name' ], user[ 'gender' ], user[ 'followers_count' ], user[ 'lang' ], user[ 'verified' ], user[ 'url' ], user[ 'province' ], user[ 'city' ], key ]
        cursor.execute( "insert into follows( id, name, gender, follower, language, verified, url, province, city, keyword ) value( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", value )
        conn.commit();
        
        cursor.close()
        conn.close()
    except Exception, e:
        print e
