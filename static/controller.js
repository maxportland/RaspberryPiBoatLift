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
        {'state': 'rear_valve_state', 'url': '/rearValves', 'name': 'REAR VALVES'},
        {'state': 'front_valve_state', 'url': '/frontValves', 'name': 'FRONT VALVES'},
        {'state': 'master_valve_state', 'url': '/masterValve', 'name': 'MASTER VALVE'}
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
    $scope.toggleEasyLift = function() {
        var element = angular.element( event.currentTarget ).children( ".easy-lift-button" )[0];
        $( element ).css('background-position', '0px 0px');
        $( element ).css('padding-top', '7px');
        var interval = setInterval(function() {
            $( element ).css('background-position', '-139px 0px');
            $( element ).css('padding-top', '8px');
            clearInterval(interval);
        }, 1000);
        if($scope.status.lift_state == "down") {
            $http({
                url: '/up',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        } else if($scope.status.lift_state == "up") {
            $http({
                url: '/down',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        }
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
    $scope.blowerToggle = function() {
        if($scope.status.blower_state == "off") {
            $http({
                url: '/blowerOn',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        } else {
            $http({
                url: '/blowerOff',
                method: "POST",
                data: {},
                headers: {'Content-Type': 'application/json'}
            }).then(function (result) {
                $scope.status = result.data;
            });
        }
    };
});



