// Get a reference to the canvas
var canvas = document.getElementById("dungeon_map");
// store the 2D rendering context in ctx
var ctx    = canvas.getContext("2d");

// store the information on which key has the user pressed
var rightPressed = false;
var leftPressed = false;

// Define the ball
var ballRadius = 10;
var x = canvas.width/2;
var y = canvas.height-30;
var dx = 6;
var dy = -6;

// Define the paddle
var paddleHeight = 10;
var paddleWidth  = 75;
var paddleX = (canvas.width - paddleWidth)/2; //starting point

//track the score
var score = 0;

// handle the keystrokes
// when a key is pressed (or released) the following two functions are called by 
// the "event listener" :
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
function keyDownHandler(e) {
   if (e.keyCode == 39) {
      rightPressed = true;
   } else if (e.keyCode == 37) {
      leftPressed = true;
   }
}

function keyUpHandler(e) {
   if (e.keyCode == 39) {
      rightPressed = false;
   } else if (e.keyCode == 37) {
      leftPressed = false;
   }
}


//We can add mouse control as well!
document.addEventListener("mousemove", mouseMoveHandler, false);
function mouseMoveHandler(e) {
   var relativeX = e.clientX - canvas.offsetLeft;
   if (relativeX > 0 && relativeX < canvas.width) {
      paddleX = relativeX - paddleWidth/2;
   }
}


// let set up the bricks!
var brickRowCount = 3;
var brickColumnCount = 5;
var brickWidth = 75;
var brickHeight = 20;
var brickPadding = 10;
var brickOffsetTop = 30;
var brickOffsetLeft = 30;

var bricks = [];
for(c=0; c<brickColumnCount; c++) {
bricks[c] = [];
for(r=0; r<brickRowCount; r++) {
      // let's add an extra parameter to the brick
      // to see whether they are active or not
   bricks[c][r] = { x: 0, y: 0, status: 1};
}
}

// loop over the brick array and draw them on screen!
function drawBricks() {
   var bricksLeft = false;
for(c=0; c<brickColumnCount; c++) {
   for(r=0; r<brickRowCount; r++) {
      var brickX = (c*(brickWidth + brickPadding)) + brickOffsetLeft;
            var brickY = (r*(brickHeight + brickPadding)) + brickOffsetTop;
            if (bricks[c][r].status == 0) continue;
      bricks[c][r].x = brickX;
      bricks[c][r].y = brickY;
      ctx.beginPath();
      ctx.rect(brickX, brickY, brickWidth, brickHeight);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
            bricksLeft = true;
   }
}
   if (!bricksLeft) {
      alert("You won! Congratulations!");
      document.location.reload();
   }
}

// Now we also need a colission detection function!
function collisionDetection() {
for(c=0; c<brickColumnCount; c++) {
   for(r=0; r<brickRowCount; r++) {
            var b = bricks[c][r];
            // if the x/y position of the ball is inside the brick, then we collide
            // and the ball gets "bounced back"
            if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y +brickHeight && b.status == 1) {
               dy = -dy ;
               b.status = 0;
               bricks[c][r] = b;
               score++;
            }
      }
   }
}
   

function drawPaddle() {
   ctx.beginPath();
   ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
   ctx.fillStyle = "#0095DD";
   ctx.fill();
   ctx.closePath();
}

function drawBall() {
   ctx.beginPath();
   ctx.arc(x, y, ballRadius, 0, Math.PI*2);
   ctx.fillStyle = "#0095DD";
   ctx.fill();
   ctx.closePath();
}

function drawScore() {
   ctx.font = "16px Arial";
   ctx.fillStyle = "#0095DD";
   ctx.fillText("Score: " + score, 8, 20);
}

function draw() {
   ctx.clearRect(0,0,canvas.width, canvas.height);
   drawBall();
   drawPaddle();
   drawBricks();
   collisionDetection();
   drawScore();

   if (dy == 0) dy = 4;

   if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) {
   dx = -dx;
}
if(y + dy < ballRadius) {
   dy = -dy;
   } else if (y + dy > canvas.height-ballRadius) {
      // I've removed the gameover because it's annoying
      // but if the ball "escapes" the paddle it will be stuck forever!
      // (until we hit it again...)
      if ( x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
      } else { 
            dy = 0;
      }
   }

if(rightPressed && paddleX < canvas.width-paddleWidth) {
   paddleX += 7;
}
else if(leftPressed && paddleX > 0) {
   paddleX -= 7;
}

   x += dx;
   y += dy;

   // Lets also improve the feeling of the game with
   requestAnimationFrame(draw);
}
// since we are now calling the function draw at the end of itself (so it will recusively call itself 4-ever
// we don't need setInterval anymore:
// draw();
