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

[Setting]
	To use these codes, you should check you settings before running.
	(1) You must have set your MySQL server, and you should sure that it can be accessed by network or localhost;
	(2) Set up your python running environment, which is the baisc step.
	(3) In your database, there should have two tables( users and follows ) at least.
		And both of them should match the standard format. You can find them in the code, but good luck to you.
	(4) Check the configuration, for example:
	accessKey.conf
		line 1: 30218xxxxx ----Your Weibo developer App Key
		line 2: 4be8296fe17d5e5f6xxxxxxxxxxxxxxx ----App Secret
		line 3: https://api.weibo.com/oauth2/default.html ----App callback URL
	mark.conf
		line 1: 12 ----this number means that the program will begin with the 12nd ID in database
	server.conf
		line 1: 127.0.0.1 ----MySQL server IP
		line 2: root ----MySQL user name
		line 3: root ----MySQL password
		line 4: ai_hw ----the database's name
		line 5: utf8 ----coding format
		
[Run]
	You can directly run the main file--collect.py, or you can import it and use it as a subfunction( eg: collect.main() ).
	After you run these code, the program will require you to input the code from the popup. What you need to do is to copy the string after 'code=' and paste it to the python command window.
	Then press enter, the program will run automatically.
	However, for the strict control by sina, the program would stop in the middle. At this time, you should wait 5 or more minutes.
	After waitting, you can rerun the program without any settings.
