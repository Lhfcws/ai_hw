# author: chenzhao 10389417
# version: 1.0

import sys
import webbrowser
import urllib, httplib
import os
path = os.path.dirname(__file__)

from weibo import APIClient

def getAccess():
    ACCOUNT = "ai2012_go@126.com"
    PASSWORD = "aiai2012"
    
    # get configure from file
    accessFile = open( path+"/accessKey.conf", "r" )
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
        # webbrowser.open_new( client.get_authorize_url() )
        url = client.get_authorize_url()
        conn = httplib.HTTPSConnection('api.weibo.com')
        postdata = urllib.urlencode({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':ACCOUNT,'passwd':PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
        conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
        res = conn.getresponse()
        location = res.getheader('location')
        code = location.split('=')[1]
        conn.close()
        
        r = client.request_access_token( code )
        client.set_access_token( r.access_token, r.expires_in )
        return client
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
