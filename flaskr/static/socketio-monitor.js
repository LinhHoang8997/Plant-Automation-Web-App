$(document).ready(function(){
    var connection_url = 'http://' + document.domain + ':' + location.port + '/get_monitor_data';
    var socket = io.connect(connection_url);
//    console.log(connection_url);

    socket.on('connection response', function(response) {
        console.log(response);
        socket.emit('request-monitor-data');
        console.log("Request for data sent");
    });


    socket.on('data response', function(response) {
        console.log(response.message);
        if (response.all_data) {
            var monitor_data = JSON.parse(response.all_data);
            console.log(monitor_data);
        }
        if (response.plant_data) {
            var data_by_plant = JSON.parse(response.plant_data);
            console.log(data_by_plant);
        }

        //    REMEMBER TO Calculate percentages beforehand -> For both colors and tooltips

//            QUIRKY BAR CHART ONLY accepts certain fieldnames ("x" and "y")???
            new d3plus.BarChart()
              .select("#h_barchart_plant")
              .config({
                  data: data_by_plant,
                  x: "y",
                  y: "x",
                  ySort: function(a, b) {
                    return a["y"] - b["y"];
                  },
                  tooltipConfig: {
                    title: function(d) {
                        return d["y"];
                    }
                  },
                  shapeConfig: {
                    fill: 'gray',
                    Bar: {
                        labelConfig: {
                            fontFamily: "Calibri",
                            fontMin: 15,
                            fontMax: 30,
                            fontColor: '#ffffff'
                        }
                    }
                  },
                  yConfig: {
                    tickSize: 0,
                    gridConfig: {
                        opacity : 0
                    }
                  }
                })
             .discrete('y')
             .render();

            new d3plus.Pie()
                .select("#piechart_plottype")
                .config({
                    data: monitor_data,
                    groupBy: 'PlotTypeDescription',
                    value: function(d) {
                      return d["OutputSum"];
                    },
                    tooltipConfig: {
                        title: function(d) {
                            return d['OutputSum']
                        }
            //            tbody: [
            //                ["Total", function(d) { return d["Number of Food Stores"] }]
            //              ]
                }
                })
                 .render();


            new d3plus.Treemap()
                .select("#area_data_by_plot_chart")
                .data(monitor_data)
                .groupBy('PlotName')
            //    .sort('area')
                .sum('OutputSum')
                .shapeConfig({
            //        fill: function(d) {
            //            return d.color;    REMEMBER to use Python to get the percentage and calculate the color value before hand
            //        },
                    labelConfig: {
                      fontFamily: "calibri",
                      fontMax: 30
                    }
                })
                // Remember to explore onclick feature: https://d3plus.org/examples/d3plus-hierarchy/mouse-events/
                .render();
        });
});