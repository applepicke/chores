chores = angular.module 'chores'

chores.controller 'MainController', ($scope, $route, $routeParams, House) ->

chores.controller 'Welcome', ($scope, $location, House) ->
  $scope.house = new House()

  $scope.next = ->
    $location.path('/house/' + $scope.house.id + '/members/')

chores.controller 'AddMembers', ($scope, $location, $routeParams, $rootScope, House, Account) ->
  $(document).foundation()

  _.extend $scope,
    newMember: new Account()

  House.find({id: $routeParams.houseId}).then (response) ->
    if response
      $scope.house = response[0]
    else
      $location.path('/')

  $scope.next = ->
    $location.path('/house/' + $routeParams.houseId)

  $scope.addMember = ->
    $scope.house.addMember($scope.newMember).then (response) ->
      $scope.newMember = new Account()
      closeModal()

chores.controller 'HouseList', ($scope, House) ->
  House.getHouses (data) ->
    $scope.houses = data.houses

chores.controller 'Account', ($scope, Account) ->
  $(document).foundation()
  $scope.newPassword = {}

  Account.getAccount (account) ->
    $scope.account = account

  $scope.closeModal = (result) ->
    if result.success
      $('body').foundation('reveal', 'close')

  $scope.changePassword = (done) ->
    if $scope.newPassword.password != $scope.newPassword.confirmPassword
      $scope.newPassword.generalError = true
      $scope.newPassword.generalErrorMsg = 'Passwords don\'t match'
      return done({success: false})

    Account.changePassword $scope.newPassword.password, $scope.newPassword.confirmPassword, (result) ->
      if !result.success
        $scope.newPassword.generalError = true
        $scope.newPassword.generalErrorMsg = result.msg
        return done(result)

      $scope.account.has_password = true
      done(result)

chores.controller 'HouseDetail', ($scope, $routeParams, $rootScope, House, Chore, Account) ->
  $(document).foundation()

  _.extend $scope,
    house: {},
    newChore: new Chore()
    editingChore: null
    newMember: new Account()

  House.find({id: $routeParams.houseId}).then (response) ->
    if response
      $scope.house = response[0]
    else
      $location.path('/')

  $scope.addMember = ->
    $scope.house.addMember($scope.newMember).then (response) ->
      $scope.newMember = new Account()
      closeModal()

  $scope.saveChore = (chore) ->
    $scope.house.saveChore(chore).then (response) ->
      $scope.newChore = new Chore()
      $scope.closeModal()

  $scope.removeChore = (chore) ->
    $scope.house.removeChore(chore).then (response) ->
      closeModal()

  $scope.editChore = (chore) ->
    $scope.editingChore = chore

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


