chores = angular.module 'chores'

chores.controller 'MainController', ($scope, $route, $routeParams) ->

chores.controller 'NavController', ($scope, Account) ->
  Account.find().then (response) ->
    $scope.account = response
    $(document).foundation()

chores.controller 'Welcome', ($scope, $location, $routeParams, House) ->
  $scope.house = new House()

  House.find({id: $routeParams.houseId}).then (response) ->
    if response and response.length
      $scope.house = response[0]

  $scope.createHouse = (house) ->
    house.create().then (response) ->
      if $scope.house.id
        $location.path('/house/' + $scope.house.id + '/members/')

chores.controller 'AddMembers', ($scope, $location, $routeParams, $rootScope, House, Account) ->

  _.extend $scope,
    newMember: new Account()

  House.find({id: $routeParams.houseId}).then (response) ->
    if response
      $scope.house = response[0]
    else
      $location.path('/')

  $scope.back = ->
    $location.path('/welcome/')

  $scope.next = ->
    $location.path('/house/' + $routeParams.houseId)

  $scope.addMember = (member) ->
    $scope.house.addMember(member).then (response) ->
      $scope.newMember = new Account()
      $scope.closeModal()

chores.controller 'Invitations', ($scope, Account) ->

  Account.find().then (response) ->
    $scope.account = response

  $scope.acceptInvite = (invite) ->
    $scope.account.acceptInvite(invite)

chores.controller 'HouseList', ($scope, House) ->
  House.getHouses (data) ->
    $scope.houses = data.houses

chores.controller 'Account', ($scope, Account, Timezones) ->

  $scope.newPassword = ''
  $scope.confirmPassword = ''

  Timezones.get().then (response) ->
    $scope.timezones = response

  Account.find().then (response) ->
    $scope.account = response

  $scope.changePassword =  ->
    $scope.account.changePassword($scope.newPassword, $scope.confirmPassword).then ->
      $scope.newPassword = ''
      $scope.confirmPassword = ''
      $scope.closeModal()

  $scope.saveAccount = ->
    $scope.account.savePreferences().then ->
      humane.log 'Saved!'

chores.controller 'HouseDetail', ($scope, $routeParams, $rootScope, House, Chore, Account, Reminder, Timezones) ->

  _.extend $scope,
    house: {}
    newChore: new Chore()
    editingChore: null
    newMember: new Account()
    newReminder: new Reminder()

  House.find({id: $routeParams.houseId}).then (response) ->
    if response
      $scope.house = response[0]
    else
      $location.path('/')

  Timezones.get().then (response) ->
    $scope.timezones = response

  $scope.addMember = (member) ->
    $scope.house.addMember(member).then (response) ->
      $scope.newMember = new Account()
      $scope.closeModal()

  $scope.saveChore = (chore) ->
    $scope.house.saveChore(chore).then (response) ->
      $scope.newChore = new Chore()
      $scope.closeModal()

  $scope.removeChore = (chore) ->
    $scope.house.removeChore(chore).then (response) ->
      $scope.closeModal()

  $scope.removeMember = (user) ->
    $scope.house.removeMember(user).then (response) ->
      $scope.closeModal()

  $scope.editChore = (chore) ->
    $scope.editingChore = new Chore(chore)

  $scope.changeDay = (day) ->
    $scope.house.changeDay(day)

  $scope.editReminder = (chore) ->
    if chore.reminder
      $scope.newReminder = new Reminder(chore.reminder)
    else
      $scope.newReminder = new Reminder()

    $scope.newReminder.chore = chore
    $scope.editChore(chore)

  $scope.saveReminder = (reminder) ->
    $scope.newReminder = new Reminder(reminder)
    $scope.newReminder.chore = $scope.editingChore
    $scope.newReminder.save().then (result) ->
      chore = $scope.house.getChore(result.chore_id)
      chore.reminder = new Reminder(result)
      $scope.newReminder = new Reminder()
      $scope.closeModal()

  $scope.replaceNewChore = (id) ->
    id = parseInt id
    chore = _.find $scope.house.chores, (c) ->
      return c.id == id

    _.extend $scope.newChore.model,
      name: chore.name,
      description: chore.description,
      userId: if chore.user then chore.user.id else $scope.house.owner.id,
      id: chore.id

    $scope.newChore.title = "Edit Chore"
    $scope.newChore.showDelete = true

  $scope.deleteChore = (id, done) ->
    House.deleteChore id, (result) ->
      chores = $scope.house.chores
      $scope.house.chores = _.without(chores, _.findWhere(chores, { id: result.id }))
      done(result)


