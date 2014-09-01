'use strict';

var chores = angular.module('chores');

chores.controller('MainController', ['$scope', '$route', '$routeParams', 'House',
  function ($scope, $route, $routeParams, House) {

  }])

chores.controller('Welcome', ['$scope', 'House',
  function ($scope, House) {
    House.getHouses(function (data) {
      $scope.houses = data.houses;
    });
  }])

chores.controller('HouseList', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'WILLYYY';
  }]);

chores.controller('HouseDetail', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'AHHH';
  }])


