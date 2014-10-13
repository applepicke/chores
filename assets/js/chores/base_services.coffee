chores = angular.module 'chores'

chores.factory 'Base', ($q, $http) ->

  class Base
    @properties: ->
      p = {}
      p.id = null
      p.name = null
      p.errors = {}
      p

    @apiPath: '/api'
    @requestedFields: []

    @find: (params = {}) ->
      params.fields = if Array.isArray(params.fields) then params.fields.concat(@requestedFields) else @requestedFields

      deferred = $q.defer()

      $http.get(@apiPath, {params: params})
      .success (data, status, headers, config) =>

        if Array.isArray data.data
          response = for result in data.data then new @(result, true)
          response.delete = (object) ->
            object.delete().then ->
              response.splice response.indexOf(object), 1

        else
          response = new @(data.data, true)
        deferred.resolve response

      .error (data, status, headers, config) =>
        deferred.reject data.errors

      deferred.promise

    constructor: (propValues, convertKeys = false) ->
      if @constructor.name is "Base"
        throw "The Base class cannot be instantiated and is only meant to be extended by other classes."
      @assignProperties propValues, convertKeys

    save: (data = @getDataForApi(), params = {}) ->
      deferred = $q.defer()

      if @validate()
        params.fields = if Array.isArray(params.fields) then params.fields.concat(@requestedFields) else @requestedFields
        if @id?
          promise = $http.put "#{@constructor.apiPath}/#{@id}", data, {params: params}
        else
          promise = $http.post @constructor.apiPath, data, {params: params}
        promise
          .success (data, status, headers, config) =>
            deferred.resolve @successCallback(data, status, headers, config)
          .error (data, status, headers, config) =>
            deferred.reject @failureCallback(data, status, headers, config)
      else
        deferred.reject()

      deferred.promise

    validate: -> true

    delete: (params = {}) ->
      deferred = $q.defer()

      $http.delete("#{@constructor.apiPath}/#{@id}", {params: params})
        .success (data, status, headers, config) =>
          deferred.resolve @successCallback(data, status, headers, config)
        .error (data, status, headers, config) =>
          deferred.reject @failureCallback(data, status, headers, config)

      deferred.promise

    assignProperties: (data = {}, convertKeys = false) ->
      for name, property of @constructor.properties()
        dataKey = if convertKeys then Base.toUnderScore name else name

        @[name] =
          if data[dataKey] isnt undefined
            if property? and typeof property is "function"
              if Array.isArray data[dataKey]
                for nestedValues in data[dataKey]
                  new property(nestedValues, convertKeys)
              else
                new property(data[dataKey], convertKeys)
            else
              data[dataKey]
          else
            property

      return data

    getDataForApi: (object = @) ->
      data = {}

      for name, property of @constructor.properties()
        if object[name]?
          data[Base.toUnderScore(name)] =
            if typeof property is "function"
              if Array.isArray object[name]
                for nestedObject in object[name] then prepareData nestedObject
              else
                @getDataForApi object[name]
            else
              object[name]

      return data

    successCallback: (data, status, headers, config) =>
      @assignProperties data.data, true

    failureCallback: (data, status, headers, config) =>
      @assignErrors { msg: data.msg }

    assignErrors: (errorData) ->
      @errors = errorData

    @toCamelCase: (string) ->
      string.replace /_([a-z])/g, (g) -> g[1].toUpperCase()

    @toUnderScore: (string) ->
      string.replace /([a-z][A-Z])/g, (g) -> g[0] + '_' + g[1].toLowerCase()