chores = angular.module 'chores', ['ngRoute', 'ngResource']

chores.config ['$routeProvider', '$locationProvider',
  ($routeProvider, $locationProvider) ->
    $routeProvider
      .when '/welcome',
        templateUrl: '/static/partials/welcome.html',
        controller: 'Welcome'

      .when '/account',
        templateUrl: '/static/partials/account_detail.html',
        controller: 'Account'

      .when '/house',
        templateUrl: '/static/partials/house_list.html',
        controller: 'HouseList'

      .when '/house/:houseId/members/',
        templateUrl: '/static/partials/members.html',
        controller: 'AddMembers'

      .when '/house/:houseId',
        templateUrl: '/static/partials/house_detail.html',
        controller: 'HouseDetail'

      .when '/invites',
        templateUrl: '/static/partials/invites.html',
        controller: 'Invitations'

      .otherwise
        redirectTo: '/'

      $locationProvider.html5Mode true
]