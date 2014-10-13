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

    saveChore: (chore) ->
      chore.save(@id).then (_chore) =>
        @chores.push(_chore)

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
      p

    @apiPath: "#{Base.apiPath}/chore/"

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


chores.factory 'Account', (Base) ->
  class Account extends Base

    @properties: ->
      p = Base.properties()
      p.email = null

    @apiPath: "#{Base.apiPath}/account/"

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

    create: ->
      if @validate()
        @save
          email: @email

  Account
