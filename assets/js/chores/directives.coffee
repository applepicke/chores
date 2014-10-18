chores = angular.module('chores')

chores.directive 'ngModalClose', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    scope.closeModal = ->
      $('body').foundation('reveal', 'close')

chores.directive 'ngConfirm', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.click =>
      message = attrs.ngConfirmMessage
      modal = $('#confirm-modal')
      $('.message', modal).text(message)

      $('.okay', modal).unbind().click =>
        $scope.$eval attrs.ngConfirm

      $('.cancel', modal).click =>
        modal.foundation 'reveal', 'close'

      modal.foundation 'reveal', 'open'


