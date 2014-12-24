window.chores = window.chores || {};

$ ->
  $.fn.weekday = (config) ->
    input = @
    input.hide();

    config = config || {}

    weekline = $(Mustache.render($('#weekday-partial').html()))

    $('.day', weekline).click (e) ->
      e.preventDefault()
      item = $(e.target).closest('.day')

      input.val item.data('day')
      $('.day', weekline).removeClass('selected')
      item.addClass('selected')

      input.change()

    input.after(weekline)

  $.fn.popover = (config) ->
    elm = @
    config = config || {}

    popover = $('<div class="popover weekday"></div>')
    popover.append(config.content || $('<div></div>'))

    elm.addClass 'popover-item'
    elm.append popover

    popover.hide()

    elm.click (e) ->
      e.preventDefault()
      elm.addClass('popped')
      popover.show()

    $(document).click (e) ->
      if not $(e.target).closest(elm).length or $(e.target).closest('.day').length
        elm.removeClass('popped')
        popover.hide()




