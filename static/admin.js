(function () {

  'use strict';

  angular.module('VideoCrowdControlAdminApp', ['ngMaterial', 'md.data.table'])
  .config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .dark();
  })
  .controller('AdminController', ['$scope', '$log', '$http', '$filter',
    function($scope, $log, $http, $filter) {
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

    }
  ]);

}());
