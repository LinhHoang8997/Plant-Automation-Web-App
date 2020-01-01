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

//      Filter Object by Keys (key = index here) -> remove 13 entries so there is enough room
//        weather_data = weather_data.slice(1, weather_data.length - 13);

        var day = Object.values(weather_data['day']);
//        console.log(day);

        var month = Object.values(weather_data['month']);
//        console.log(month);

        var hour = Object.values(weather_data['hour']);
//        console.log(hour);

        var humidity_array = Object.values(weather_data['humidity']);
//        console.log(humidity_array);

        var humidity_temp = Object.values(weather_data['temperature']);
//        console.log(humidity_array);

        var data_label = []
        for (var i = 0; i < day.length; i++) {
            data_label.push("".concat(day[i],"/",month[i],"-Hour:",hour[i]))
        }
        console.log(data_label)

        var linec_humidity = new Chart(document.getElementById('line-chart-humidity'), {
              type: 'line',
              data: {
                labels: data_label,
                datasets: [{
                    data: humidity_array,
                    label: "Humidity"
                }]
             },
        });

        var linec_temperature = new Chart(document.getElementById('line-chart-temperature'), {
              type: 'line',
              data: {
                labels: data_label,
                datasets: [{
                    data: humidity_temp,
                    label: "Avg. Temperature"
                }]
             },
        });

    });
});


