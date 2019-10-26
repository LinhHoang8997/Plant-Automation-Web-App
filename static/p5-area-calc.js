var parentWidth;
var parentHeight;

function setup() {
  // We are still calling createCanvas like in the past, but now
  // we are storing the result as a variable. This way we can
  // call methods of the element, to set the position for instance.
  parentWidth = $("#canvas-parent").width();
  parentHeight = $("#canvas-parent").height();
  ellipseMode(CENTER);
  let canvas = createCanvas(parentWidth, parentHeight);
  canvas.parent('#canvas-parent');
//  $(".placeholder-rock").css("display", "none");
}

  // Here we call methods of each element to set the position
  // and id, try changing these values.
  // Use the inspector to look at the HTML generated from this
  // code when you load the sketch in your browser.
//  canvas.position(300, 50);
//  canvas.class("lemon");

function draw() {
	background(220);


	for (var x = 0; x < width - 0.01; x += width / 10) {
		for (var y = 0; y < height - 0.01; y += height / 5) {
			stroke(0);
			strokeWeight(1);
			line(x, 0, x, height);
			line(0, y, width, y);
      if (x > 0 && y > 0) {
        fill(0);
        ellipse(x,y,35,35);
        fill(255);
        textAlign(CENTER, CENTER);
        text("X", x, y);
      }
		}
	}
}

function windowResized() {
  parentWidth = $("#canvas-parent").width();
  parentHeight = $("#canvas-parent").height();
  resizeCanvas(parentWidth, parentHeight);
}
