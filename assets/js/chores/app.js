'use strict';

var chores = angular.module('chores', ['ngRoute', 'ngResource']);

chores.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '/static/partials/welcome.html',
        controller: 'Welcome'
      }).
      when('/houses', {
        templateUrl: '/static/partials/house_list.html',
        controller: 'HouseList'
      }).
      when('/houses/:houseId', {
        templateUrl: '/static/partials/house_detail.html',
        controller: 'HouseDetail'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);