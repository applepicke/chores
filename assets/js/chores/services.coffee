chores = angular.module 'chores'

chores.factory 'House', (Base, Account, $resource) ->

  class House extends Base

    @properties: ->
      p = Base.properties()
      p.members = []
      p

    @apiPath: "#{Base.apiPath}/houses/"

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

  return House

  getHouse = (id, done) ->
    house = $resource '/api/houses/:houseId/', {},
      query:
        method:'GET',
        params:
          houseId: id

    house.query(done)

  getHouses = (done) ->
    houses = $resource '/api/houses/', {},
      query:
        method: 'GET',
        params: {}

    houses.query(done)

  getChores = (house, done) ->
    chores = $resource '/api/houses/:houseId/chores/', {},
      query:
        method: 'GET',
        params:
          houseId: house.id

    chores.query(done)

  deleteChore = (id, done) ->
    Chore = $resource '/api/chores/:choreId/', {},
      delete:
        method: 'DELETE',
        params:
          choreId: id

    Chore.delete {}, {}, done

  createHouse = (name, done) ->
    house = $resource '/api/houses/', {},
      query:
        method: 'POST',
        params:
          'name': name

    house.query done;

  createChore = (house, chore, done) ->
    Chore = $resource '/api/houses/:houseId/chores/', {},
      save:
        method: 'POST',
        params:
          houseId: house.id

    Chore.save(
      name: chore.name,
      description: chore.description,
      userId: chore.userId,
      id: chore.id
    , {}, done)


  addMember = (house, email, done) ->
    Member = $resource '/api/houses/:houseId/members/', {},
      add:
        method: 'POST',
        params:
          houseId: house.id

    Member.add(
      email: email
    , {}, done)

  return {
    getHouse: getHouse,
    getHouses: getHouses,
    createHouse: createHouse,
    createChore: createChore,
    getChores: getChores,
    deleteChore: deleteChore,
    addMember: addMember
  }

chores.factory 'Account', (Base, $resource) ->

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

  return Account

  Account = $resource '/api/account', {},
    get: { method: 'GET', params: {} },
    post: { method: 'POST', params: {} }

  getAccount = (done) ->
    Account.get({}, done)

  changePassword = (password, confirmPassword, done) ->
    Account.post({}, JSON.stringify(
      password: password,
      confirm_password: confirmPassword
    ), done);

  return {
    getAccount: getAccount,
    changePassword: changePassword
  }