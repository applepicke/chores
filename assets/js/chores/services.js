'use strict';

var chores = angular.module('chores');

chores.factory('House', ['$resource',
  function($resource){

    function getHouse(id, done) {
      var house = $resource('api/houses/:houseId', {}, {
        query: { method:'GET', params: { houseId: id } }
      });
      house.query(done);
    }

    function getHouses(done) {
      var houses = $resource('api/houses', {}, {
        query: { method: 'GET', params: {}}
      });
      houses.query(done);
    }

    return {
      getHouse: getHouse,
      getHouses: getHouses
    }
  }]);