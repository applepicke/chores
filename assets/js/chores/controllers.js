'use strict';

var chores = angular.module('chores');

chores.controller('MainController', ['$scope', '$route', '$routeParams', 'House',
  function ($scope, $route, $routeParams, House) {

  }])

chores.controller('HouseList', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'WILLYYY';
  }]);

chores.controller('HouseDetail', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'AHHH';
  }])

chores.controller('HouseDetail', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'AHHH';
  }])
