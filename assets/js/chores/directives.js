
var chores = angular.module('chores');

function makeDirective(name, event, done) {
  chores.directive(name, function () {
    return function ($scope, element, attrs) {
      if (event === 'attr') {
        event = attrs[name];
      }
      element.bind(event, function (event) {
        done($scope, element, attrs, event);
      });
    };
  });
}


makeDirective('ngEnter', 'keydown keypress', function ($scope, element, attrs, event) {
  if(event.which === 13) {
    $scope.$apply(function (){
      $scope.$eval(attrs.ngEnter);
    });
    event.preventDefault();
  }
});


chores.directive('ngSaveChore', function () {
  return function ($scope, element, attrs) {
    element.bind(attrs['ngSaveChore'], function (event) {
      if (event.which !== 13 && event.which !== 1) {
        return;
      }

      $scope.saveChore(function (newChore) {
        if (newChore.success) {
          element.foundation('reveal', 'close');
        }
      });
    });
  };
});

chores.directive('ngAddMember', function () {
  return function ($scope, element, attrs) {
    element.bind(attrs['ngAddMember'], function (event) {
      if (event.which !== 13 && event.which !== 1) {
        return;
      }

      $scope.addMember(function (result) {
        if (result.success) {
          element.foundation('reveal', 'close');
        }
      });
    });
  };
});

chores.directive('ngDeleteChore', function () {
  return function ($scope, element, attrs) {
    element.bind('click', function (event) {
      $scope.$apply(function () {
        $scope.deleteChore(attrs.ngDeleteChore, function () {
          element.foundation('reveal', 'close');
        });
      });
    });
  };
});

makeDirective('ngEditChore', 'click', function ($scope, element, attrs, event) {
  $scope.$apply(function () {
    $scope.replaceNewChore(attrs.ngEditChore);
  });
});

makeDirective('ngClear', 'click', function ($scope, element, attrs, event) {
  $scope.$apply(function () {
    if (attrs['ngClear'] === 'chore') {
      $scope.resetNewChore();
    }
    else if (attrs['ngClear'] === 'member') {
      $scope.newMember.model = {};
    }
  });
});

