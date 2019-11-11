$(document).ready(function(){
    var weather_data;

    var connection_url = 'http://' + document.domain + ':' + location.port + '/weather';
    var socket = io.connect(connection_url);
    console.log(connection_url);

    socket.on('connection response', function(msg) {
        console.log('received');
        console.log(msg);
    });

    $('#clickJSON').click(function(event) {
        socket.emit('request-weather-data', {data: $('#zipcode-weather').val()});
        console.log('Sent request to server for weather data');
        return false; /* Don't know what this does */
    });
    socket.on('data response', function(json) {
        console.log("JSON received");
        weather_data = JSON.parse(json.data);
        var humidity_index = Object.values(weather_data['day']);
//        console.log(humidity_index);
        var humidity_array = Object.values(weather_data['humidity']);
//        console.log(humidity_array);

        var linec = new Chart(document.getElementById('line-chart'), {
              type: 'line',
              data: {
                labels: humidity_index,
                datasets: [{
                    data: humidity_array,
                    label: "Humidity"
                }]
             },
        });

    });
});


