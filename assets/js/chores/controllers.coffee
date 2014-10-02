chores = angular.module 'chores'

initScope = (scope, defaults) ->
  _.extend scope, defaults

  _.extend scope,
    addMember: (done) ->
      email = $scope.newMember.model.email

      if not email
        $scope.newMember.model.generalError = true
        $scope.newMember.model.generalErrorMsg = 'Must specify an email'
        return done({ success: false })

      House.addMember $scope.house, email, (result) ->
        $scope.newMember.model.email = ''
        if result.success
          $scope.house.members.push(result.member)
          done(result)

        else
          $scope.newMember.model.generalError = true
          $scope.newMember.model.generalErrorMsg = result.msg
          done({success: false})

  scope

chores.controller 'MainController', ($scope, $route, $routeParams, House) ->

chores.controller 'Welcome', ($scope, $location, House) ->
  $scope.house = new House()

  $scope.next = ->
    $location.path('/houses/' + $scope.house.id + '/members/')

chores.controller 'AddMembers', ['$scope', '$location', '$routeParams', '$rootScope', 'House',
  ($scope, $location, $routeParams, $rootScope, House) ->
    $(document).foundation()

    _.extend($scope, new Scope())

    $scope.nextPage = ->
      $location.path('/houses/' + $routeParams.houseId)

    House.getHouse $routeParams.houseId, (response) ->
      if response.success
        $scope.house = response.house
        $rootScope.title = $scope.house.name
      else
        $location.path('/')
]

chores.controller 'HouseList', ['$scope', 'House',
  ($scope, House) ->
    House.getHouses (data) ->
      $scope.houses = data.houses
]

chores.controller 'Account', ['$scope', 'Account',
  ($scope, Account) ->
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
]

chores.controller 'HouseDetail', ($scope, $routeParams, $rootScope, House) ->
  $(document).foundation()

  $scope = initScope $scope,

    house: {},
    newChore:
      nameError: false,
      model: {}
    newMember:
      generalError: false,
      model: {}

  House.getHouse $routeParams.houseId, (response) ->
    if response.success
      $scope.house = response.house
      $scope.resetNewChore()

      if !$scope.house.description
        $scope.house.description = 'Your household doesn\'t have a description yet!'

      $rootScope.title = $scope.house.name

    else {
      #Redirect somewhere else
    }

  $scope.reloadChores = ->
      House.getChores $scope.house, (result) ->
        $scope.house.chores = result.chores


  $scope._replaceChore = (newChore) ->
    chore = _.find $scope.house.chores, (chore) ->
      return chore.id == newChore.id

    chore.name = newChore.name
    chore.description = newChore.description
    chore.user = newChore.user

  $scope.saveChore = (done) ->
    if !$scope.newChore.model.name
      $scope.newChore.nameError = true
      $scope.newChore.nameErrorMsg = 'Cannot be empty'
      return done({ success: false })

    House.createChore $scope.house, $scope.newChore.model, (result) ->

      if !result.success
        $scope.newChore.generalError = true
        $scope.newChore.generalErrorMsg = result.msg
        return done(result)

      $scope.reloadChores()

      done(result);

  $scope.resetNewChore = ->
    $scope.newChore.model = {}
    $scope.newChore.model.userId = $scope.house.owner.id
    $scope.newChore.title = 'Add Chore'
    $scope.newChore.showDelete = false
    $scope.newChore.generalError = false
    $scope.newChore.nameError = false
    true

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


