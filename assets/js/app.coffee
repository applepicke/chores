window.chores = window.chores || {};

$.fn.weekday = ->
  input = @
  input.hide();

  weekline = $(Mustache.render($('#weekday-partial').html()))

  $('.day', weekline).click (e) ->
    e.preventDefault()
    input.val @.data('day')
    $('.day', weekline).removeClass('selected')
    @.addClass('selected')

  input.after(weekline)