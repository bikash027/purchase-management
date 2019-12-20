function httpGetAsync(theUrl, callback){
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.response);
    }
    xmlHttp.responseType='json';
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}
const deptId=document.getElementById('deptId').textContent;
const amount=parseInt(document.getElementById('amount').textContent);
const ctx = document.getElementById('myChart').getContext('2d');
function formChart(fundData){
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['fund remaining', 'fund required', 'fund required by all'],
            datasets: [{
                label: 'Amount in Rs',
                data: [
                    fundData['fund remaining'],
                    amount,
                    fundData['fund required total']
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1
            }]
        },
        /*options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }*/
    });
    if(amount>fundData['fund remaining']){
        document.getElementById('forward').lastElementChild.style.display='none';
    }
}
httpGetAsync("/purchase-request/get_stats/department_fund_summary?id="+deptId,formChart);
