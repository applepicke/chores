'use strict';

var chores = angular.module('chores');

chores.controller('MainController', ['$scope', '$route', '$routeParams', 'House',
  function ($scope, $route, $routeParams, House) {

  }])

chores.controller('Welcome', ['$scope', '$location', 'House',
  function ($scope, $location, House) {
    $scope.houseName = '';
    $scope.errorClass = 'hidden';

    $scope.saveHouse = function () {
      House.createHouse($scope.houseName, function (result) {
        if (result.success) {
          $location.path('/houses/' + result.id);
        }
        else {
          $scope.error = result.msg;
          $scope.errorClass = '';
        }
      });
    };
  }])

chores.controller('HouseList', ['$scope', 'House',
  function ($scope, House) {
    House.getHouses(function (data) {
      $scope.houses = data.houses;
    });
  }]);

chores.controller('HouseDetail', ['$scope', 'House',
  function ($scope, House) {
    $scope.name = 'AHHH';
  }])


