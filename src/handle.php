<?php
	session_start();
	require_once("conf.php");
	$conn = mysql_connect($dbs[0], $dbs[1], $dbs[2]) or die("mysql connect failed!");
	$conn = mysql_select_db('ai_hw', $conn) or die("database select failed!");
	mysql_query("set names 'utf8'");

	$name = $_POST["name"];
	var_dump($name);
	$finish = false;
	$query = mysql_query("select * from `finish` where keyword='$name'");
	$finish = (mysql_num_rows($query) > 0);

	if ($finish){
		$_SESSION["keyword"] = $name;
		header("Location: graph.php");
	}
	else{
		$query = mysql_query("select * from `request` where keyword='$name'");
		if (mysql_num_rows($query) == 0)
			$query = mysql_query("INSERT INTO `request`(`id`, `keyword`) VALUES (0, '$name')") or die("insert keyword into database failed!");
		header("Location: wait.php");
	}
?>
