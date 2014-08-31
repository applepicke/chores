'use strict';

var chores = angular.module('chores');

chores.factory('House', ['$resource',
  function($resource){

    function getHouse(id) {
      $resource('api/houses/:houseId', {}, {
        query: { method:'GET', params: { houseId: id } }
      });
    }

    function getHouses() {
      $resource('api/models/houses', {}, {
        query: { method: 'GET', params: {}}
      });
    }

    return {
      getHouse: getHouse,
      getHouses: getHouses
    }
  }]);