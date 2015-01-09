window.chores = window.chores || {};

String::capitalize = ->
  @substr(0, 1).toUpperCase() + @substr(1)

# $.fn.popover = (config) ->
#   elm = @
#   config = config || {}

#   popover = $('<div class="popover weekday"></div>')
#   popover.append(config.content || $('<div></div>'))

#   elm.addClass 'popover-item'
#   elm.append popover

#   popover.hide()

#   elm.click (e) ->
#     e.preventDefault()
#     elm.addClass('popped')
#     popover.show()

#   $(document).click (e) ->
#     if not $(e.target).closest(elm).length or $(e.target).closest('.day').length
#       elm.removeClass('popped')
#       popover.hide()




