'use strict';

var chores = angular.module('chores', [
  'ngRoute'
]);

chores.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/houses', {
        templateUrl: 'partials/house_list.html',
        controller: 'HouseList'
      }).
      when('/houses/:houseId', {
        templateUrl: 'partials/house-detail.html',
        controller: 'HouseDetail'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);