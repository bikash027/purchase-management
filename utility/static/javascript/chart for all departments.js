let labels=[];
function formChart(receivedData){
	labels=receivedData['departments']
	const backgroundColor= [
            'rgba(138, 43, 226, 0.6)',
            'rgba(165, 42, 42, 0.6)',
            'rgba(255, 127, 80, 0.6)',
            'rgba(220, 20, 60, 0.6)',
            'rgba(218, 165, 32, 0.6)',
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(240, 248, 255, 0.6)',
            'rgba(245, 245, 220, 0.6)',
            'rgba(255, 228, 196, 0.6)',
     ];
	const datasets=[];
	for(let i=0;i<receivedData['data'].length;i++){
		datasets.push({
			label: 'fund'+(i+1),
			backgroundColor: backgroundColor[i],
			data: receivedData['data'][i]
		})
	}
	const chartData={labels,datasets};

	const ctx= document.getElementById('myChart');
	const chart= new Chart(ctx, {
		type: 'horizontalBar',
		data: chartData,
		options: {
			title: {
				display: true,
				text: 'Fund Distribution for all departments'
			},
			tooltips: {
				mode: 'index',
				intersect: false
			},
			responsive: true,
			scales: {
				xAxes: [{
					stacked: true,
				}],
				yAxes: [{
					stacked: true
				}]
			},
			onClick: barClickHandler
		}
	});

}
function barClickHandler(event,array){
	window.location.href='/purchase-request/get_stats/department_fund/?id='+labels[array[0]._index];
}
formChart({data,departments});