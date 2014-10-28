chores = angular.module 'chores'

chores.factory 'House', (Base, Account, Chore) ->
  class House extends Base

    @properties: ->
      p = Base.properties()
      p.members = []
      p.chores = []
      p

    @apiPath: "#{Base.apiPath}/house/"

    validateName: ->
      if not @name
        @errors = {msg: 'You forgot to give your household a cool name!'}
        return false
      true

    create: ->
      if @validateName()
        @save
          name: @name

    addMember: (member) ->
      member.sendInvite(@id).then (_member) =>
        @members.push(_member)

    removeChore: (chore) ->
      chore_id = chore.id
      chore.delete().then =>
        @chores = _.filter(@chores, (item) -> item.id != chore_id)

    saveChore: (chore) ->
      existing = !!chore.id
      chore.save(@id).then (_chore) =>
        if not existing
          if not @chores.length
            @chores = [_chore]
          else
            @chores.push(_chore)
        else
          _.extend(_.find(@chores, (item) -> item.id == _chore.id), _chore)

    successCallback: (data, status, headers, config) =>
      super
      @.members = _.map @.members, (member) ->
        return new Account(member)

  House

chores.factory 'Chore', (Base) ->
  class Chore extends Base

    @properties: ->
      p = Base.properties()
      p.assigned = null
      p.description = null
      p

    @apiPath: "#{Base.apiPath}/chore"

    validate: ->
      if not @name
        @errors = {name: 'Forgot something!'}
        return false
      return true

    save: (house_id) ->
      if @validate()
        super
          name: @name
          assigned: [if @assigned then @assigned.id else null]
          house_id: house_id
          description: @description

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
      p

    @apiPath: "#{Base.apiPath}/account"

    validate: ->
      if not @validateForConfirmation()
        return false
      super

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

    create: ->
      if @validate()
        @save
          email: @email

  Account
