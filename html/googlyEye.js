"use strict";

function googlyEye(paper, xpos, ypos) {
    var iris = paper.circle(xpos, ypos, 100);
    iris.attr({
        fill: "#eee",
        stroke: "#000",
        strokeWidth: 5
    });
    paper.circle(xpos, ypos + 50, 50);
}