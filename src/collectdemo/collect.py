# author: chenzhao 10389417
# version: 1.0

import sys
import string

from getAccess import getAccess
from getUids import getUids
from setFollows import setFollows
import os
path = os.path.dirname(__file__)

def main():
    # get access client
    client = getAccess()
    uids = getUids()
    tempMark = 0

    mark = open( path+"/mark.conf", "r" )
    start = string.atoi( mark.readline() )
    mark.close()
    try:
        for uid in uids:
            tempMark += 1
            if tempMark > 50:
                break
            
            # handle the ids
            print uid[ 0 ] + " is doing..."
            userId = string.atoi( uid[ 0 ] )
            userInfo = client.get.users__show( uid = userId )
            setFollows( userInfo, uid[ 1 ] )
            print "done."
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
    mark = open( "mark.conf", "w" )
    mark.write( repr( tempMark + 1 ) )
    mark.close()

if __name__ == '__main__':
    main()
