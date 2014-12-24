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

chores.directive 'ngHoverShow', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    item = $('.' + attrs.ngHoverShow, elm)
    elm.hover =>
      item.show()

chores.directive 'ngReveal', () ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.click ->
      modal = $('#' + attrs.ngReveal)
      modal.foundation 'reveal', 'open'
      false

chores.directive 'ngReminderChoice', () ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    if scope.newReminder.type == attrs.ngReminderChoice
      elm.addClass 'selected'

    elm.click ->
      scope.$apply ->
        scope.newReminder =
          type: attrs.ngReminderChoice

      elm.addClass 'selected'
      elm.siblings().removeClass 'selected'

chores.directive 'ngWeekdayPopover', ($parse) ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    content = $('<input class="day-input"></input>')

    content.change ->
      value = content.val()
      item = $parse(attrs.ngWeekdayPopover)
      item.assign(scope, value)

      scope.$eval(attrs.ngWeekdayChange)

    elm.popover
      content: content

    content.weekday {}

chores.directive 'ngWeekday', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.weekday()

chores.directive 'ngCalendar', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.datepicker()

chores.directive 'ngTime', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.timepicker()







