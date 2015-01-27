chores = angular.module 'chores'

chores.factory 'House', (Base, Account, Chore) ->
  class House extends Base

    @properties: ->
      p = Base.properties()
      p.members = []
      p.chores = []
      p.recurs = null
      p

    @apiPath: "#{Base.apiPath}/house"

    constructor: (propValues, convertKeys = false) ->
      super
      @chores = _.map @chores, (chore) ->
        new Chore(chore)

    validateName: ->
      if not @name
        @errors = {msg: 'You forgot to give your household a cool name!'}
        return false

      true

    myHouse: ->
      @find({}, '/api/house/my_house/')

    create: ->
      if @validateName()
        @save
          name: @name

    addMember: (member) ->
      member.sendInvite(@id).then (_member) =>
        @members.push(_member)

    changeDay: (day) ->
      @recurs = day
      @save
        recurs: @recurs

    getChore: (choreId) ->
      _.find @chores, (item) ->
        choreId == item.id

    removeChore: (chore) ->
      chore_id = chore.id
      chore.delete().then =>
        @chores = _.filter(@chores, (item) -> item.id != chore_id)

    saveChore: (chore) ->
      existing = !!chore.id
      chore.houseId = @id
      chore.save().then (_chore) =>
        if not existing
          if not @chores.length
            @chores = [_chore]
          else
            @chores.push(_chore)
        else
          _.extend(_.find(@chores, (item) -> item.id == _chore.id), _chore)

    successCallback: (data, status, headers, config) =>
      if data
        super
      if data.members
        @members = _.map @members, (member) ->
          new Account(member)
      if data.chores
        @chores = _.map @chores, (chore) ->
          new Chore(chore)

  House

chores.factory 'Chore', (Base, Reminder) ->
  class Chore extends Base

    @properties: ->
      p = Base.properties()
      p.assigned = null
      p.description = null
      p.houseId = null
      p.reminder = null
      p

    @apiPath: "#{Base.apiPath}/chore"

    constructor: (propValues, convertKeys = false) ->
      super
      if @reminder
        @reminder = new Reminder(@reminder)

    validate: ->
      if not @name
        @errors = {name: 'Forgot something!'}
        return false
      return true

    save: (data) ->
      if @validate()
        if not data
          data =
            name: @name
            assigned: [if @assigned then @assigned.id else null]
            description: @description

        data.house_id = @houseId
        super data

    successCallback: (data, status, headers, config) =>
      super
      if data.data.reminder
        @reminder = new Reminder(data.data.reminder)
      @

chores.factory 'Reminder', (Base) ->
  class Reminder extends Base

    @properties: ->
      p = Base.properties()
      p.type = 'weekly'
      p.date = null
      p.time = null
      p.day = null
      p.chore = null
      p

    @apiPath: "#{Base.apiPath}/reminder"

    pretty: ->
      if @type == 'once'
        date = moment("#{@date} #{@time}" , 'MM/DD/YYYY hh:mm a')
        return date.format('MMM DD, YYYY hh:mm a')

      if @type == 'weekly'
        return "#{@day.capitalize()}s @ #{@time}"

      if @type == 'daily'
        return "Daily @ #{@time}"

      return ''

    validate: ->
      valid = true
      @errors = {}

      if @type == 'once' and not moment(@date, 'MM/DD/YYYY', true).isValid()
        @errors.date = 'Invalid date or time format'
        valid = false

      if not moment(@time, 'hh:mm a', true).isValid()
        @errors.time = 'Invalid time'
        valid = false

      valid

    save: ->
      if @validate()
        super
          type: @type
          date: @date
          time: @time
          day: @day
          chore_id: @chore.id

chores.factory 'Account', (Base) ->
  class Account extends Base

    @properties: ->
      p = Base.properties()
      p.confirmed = false
      p.emailEnabled = false
      p.firstName = ''
      p.lastName = ''
      p.hasPassword = false
      p.name = ''
      p.smsEnabled = false
      p.smsVerified = false
      p.email = null
      p.phoneNumber = ''
      p.verificationCode = null
      p

    @apiPath: "#{Base.apiPath}/account"

    validate: ->
      if not @validateForConfirmation()
        return false
      super

    validateSms: ->
      # TODO: Some real sms validation
      return true

    validateSmsCode: ->
      if not @verificationCode.length or @verificationCode.length != 5
        @errors = { sms_verify: 'Invalid verification code' }
        return false

      return true

    validateForConfirmation: ->
      if not @email
        @errors = {msg: 'You forget to type in an email. Dummy.'}
        return false
      true

    sendInvite: (houseId) ->
      if @validateForConfirmation()
        @save
          email: @email
          house_id: houseId

    changePassword: (newPassword, confirmPassword) ->
      if newPassword != confirmPassword
        @errors =
          password: 'Passwords don\'t match!'
        return
      @save
        password: newPassword

    savePreferences: ->
      if @validate()
        @save()

    sendSmsVerification: ->
      if @validateSms
        @save
          send_sms_verification_code: true
          sms: @phoneNumber

    verifySms: ->
      if @validateSmsCode
        @save
          verify_sms: true,
          sms_code: @verificationCode

    create: ->
      if @validate()
        @save
          email: @email

  Account
