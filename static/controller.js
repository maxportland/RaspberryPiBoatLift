var app = angular.module('liftApp', []);
app.controller('boatLiftController', function($scope, $http, $timeout) {
    $scope.status = {
        "lift_state": "",
        "blower_state": "",
        "master_valve_state": "",
        "rear_valve_state": "",
        "front_valve_state": ""
    };
    $scope.valves = [
        {state:'master_valve_state', url: '/masterValve', name:'MASTER VALVE'},
        {state:'front_valve_state', url: '/frontValve', name:'FRONT VALVE'},
        {state:'rear_valve_state', url: '/rearValve', name:'REAR VALVE'}
    ];
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
    $scope.toggleValve = function(event, valve_state, valve_url) {
        var element = angular.element( event.currentTarget ).children( ".switch" )[0];

        if($scope.status[ valve_state ] == "closed") {
            var size = 30;
            var frame = -1;
            var interval = setInterval(function() {
                $( element ).css('background-position', frame * size + 'px 0px');
                frame--;
                if (frame == -12) {
                    clearInterval(interval);
                }
            }, 273);
            $http({
                url: valve_url + 'Open',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
                $( element ).removeAttr("style");
            });
        } else if($scope.status[ valve_state ] == "open") {
            var size = 30;
            var frame = -12;
            var interval = setInterval(function() {
                $( element ).css('background-position', frame * size + 'px 0px');
                frame++;
                if (frame == -1) {
                    clearInterval(interval);
                }
            }, 273);
            $http({
                url: valve_url + 'Close',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
                $( element ).removeAttr("style");
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



