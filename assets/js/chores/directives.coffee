chores = angular.module('chores')

chores.directive 'foundationInit', ->
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
    elm.click ->
      scope.$apply ->
        scope.newReminder.type = attrs.ngReminderChoice

chores.directive 'ngWeekday', ($parse) ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    item = $parse(attrs.ngWeekday)
    $('.day', elm).click (e) ->
      scope.$apply ->
        item.assign(scope, $(e.target).data('day'))

        if attrs.ngWeekdayChange
          scope.$eval attrs.ngWeekdayChange

    scope.$watch attrs.ngWeekday, ->
      $('.day', elm).removeClass('selected')
      $('.day[data-day="' + scope.$eval(attrs.ngWeekday) + '"]', elm).addClass 'selected'

chores.directive 'ngPopover', () ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    selector = attrs.ngPopover
    item = $(selector, elm)

    elm.click ->
      item.toggleClass('popped')

chores.directive 'ngCalendar', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    elm.datepicker()

chores.directive 'ngTime', ->
  restrict: 'A'
  link: (scope, elm, attrs) ->
    console.log()

    #elm.timepicker()







