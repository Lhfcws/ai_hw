<?php
$file = fopen("server.conf", "r") or exit("Unable to open server.conf !");
//Output a line of the file until the end is reached
$dbs = array();
while(!feof($file))
{
	$temp = fgets($file);

	array_push($dbs, trim($temp));
}
fclose($file);
?>
