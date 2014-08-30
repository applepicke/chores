'use strict';

var chores = angular.module('chores', ['ngResource']);

chores.factory('House', ['$resource',
  function($resource){

    function getHouse(id) {
      $resource('houses/:houseId', {}, {
        query: { method:'GET', params: { houseId: id } }
      });
    }

    function getHouses() {
      $resource('houses', {}, {
        query: { method: 'GET', params: {}}
      });
    }

    return {
      getHouse: getHouse,
      getHouses: getHouses
    }
  }]);