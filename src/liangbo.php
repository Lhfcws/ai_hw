<?php 
	require_once("model_liangbo.php");
?>
<!doctype html>
<html>
<head>
<title>选秀明星关注率走势</title>
<meta charset="utf-8">
<script src="highchart/jquery.min.js"></script>
<script src="highchart/js/highcharts.js"></script>
<script type="text/javascript">
	var chart,pie1;
	var date_prefix = '2012-09-';
	var dateArr = eval(<?=$plots?>);
	var stat = eval(<?=$stat?>);
	/*
	for (var i=1;i<=30;i++) {
		if (i<10) {
			dateArr.push(date_prefix+'0'+i);
		}
		else {
			dateArr.push(date_prefix+i);
		}
	}*/

	$(document).ready(function(){
		chart = new Highcharts.Chart({
			chart: {
				renderTo: 'container',
				defaultSeriesType: 'line'
			},
			title:{
				text: '中国好声音新浪微博关注率走势图',
				x: -20
			},
			subtitle:{
				text: 'Produced by Group 11',
				x: -20
			},
			xAxis:{
				categories: <?=$plots?>
			},
			yAxis:{
				title:{
					text: '关注人数'
				},
				plotLines: [{
					value: 0,
					width: 1,
					color: '#808080'
				}]
			},
			plotOptions: {
				line: {
					dataLabels: {
						enabled: true			
					}
				} 
			},
			series: [{
				name: '梁博',
				data: <?=$stat?>
			}]
		});			
				pie1 = new Highcharts.Chart({
            chart: {
                renderTo: 'container1',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '关注用户的性别分布'
            },
            tooltip: {
        	    pointFormat: '{series.name}: <b>{point.percentage}%</b>',
            	percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>'+ this.point.name +'</b>: '+ Highcharts.numberFormat(this.percentage, 2) +' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: '性别分布',
                data: <?=$gender?>
            }]
        });
	});
</script>
</head>
<body>
<div id="container" style="width: 1300px;height: 800px; margin: 0 auto;"></div>
<div id="container1" style="width: 660px;height: 600px; margin: 0 auto;"></div>
</body>
</html>
