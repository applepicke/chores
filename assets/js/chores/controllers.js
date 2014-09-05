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
      House.createHouse($scope.houseName, function (response) {
        if (response.success) {
          $location.path('/houses/' + response.id);
        }
        else {
          $scope.error = response.msg;
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

chores.controller('HouseDetail', ['$scope', '$routeParams', '$rootScope', 'House',
  function ($scope, $routeParams, $rootScope, House) {
    $(document).foundation();
    $scope.house = {};
    $scope.newChore = {
      nameError: false,
      model: {}
    };

    House.getHouse($routeParams.houseId, function (response) {
      if (response.success) {
        $scope.house = response.house;
        $scope.resetNewChore();

        if (!$scope.house.description) {
          $scope.house.description = 'Your household doesn\'t have a description yet!'
        }
        $rootScope.title = $scope.house.name;
      }
      else {
        //Redirect somewhere else
      }
    });

    $scope.saveChore = function (done) {
      if (!$scope.newChore.model.name) {
        $scope.newChore.nameError = true;
        $scope.newChore.nameErrorMsg = 'Cannot be empty';
        return done({ success: false });
      }

      House.createChore($scope.house, $scope.newChore.model, function (result) {

        if (!result.success) {
          $scope.newChore.generalError = true;
          $scope.newChore.generalErrorMsg = result.msg;
          return done(result);
        }

        House.getChores($scope.house, function (result) {
          $scope.house.chores = result.chores;
        });

        done(result);
      });
    }

    $scope.resetNewChore = function () {
      $scope.newChore.model = {};
      $scope.newChore.model.userId = $scope.house.owner.id;
      $scope.newChore.title = 'Add Chore';
      $scope.newChore.showDelete = false;
    };

    $scope.replaceNewChore = function (id) {
      var chore = _.find($scope.house.chores, function (c) {
        return c.id == id;
      });

      _.extend($scope.newChore.model, {
        name: chore.name,
        description: chore.description,
        userId: chore.user ? chore.user.id : $scope.house.owner.id,
        id: chore.id
      });

      $scope.newChore.title = "Edit Chore";
      $scope.newChore.showDelete = true;
    };

  }])


