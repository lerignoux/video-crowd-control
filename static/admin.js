(function () {

  'use strict';

  angular.module('VideoCrowdControlAdminApp', ['ngMaterial', 'md.data.table'])
  .config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .dark();
  })
  .controller('AdminController', ['$scope', '$log', '$http', '$filter', '$location',
    function($scope, $log, $http, $filter, $location) {
      $log.log("Controller initialiation");
      $scope.data = [];

      $http.get('/video/stats', {params: {version: 1}}).
      success(function(results) {
        $log.log("Stats fetched");
        $scope.data = results.data;
      }).
      error(function(error) {
        $log.log(error);
      });

      $scope.getVideoLink = function(name) {
        return "http://" + $location.host() + ":" + $location.port() + "/#?name=" + encodeURI(name);
      };



    }
  ]);

}());
