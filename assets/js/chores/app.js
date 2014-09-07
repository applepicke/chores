'use strict';

var chores = angular.module('chores', ['ngRoute', 'ngResource']);

chores.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/welcome', {
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

      $locationProvider.html5Mode(true);
  }]);