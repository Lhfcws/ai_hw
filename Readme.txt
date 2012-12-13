[Description]
	In folder collect, there are 5 'py' files and 3 'conf' files.
	collect/
		accessKey.conf----set the sina weibo developer infomations
		mark.conf---------change that where will the program start at, 0 is set to start from the begining
		server.conf-------your MySQL server configuration
		
		collect.py--------main function: you can run it directly or use it as a subfunction ( eg: collect.main() )
		getAccess.py------get the authorization to use weibo API
		getUids.py--------get the weibo user IDs from your MySQL database
		setFollows.py-----store the user's detail message into MySQL database
		weibo.py----------weibo library
		