var app = angular.module('liftApp', []);
app.controller('boatLiftController', function($scope, $http, $timeout) {
    $scope.status = {
        "lift_state": "",
        "blower_state": "",
        "master_valve_state": "",
        "rear_valve_state": "",
        "front_valve_state": ""
    };
    var init = function () {
        $timeout(function() {
            $http({
                url: '/status',
                method: "GET",
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
         }, 0);
    };
    init();
    $scope.upPushed = function() {
        $http({
            url: '/up',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.downPushed = function() {
        $http({
            url: '/down',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.frontValvesOpen = function() {
        $http({
            url: '/frontValvesOpen',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.frontValvesClose = function() {
        $http({
            url: '/frontValvesClose',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.rearValvesOpen = function() {
        $http({
            url: '/rearValvesOpen',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.rearValvesClose = function() {
        $http({
            url: '/rearValvesClose',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.toggleMasterValve = function(event) {
        var element = angular.element( event.currentTarget ).children( ".switch" )[0];
        if($scope.status.master_valve_state == "open") {
            var size = 30;
            var frame = 0;
            var interval = setInterval(function() {
                element.css('background-position', frame * size + 'px 0px');
                frame--;
                if (frame == -10) {
                    clearInterval(interval);
                }
            }, 273);
            $http({
                url: '/masterValveClose',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        } else if($scope.status.master_valve_state == "closed") {
            element.css('background-position', '-300px 0px');
            var size = 30;
            var frame = -10;
            var interval = setInterval(function() {
                element.css('background-position', frame * size + 'px 0px');
                frame++;
                if (frame == 0) {
                    clearInterval(interval);
                }
            }, 273);
            $http({
                url: '/masterValveOpen',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        }

    };
    $scope.blowerOn = function() {
        $http({
            url: '/blowerOn',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
    $scope.blowerOff = function() {
        $http({
            url: '/blowerOff',
            method: "POST",
            data: {},
            headers: {'Content-Type': 'application/json'}
        }).then(function (result) {
            $scope.status = result.data;
        });
    };
});



