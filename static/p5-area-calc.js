let parentWidth;
let parentHeight;
let sunChartWidth;
let sunChartHeight;



var plot_canvas = new p5(function (p) {

  p.setup = function(){
    parentWidth = $("#canvas-parent").width();
    parentHeight = $("#canvas-parent").height();
    p.createCanvas(parentWidth, parentHeight);
    p.ellipseMode(p.CENTER);
  }

  p.draw = function() {
	p.background(155,153,143);
	for (var x = 0; x < p.width; x += p.width / 10) {
		for (var y = 0; y < p.height; y += p.height / 5) {
			p.stroke(0);
			p.strokeWeight(1);
			p.line(x, 0, x, p.height);
			p.line(0, y, p.width, y);

            if (x > 0 && y > 0 && x < p.width - 0.01 && y < p.height - 0.01) {
                p.fill(0);
                p.ellipse(x,y,35,35);
                p.fill(255);
                p.textAlign(p.CENTER, p.CENTER);
                p.text("X", x, y);
            }
		}
	}
    }

    p.windowResized = function(){
        parentWidth = $("#canvas-parent").width();
        parentHeight = $("#canvas-parent").height();
        p.resizeCanvas(parentWidth, parentHeight);
    }
}, "canvas-parent");

var sun_canvas = new p5(function (p) {
  p.setup = function(){
    sunChartWidth = $("#sun-angle-canvas").width();
    sunChartHeight = $("#sun-angle-canvas").height();
    p.createCanvas(sunChartWidth, sunChartHeight);
    p.ellipseMode(p.CENTER);
    p.hypothenuse = 250;
  }

  p.draw = function() {
	p.background(0);
	console.log(p.width/2);

	p.translate(p.width/2, p.height);
	p.stroke(200);
	p.strokeWeight(1.4);
	p.line(0,0,0,-p.height);
	p.fill(255);
	p.ellipse(0,0,40,40);
    p.months = calc_data_json.solar_months;
    p.ghi = calc_data_json.solar_ghi;

	if (p.months !== 0 && p.ghi !== 0) {
            p.months.forEach(function(item,index){
                let x = p.hypothenuse*p.sin(180-p.ghi[index]); // p.ghi[index] being the degrees compared to the Zenith
                let y = p.hypothenuse*p.cos(180-p.ghi[index]);
                p.noStroke();
                p.stroke(180);
                p.line(0,0,x,y);
                p.fill(255,227,119);
                p.ellipse(x,y, 40,40);
                p.fill(255);
	            p.ellipse(0,0,40,40);
            });
	    }
    }


    p.windowResized = function(){
        sunChartWidth = $("#sun-angle-canvas").width();
        sunChartHeight = $("#sun-angle-canvas").height();
        p.resizeCanvas(sunChartWidth, sunChartHeight);
    }
}, "sun-angle-canvas");


//  let sun_canvas = createCanvas(parentWidth,parentHeight/2.5)
//  sun_canvas.parent('#sun-canvas');
//  $(".placeholder-rock").css("display", "none");
