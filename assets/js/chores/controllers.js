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
      nameError: false
    };

    House.getHouse($routeParams.houseId, function (response) {
      if (response.success) {
        $scope.house = response.house;
        $scope.newChore.userId = response.house.owner.id;

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
      if (!$scope.newChore.name) {
        $scope.newChore.nameError = true;
        $scope.newChore.nameErrorMsg = 'Cannot be empty';
        return done({ success: false });
      }

      House.createChore($scope.house, $scope.newChore, function (newChore) {

        if (!newChore.success) {
          $scope.newChore.generalError = true;
          $scope.newChore.generalErrorMsg = newChore.msg;
          return done(newChore);
        }

        $scope.house.chores.push(newChore);
        done(newChore);
      });
    }

  }])


