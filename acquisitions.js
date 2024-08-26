(async function () {

    const rawData = JSON.parse(await (await fetch('http://127.0.0.1:5500/assets/Values.json')).text());
    const data = {
        datasets: [{
            label: 'Scatter Dataset',
            data: rawData,
            pointBackgroundColor: function(context) {
                const value = context.raw;
                return value.class == 'g' ? 'green' : 'red';
            }
        }],
    };
    const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    };
    new Chart(
        document.getElementById('acquisitions'),
        config
    );
})();
