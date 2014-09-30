chores = angular.module('chores')

makeDirective = (name, event, done) ->
  chores.directive name, ->
    return ($scope, element, attrs) ->
      if event == 'attr'
        event = attrs[name]

      element.bind event, (event) ->
        done($scope, element, attrs, event)


makeDirective 'ngEnter', 'keydown keypress', ($scope, element, attrs, event) ->
  if event.which == 13
    $scope.$apply ->
      $scope.$eval(attrs.ngEnter)

    event.preventDefault()

chores.directive 'ngSaveChore', ->
  return ($scope, element, attrs) ->
    element.bind attrs['ngSaveChore'], (event) ->
      if event.which != 13 and event.which != 1
        return

      $scope.saveChore (newChore) ->
        if newChore.success
          element.foundation('reveal', 'close')


chores.directive 'ngAddMember', ->
  return ($scope, element, attrs) ->
    element.bind attrs['ngAddMember'], (event) ->
      if event.which != 13 and event.which != 1
        return

      $scope.addMember (result) ->
        if result.success
          element.foundation('reveal', 'close')


chores.directive 'ngDeleteChore', ->
  return ($scope, element, attrs) ->

    element.bind 'click', (event) ->
      $scope.$apply ->
        $scope.deleteChore attrs.ngDeleteChore, ->
          element.foundation('reveal', 'close')

makeDirective 'ngEditChore', 'click', ($scope, element, attrs, event) ->
  $scope.$apply ->
    $scope.replaceNewChore(attrs.ngEditChore)

makeDirective 'ngClear', 'click', ($scope, element, attrs, event) ->
  $scope.$apply ->

    if attrs['ngClear'] == 'chore'
      $scope.resetNewChore()

    else if attrs['ngClear'] == 'member'
      $scope.newMember.model = {}

    else if attrs['ngClear'] == 'password'
      $scope.newPassword = {}

