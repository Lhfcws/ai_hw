<?php
/*
	function die($st) {
		die($st + "</br>");	
	}
 */
	session_start();
	require_once("conf.php");
	$conn = mysql_connect($dbs[0], $dbs[1], $dbs[2]) or die("mysql connect failed!");
	$conn = mysql_select_db('ai_hw', $conn) or die("database select failed!");
	mysql_query("set names 'utf8'");
	$keyword = $_SESSION["keyword"];
	$query = mysql_query("select * from plots where keyword='$keyword'") or die("select plots failed!");
	$arr = array();
	$dat = array();

	while ($row = mysql_fetch_row($query)) {
		array_push($arr, $row[0]);
		array_push($dat, $row[1]);

	}
	$plots = json_encode($dat);
	foreach ($arr as $k=>$s) {
		$arr[$k] = (int)($s);
	}
	$stat = json_encode($arr);
	
	$gender = array(array('female', 0),array('male', 0));
	$query = mysql_query("select * from follows where keyword = '$keyword'") or die("select follows failed!");
	while ($row = mysql_fetch_row($query)) {
		# GENDER
		if ($row[2] == 'f')
			$gender[0][1] += 1;
		else
			$gender[1][1] += 1;

		#PROVINCE
		$p = $row[7];
		if ($tp_pr[$p] == null)
			$tp_pr[$p] = 1;
		else $tp_pr[$p]++;
	}
	
	$s = $gender[0][1] + $gender[1][1];
	$gender[0][1] = $gender[0][1] * 100 / $s;
	$gender[1][1] = $gender[1][1] * 100 / $s;
	$gender = json_encode($gender);
	# province
	$pr = array();
	$pr_sum = 0;
	foreach ($tp_pr as $k=>$v) {
		$temp = array($k, (int)$v);
		$pr_sum += $v;
		array_push($pr, $temp);
	}
	$pr = json_encode($pr);
	#love music
	$ml = array();
	$ml_sum = 0;
	$query = mysql_query("select * from music_love where keyword='$keyword'") or die('love music select failed');
	while ($row = mysql_fetch_row($query)) {
		$temp = array();
		$m = "love";
		array_push($temp,$m);
		$m = (float)$row[1]/(float)$row[0] * 100;
		array_push($temp,$m);
		array_push($ml, $temp);
		$temp = array();
		$m = "others";
		array_push($temp,$m);
		$m = ((int)$row[0] - (int)$row[1]) / (float)$row[0] * 100;
		array_push($temp,$m);
		array_push($ml, $temp);
	}

	$ml = json_encode($ml);
?>
