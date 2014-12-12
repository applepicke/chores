chores = angular.module('chores')

chores.directive 'modalInit', ->
  restrict: 'E'
  link: (scope, elm, attrs) ->
    $(document).foundation()

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
        scope.$eval attrs.ngConfirm

      $('.cancel', modal).click =>
        modal.foundation 'reveal', 'close'

      modal.foundation 'reveal', 'open'

chores.directive 'ngSmsConfirm', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.click =>
      account = scope.account
      if not account.smsVerified
        account.smsEnabled = false
        $('#allow-sms').attr "checked", false
        $('#confirm-sms-modal').foundation('reveal', 'open');

chores.directive 'ngSmsChange', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.click =>
      $('#confirm-sms-modal').foundation('reveal', 'open');

chores.directive 'ngSendVerification', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    $('.send-verification').click =>
      scope.account.sendSmsVerification().then ->
        $('#confirm-sms-code-modal').foundation('reveal', 'open');

    $('.verify-sms').click =>
      scope.account.verifySms().then ->
        $('#confirm-sms-code-modal').foundation('reveal', 'close');
        scope.account.smsVerified = true
        scope.account.smsEnabled = true



# chores.directive 'ngMobile', ->
#   restrict: 'A'
#   link: (scope, elm, attrs) ->
#     items = attrs.ngMobile.split('.')
#     obj = null
#     if items.length == 1
#       scope[items[0]].
#     else
#       _.each items, (item, index) ->
#         if index == (items.length - 1)
#           obj =





