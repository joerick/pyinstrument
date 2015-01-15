/* jshint globalstrict: true */
/* global $ */

'use strict';

var data = JSON.parse(document.getElementById('data').text);

var width = 960,
    frameHeight = 25;

var x = d3.scale.linear().clamp(true)
    .range([0, width]);

function nodeWidth(d) {
    return Math.max(x(d.x + d.dx) - x(d.x) - 2, 0)
}

var y = d3.scale.linear().clamp(true);

var chart = d3.select('.flamechart')
    .attr("width", width);

chart.append('svg:rect')
     .attr('width', '100%')
     .attr('height', '100%')
     .attr('fill', 'darkslategrey')
     .attr('rx', 5)
     .attr('ry', 5);

function valueFn(d) {
    return d.time;
}

function childrenFn(d) {
    if (d.children.length == 0) {
        return null;
    } else {
        // Add a new 'child' that will be hidden
        // but will contribute the 'self' time for this
        // node
        var selfTime = d.time;
        var childCount = d.children.length;
        for (var i = 0; i < childCount; i++) {
            selfTime -= d.children[i].time;
        }
        d.children.push({
            time: selfTime,
            placeholder: true,
            children: []
        })
        return d.children;
    }
}

function compareFn(a, b) {
    // Always sort a placeholder to the end
    if (a.placeholder && !b.placeholder) {
        return 1;
    } else if (b.placeholder && !a.placeholder) {
        return -1;
    } else {
        return b.value - a.value;
    }
}

var partition = d3.layout.partition()
    .value(valueFn)
    .children(childrenFn)
    .sort(compareFn);

var partitioned = partition(data);

var color = d3.scale.linear()
    .domain([0, 1])
    .range(["yellow", "red"]);

var minWidth = 2;

function keyFn(d) {
    if (d.key) {
        return d.key;
    }
    var key;
    if (d.parent == null) {
        key = d.code_position;
    } else {
        key = keyFn(d.parent) + '/' + d.code_position;
    }
    d.key = key;
    return key;
}

if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.substring(0, str.length) === str;
  };
}

function tooltipFn(d) {
    return d.function + " (" + d.code_position + ", " + d.time + "s, " + d.total_proportion * 100 + "% of total) " + d.value + ", " + d.parent_proportion + ', ' + d.dx;
}

function updateChart(focus) {
    if (focus) {
        x.domain([focus.x, focus.x + focus.dx]);
    }

    var selectedData = partitioned.filter(function(d) {return (!d.placeholder) && nodeWidth(d) > minWidth;})
    var updateSel = chart.selectAll('g')
        .data(selectedData, keyFn);

    var maxDepth = d3.max(selectedData, function(d) { return d.depth; });
    var height = (maxDepth + 1) * frameHeight;
    chart.attr('height', height);
    y.domain([0, maxDepth]).range([height, 0]);

    var enterGroup = updateSel.enter().append('g')
             .on("click", updateChart);

    enterGroup.append('title')
              .text(tooltipFn)

    enterGroup.append('rect')
              .attr('fill', function (d) {return color(d.parent_proportion);})
              .attr('rx', 2)
              .attr('ry', 2);

    enterGroup.append('text')
              .attr('text-anchor', 'middle')
              .attr('dominant-baseline', 'central')
              .text(function(d) {return d.function;})
              .attr('visibility', 'hidden');

    updateSel.select('rect')
             .attr('y', function (d) {return y(d.depth) + 1;})
             .attr('height', function (d) {return frameHeight - 2;})
             .attr('x', function(d) { return x(d.x) + 1})
             .attr('width', nodeWidth);

    updateSel.select('text')
             .attr('x', function(d) { return (x(d.x) + x(d.x + d.dx)) / 2; })
             .attr('y', function(d) {return y(d.depth - .5);})

    updateSel.each(function(d) {
        d3.select(this).select('text').attr('visibility', function(t) {
            return nodeWidth(d) > this.getComputedTextLength() ? 'visible' : 'hidden';
        })
    })

    updateSel.exit().remove();

    updateSel.on("click", updateChart);
}

updateChart(null);