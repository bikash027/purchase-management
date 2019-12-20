function formChart(){
	const labels=[]
	for(let i=0;i<fund_distributions.length;i++)
		labels.push(`fund${i+1}`);
	const datasets=[];
	datasets.push({
		label: 'fund remaining',
		backgroundColor:[
            'rgba(138, 43, 226, 1)',
            'rgba(165, 42, 42, 1)',
            'rgba(255, 127, 80, 1)',
            'rgba(220, 20, 60, 1)',
            'rgba(218, 165, 32, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(240, 248, 255, 1)',
            'rgba(245, 245, 220, 1)',
            'rgba(255, 228, 196, 1)',
     	],
		data: fund_distributions.map((dist)=>
			dist.totalAmountReceived-dist.fundUsed
		)
	});
	datasets.push({
		label: 'fund used',
		backgroundColor:[
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
     	],
		data: fund_distributions.map((dist)=>
			dist.fundUsed
		)
	});
	const chartData={labels,datasets};

	const ctx= document.getElementById('myChart');
	const chart= new Chart(ctx, {
		type: 'bar',
		data: chartData,
		options: {
			title: {
				display: true,
				text: 'Fund Distribution for '+deptId
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
			// onClick: barClickHandler
		}
	});

}
formChart();