# Description
**AI homework:**

Based on Sina Weibo (<http://www.weibo.com>), dig out some information to build a plot and some pie graph for a star competitor.

We use splinter to get the webpage source and avoid the captcha.

While using splinter, the app will automatically keep popping out the browser and automatically close it. Meanwhile, users are supposed not to operate the computer in order to ensure the stability of splinter, especially not to operate the firefox browser popped out by the webdriver. 


-> _See docs in_ **ai_hw/doc**

-> _See structure in_ **ai_hw/treelist**, _Especially for TA!!_
#### Gain a better experience in reading README.md:   <https://github.com/Lhfcws/ai_hw/blob/master/README.md>
###This project can be downloaded on Github: <https://github.com/Lhfcws/ai_hw>

# Installation
### Strongly suggest you to run in Linux.
1. Make sure you have apache(or any server can run php), python 2.7.

2. Install splinter ( including lxml and selenium ) and MySQLdb for python.
	+ ####Linux(Strongly suggested):

		*Take Ubuntu as an example. Fedora and Arch are similar to this, Fedora may use "python-pip" instead of "pip".*

			sudo apt-get install python-lxml python-pip cython python-mysqldb python-pyquery python-numpy

			pip install splinter

			pip install jieba
	+ ####Windows(not recommend):

		Cython: 	<http://download.csdn.net/detail/feisan/4301293>

		lxml:		<http://lxml.de/>

		selenium:	<http://pypi.python.org/pypi/selenium/2.25.0#downloads>

		splinter:	<http://splinter.cobrateam.info/>

		mysqldb:	<http://mysql-python.sourceforge.net/>

		jieba:		<https://github.com/fxsjy/jieba>	

		pyquery:	<http://pypi.python.org/pypi/pyquery>

		numpy:		<http://www.scipy.org/>

		Download all above and install them for python on windows.

3. Install Firefox, make sure that the version is not too old.

# Run
### Strongly suggest you to run in Linux.
1. Edit src/server.conf as follow:

		line 1: hostname, use localhost if for test

		line 2: database username

		line 3: database password

2. Import src/ai_hw.sql. May be it's neccesary to create a DATABASE first.

3. Check the configuration in src/collect for weibo API module, for example:


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

4. **2 Demos:**				**(IMPORTANT)**

	1) Open liangbo.php to see the demo graph. [Without Running Python Scripts]

	2) Or after configuration well, you can do the following steps to go through the whole procedure. 

	>Input a star's name you wanted to know about.

	>After seeing the wait.php page, run generate.py to generate the data.

	>Then after **generate.py** finished, please run **generate1.py**. 

	   > _You may meet the captcha here, just open a search page in <http://s.weibo.com> (such as <http://s.weibo.com/weibo/ai>) and input the captcha by human.
	   Then run generate1.py again, it should be done!_

	>Go to **index.php** in Browser and input the star name again, it should show you **graph.php**, containing lines graph and pie graphs.

###The following steps are for the release version. We're sorry to tell you that now we just post the demo version.

5. Open index.php, make sure session can be used in your php.

6. Input a star's name you wanted to know about.

7. After seeing the wait.php page, run generate.py to generate the data.

8. Wait for a few minutes. (may be tens or more, depends on the amount of data and the network speed )

	*WARN: If you are running under your localhost, which means the python scripts are running in your PC, then keep patient and do not operate your computer while running! As the running time depends on your network speed and your main memory. And web driver is not stable, so sometimes it may somehow stop without any reason.*

9. You can directly run the main file -- **collect.py**, or you can import it and use it as a subfunction( eg: collect.main() ).

	After you run these code, the program will require you to input the code from the popup. What you need to do is to copy the string after 'code=' and paste it to the python command window.

	Then press enter, the program will run automatically.

	However, for the strict control by sina, the program would stop in the middle. At this time, you should wait 5 or more minutes.

	After waitting, you can rerun the program without any settings.

10. Finally, if all the data has been collected successfully, you can input the name again in the index.php. If the page show you "waiting", then the running is not finished; otherwise, it will show you graph.php which contains at least a lines graph and several pie graphs.
