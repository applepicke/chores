'use strict';

var chores = angular.module('chores');

chores.factory('House', ['$resource',
  function($resource){

    function getHouse(id, done) {
      var house = $resource('/api/houses/:houseId/', {}, {
        query: { method:'GET', params: { houseId: id } }
      });
      house.query(done);
    }

    function getHouses(done) {
      var houses = $resource('/api/houses/', {}, {
        query: { method: 'GET', params: {}}
      });
      houses.query(done);
    }

    function getChores(house, done) {
      var chores = $resource('/api/houses/:houseId/chores/', {}, {
        query: { method: 'GET', params: { houseId: house.id } }
      });
      chores.query(done);
    }

    function deleteChore(id, done) {
      var Chore = $resource('/api/chores/:choreId/', {}, {
        delete: { method: 'DELETE', params: { choreId: id } }
      });
      Chore.delete({}, {}, done);
    }

    function createHouse(name, done) {
      var house = $resource('/api/houses/', {}, {
        query: { method: 'POST', params: {
          'name': name,
        }}
      })
      house.query(done);
    }

    function createChore(house, chore, done) {
      var Chore = $resource('/api/houses/:houseId/chores/', {}, {
        save: { method: 'POST', params: { houseId: house.id } }
      });

      Chore.save({
        name: chore.name,
        description: chore.description,
        userId: chore.userId,
        id: chore.id
      }, {}, done);
    }

    function addMember(house, email, done) {
      var Member = $resource('/api/houses/:houseId/members/', {}, {
        add: { method: 'POST', params: { houseId: house.id } }
      });

      Member.add({
        email: email
      }, {}, done);
    }

    return {
      getHouse: getHouse,
      getHouses: getHouses,
      createHouse: createHouse,
      createChore: createChore,
      getChores: getChores,
      deleteChore: deleteChore,
      addMember: addMember,
    }
  }]);

chores.factory('Account', ['$resource',
  function ($resource) {

    function getAccount(done) {
      var Account = $resource('/api/account', {}, {
        get: { method: 'GET', params: {} }
      });

      Account.get({}, done);
    }

    return {
      getAccount: getAccount
    }
  }]);