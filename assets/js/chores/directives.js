
var chores = angular.module('chores');

chores.directive('ngEnter', function () {
  return function ($scope, element, attrs) {
    element.bind("keydown keypress", function (event) {
      if(event.which === 13) {
        $scope.$apply(function (){
          $scope.$eval(attrs.ngEnter);
        });
        event.preventDefault();
      }
    });
  };
});

chores.directive('ngSaveChore', function () {
  return function ($scope, element, attrs) {
    element.bind('click', function (event) {
      $scope.saveChore(function (newChore) {
        if (newChore.success) {
          element.foundation('reveal', 'close');
        }
      });

    });
  };
});