<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<style>
		body{
			background: #e3e3e3;
			text-align: center;
			font-family: Georgia;
		}
		a{
			text-decoration: none;
		}
		a:hover{
			text-decoration: underline;
		}
		table{
			margin: 0 auto;
		}
		span{
			color: #ff0000;
			font-weight: 700;
		}
		ul{
			width: 400px;
			margin: 0 auto;
			list-style-type: decimal;
			font-family: Georgia,Serif;
			text-align: left;
		}
	</style>
	<title>选秀节目数据抓取与分析</title> <!-- Web name -->
</head>
<body>
	<h1>选秀节目数据抓取与分析</h1><!-- Title -->
	<h2>——基于新浪微博应用的信息分类方法</h2>
	<h4>---Rleased by--- <br /> ---赵哲民、吴文杰、陈潇楠、陈照、蔡志杰---</h4>
	<br /><br />
	<ul>
		<li>注意到下面的文本框了吗？请在里面<span>输入选手名字</span>~</li>
		<br /><li>请您务必注意要<span>耐心等候</span>，在此期间<span>不要对浏览器进行其他操作</span>，以免出错！</li>
		<br /><li>在后台程序运行完毕之后，您就可以看到选手粉丝<span>个人信息的分布情况</span>了！</li>
	</ul><!-- Tips -->
	<br /><br />
	<hr/>
	<form method="post" action="handle.php">
	<table>
		<tr>
			<td>
				Name: &nbsp &nbsp
			</td>
			<td>
				<input type="text" name="name" size="35" placeholder="please input the competitor's name"/>
			</td>
			<td>
				<input type="submit" />
			</td>
		</tr>
	</table>
	<hr/>
	<h2>See <a href="liangbo.php">Demo</a></h2>
</form>
</body>
</html>
