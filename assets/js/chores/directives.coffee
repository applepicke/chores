chores = angular.module('chores')

chores.directive 'ngModalClose', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    scope.closeModal = ->
      $('body').foundation('reveal', 'close')

