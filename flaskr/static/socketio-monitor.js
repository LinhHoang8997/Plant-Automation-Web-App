$(document).ready(function(){
    var plant_category;
    var output_by_plant;

//    var output_chart = new Chart(document.getElementById('h_barchart_plant'), {
//        type: 'horizontalBar',
//        data: {
//            labels: ["Yellow Bamboo","Clumping Bamboo","Ougon-Kouchiku","Reddish Bamboo"],
//            datasets: [{
//                label:"Output by Weight",
//                data: [12, 19, 3, 5]
//            }]
//        }
//      });

    var area_data_by_plot = [
        {plot_name:'A', area: 50},
        {plot_name:'B', area: 70},
        {plot_name:'C', area: 100},
        {plot_name:'D', area: 200}
    ]

    var data_by_plant = [
          {id: "Yellow Bamboo", x: "Yellow Bamboo", y: 7},
          {id: "Clumping Bamboo", x: "Clumping Bamboo", y: 25},
          {id: "Ougon-Kouchiku", x: "Ougon-Kouchiku", y: 13},
          {id: "Reddish Bamboo",  x: "Reddish Bamboo", y: 17},
    ];

    var data_by_plottype = [
        {plottype: "Greenhouse", output: 20},
        {plottype: "Greenhouse", output: 19},
        {plottype: "Standard", output: 8},
        {plottype: "Standard", output: 9}
    ]
//    REMEMBER TO Calculate percentages beforehand -> For both colors and tooltips

    new d3plus.BarChart()
      .select("#h_barchart_plant")
      .discrete("y")
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
     .render();

    new d3plus.Pie()
    .select("#piechart_plottype")
    .config({
        data: data_by_plottype,
        groupBy: "plottype",
        value: function(d) {
          return d["output"];
        },
        tooltipConfig: {
            title: function(d) {
                return d['output']
            }
//            tbody: [
//                ["Total", function(d) { return d["Number of Food Stores"] }]
//              ]
    }
    })
      .render();


    new d3plus.Treemap()
    .select("#area_data_by_plot_chart")
    .data(area_data_by_plot)
    .groupBy('plot_name')
//    .sort('area')
    .sum('area')
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