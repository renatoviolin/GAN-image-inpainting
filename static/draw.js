// get reference to canvas and save canvas offsets
var canvas = document.getElementById('drawing');
var offsetX = canvas.offsetLeft;
var offsetY = canvas.offsetTop + 60;

$(window).resize(function () {
    offsetX = canvas.offsetLeft;
    offsetY = canvas.offsetTop + 60;
});

function clear_canvas() {
    context = canvas.getContext('2d')
    context.clearRect(0, 0, canvas.width, canvas.height);
}

var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

/**
 * @param {CanvasRenderingContext2D} context
 */
function PrimitiveBrush(context) {
    if (!(context instanceof CanvasRenderingContext2D)) {
        throw new Error('No 2D rendering context given!');
    }

    this.ctx = context;
    this.strokes = [];
    this.strokeIndex = 0;
    this.workingStrokes;
    this.lastLength = 0;
    this.isTouching = false;

    // init context
    this.ctx.strokeStyle = '#FFF';
    this.ctx.lineWidth = '25';
    this.ctx.lineCap = this.ctx.lineJoin = 'round';
}

/**
 * Begins a new stroke
 * @param  {MouseEvent} event
 */
PrimitiveBrush.prototype.start = function (event) {
    var x = event.clientX - offsetX;
    var y = event.clientY - offsetY;
    this.workingStrokes = [{
        x: x,
        y: y
    }];
    this.strokes.push(this.workingStrokes);
    this.lastLength = 1;
    this.isTouching = true;
    requestAnimationFrame(this._draw.bind(this));
};

/**
 * Moves the current position of our brush
 * @param  {MouseEvent} event
 */
PrimitiveBrush.prototype.move = function (event) {
    if (!this.isTouching) {
        return;
    }
    var x = event.clientX - offsetX;
    var y = event.clientY - offsetY;
    this.workingStrokes.push({
        x: x,
        y: y
    });
    requestAnimationFrame(this._draw.bind(this));
};

/**
 * Stops a stroke
 * @param  {MouseEvent} event
 */
PrimitiveBrush.prototype.end = function (event, foo) {
    this.move(event);
    this.isTouching = false;
};

PrimitiveBrush.prototype._draw = function () {

    // save the current length quickly (it's dynamic)
    var length = this.workingStrokes.length;

    // return if there's no work to do
    if (length <= this.lastLength) {
        return;
    }

    var startIndex = this.lastLength - 1;

    this.lastLength = length;

    var pt0 = this.workingStrokes[startIndex];

    this.ctx.beginPath();

    this.ctx.moveTo(pt0.x, pt0.y);

    for (var j = startIndex; j < this.lastLength; j++) {

        var pt = this.workingStrokes[j];

        this.ctx.lineTo(pt.x, pt.y);

    }

    this.ctx.stroke();

};

// Set up brush to listen to events
var brush = new PrimitiveBrush(canvas.getContext('2d'));

canvas.addEventListener('mousedown', brush.start.bind(brush));
canvas.addEventListener('mousemove', brush.move.bind(brush));
canvas.addEventListener('mouseup', brush.end.bind(brush));
canvas.addEventListener('mouseout', brush.end.bind(brush));