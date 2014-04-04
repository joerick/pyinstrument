/* jshint globalstrict: true */
/* global $ */

'use strict';
$('.frame').click(function (event) {
    $(this).toggleClass('collapse');
    event.stopPropagation();
});
$('.frame, body').mousemove(function (event) {
    $('.frame.last-hover').removeClass('last-hover');
    $(this).addClass('last-hover');
    event.stopPropagation();
});
