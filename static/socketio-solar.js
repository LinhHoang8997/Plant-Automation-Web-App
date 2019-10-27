$(document).ready(function(){
    var month_index = new Date().getMonth();
    console.log(month_index);


    var connection_url = 'http://' + document.domain + ':' + location.port + '/solar';
    var socket = io.connect(connection_url);
    console.log(connection_url);


    socket.on('connection response', function(msg) {
        console.log('received');
        console.log(msg);
    });

    $('#calc-submit-button').click(function(event) {
        socket.emit('request-solar-data', {data: $('#zipcode-solar').val()});
        console.log('Sent request to server for solar data');
        return false; /* Don't know what this does */
    });

    socket.on('data response', function(json) {
        console.log("JSON received");
        var solar_data = JSON.parse(json.data);
        console.log(solar_data);

        var month = Object.values(solar_data['Month']);
        var GHI = Object.values(solar_data['GHI']);
//         var DNI = Object.values(solar_data['DNI']);

        $("#this-month-sun").html(GHI[month_index] + " watts/m2");

        $("#solar-ghi-chart").css("display","block");
        var areac = new Chart(document.getElementById('solar-ghi-chart'), {
              type: 'line',
              data: {
                labels: month,
                datasets: [
                    {
                        data: GHI,
                        label: "GHI",
                        fill: "origin",
                        backgroundColor: '#ffffff',
                        borderColor: "gray",
                        pointStyle: 'rect',
                        radius: 5,
                        hoverRadius: 15,
                        hitRadius: 15
//                        One thing in the docs, one thing in StackOverflow
                    }
//                    ,
//                    {
//                        data: DNI,
//                        label: "DNI"
//                    }
                ]
             },
             options: {
                layout: {
                    padding: {
                        left: 10,
                        right: 0,
                        top: 0,
                        bottom: 0
                    }
                },
                legend: {
                    position: "top",
                    align: "end",
                    labels: {
                        fontColor: "white"
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: "white",
                            fontSize: 14
                        },
                        gridLines: {
                            color: "gray"
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            fontColor: "white",
                            fontSize: 18
//                            beginAtZero: true
                         }
                    }]
                }
             }
        });
   });
});

