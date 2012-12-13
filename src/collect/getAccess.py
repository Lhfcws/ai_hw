# author: chenzhao 10389417
# version: 1.0

import sys
import webbrowser

from weibo import APIClient

def getAccess():
    # get configure from file
    accessFile = open( "accessKey.conf", "r" )
    values = accessFile.readlines()
    accessFile.close()

    accessKeys = []
    for value in values:
        accessKeys.append( value.strip() )

    # get the weibo authorization
    try:
        APP_KEY = accessKeys[ 0 ]
        APP_SECRET = accessKeys[ 1 ]
        CALLBACK_URL = accessKeys[ 2 ]

        client = APIClient( app_key = APP_KEY, app_secret = APP_SECRET, redirect_uri = CALLBACK_URL )
        webbrowser.open_new( client.get_authorize_url() )
        
        r = client.request_access_token( raw_input( "Input CODE:" ) )
        client.set_access_token( r.access_token, r.expires_in )
        return client
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
