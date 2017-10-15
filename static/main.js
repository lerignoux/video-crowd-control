(function () {

  'use strict';

  angular.module('VideoCrowdControlApp', ['ngMaterial'])
  .config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .dark();
  })
  .controller('VideoController', ['$scope', '$log', '$http', '$mdToast',
    function($scope, $log, $http, $mdToast) {
      $log.log("Controller initialiation");
      $scope.video = null;
      $scope.videoFilename = null;

      $http.get('/video', {params: {"ip": "unknown"}}).
        success(function(result) {
          $log.log("Video fetched: " + result.filename);
          $scope.video = result.filename;
          $scope.version = result.version
          $scope.videoFilename = encodeURI("static/videos/" + result.filename);
        }).
        error(function(error) {
          $log.log(error);
        });

        $scope.videoFeedback = function(feedback) {
          $http.post('/video/rate', {name: $scope.video, version: $scope.version, feedback: $scope.feedback, rating:feedback}).
            success(function(results) {
              $log.log("feedback Submited: "+ feedback);
              $scope.showSuccessToast()
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.showSuccessToast = function() {
          $mdToast.show(
            $mdToast.simple()
              .textContent('Thank you for your feedback, you can refresh the page if you want to go on!')
              .position('bottom center')
              .hideDelay(10000)
              .theme("success-toast")
          );
        };

      }
  ]);

}());
