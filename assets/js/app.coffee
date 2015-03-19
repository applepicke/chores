window.chores = window.chores || {};

String::capitalize = ->
  @substr(0, 1).toUpperCase() + @substr(1)

$ ->
  $(document).click (e) ->
    if not $(e.target).closest('.popped').length and not $(e.target).closest('.popover-item').length
      $('.popped').removeClass('popped')


  $('.resend-signup-email-confirmation').click (e) ->
    $(e.target).hide()
    $('.loading').show()

    $.post '/needs_confirm', resend: true, (result) ->
      $('.loading').hide()
      $('.success').show()




