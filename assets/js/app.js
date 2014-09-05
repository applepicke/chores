window.chores = window.chores || {};

function replace(arr, val, fn) {
  var item = _.find(arr, fn);
  var index = _.indexOf(arr, item);
  arr[index] = val;
}

$(function () {

});