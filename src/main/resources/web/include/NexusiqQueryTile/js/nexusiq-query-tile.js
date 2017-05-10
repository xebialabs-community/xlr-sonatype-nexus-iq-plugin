'use strict';

(function () {

    var NexusiqQueryTileViewController = function ($scope, NexusiqQueryService, XlrTileHelper) {
        var vm = this;

        vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;

        var tile;
        var secLevel;
        var appName;

        var predefinedColors = {
          "Security-High" : {
            "develop"       : "LightSalmon",
            "build"         : "IndianRed",
            "stage-release" : "firebrick",
            "release"       : "red"
          },
          "Security-Medium" : {
            "develop"       : "bisque",
            "build"         : "sandybrown",
            "stage-release" : "chocolate",
            "release"       : "maroon"

          },
          "Security-Low" : {
            "develop"       : "green",
            "build"         : "mediumseagreen",
            "stage-release" : "springgreen",
            "release"       : "SeaGreen"
          },
          "default" : {
            "develop"       : "powederblie",
            "build"         : "lightblue",
            "stage-release" : "blue",
            "release"       : "darkblue"

          }
         
        }

        if ($scope.xlrTile) {
            // summary mode
            tile = $scope.xlrTile.tile;
            secLevel = tile.configurationProperties.secLevel;
        }
        console.log(tile.configurationProperties);

        function getColor(value) {
            if (Object.keys(predefinedColors).indexOf(secLevel) > -1)
              return predefinedColors[secLevel][value];
            else
              return predefinedColors["default"][value];
        }

        function tileConfigurationIsPopulated() {
            var config = tile.configurationProperties;
            return !_.isEmpty(config.nexusiqServer);
        }

        function toUpperCaseFirst(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }


        vm.chartOptions = {
            topTitleText: secLevel.split("-")[0],
            bottomTitleText: secLevel.split("-")[1],
            series: function (data) {
                var series = {
                    name: 'State',
                    data: []
                };
                series.data = _.map(data.data, function (value) {
                    return {y: value.counter, name: value.state, color: value.color};
                });
                return [ series ];
            },
            showLegend: false,
            donutThickness: '70%'
        };

        function load(config) {
            if (tileConfigurationIsPopulated()) {
                vm.loading = true;
                console.log("doing some stuff");
                NexusiqQueryService.executeQuery(tile.id, config).then(
                    function (response) {
                        var nexusiqPolicyViolationsArray = [];
                        var policyViolations = JSON.parse(response.data.data);
                        console.log("about to get policy Violations");                      
                        console.log(policyViolations);
                        console.log("How do I get rid of quotes " + secLevel);
                        if(policyViolations[0] === "Invalid request"){
                            console.log("Invalid request");
                            vm.invalidRequest = true;
                        }
                        else{
                            vm.invalidRequest = false;
                            vm.states = [];
                            vm.statesCounter = 0;
                            vm.policyViolationsQueryData = {
                                data: null,
                                total: 0
                            };
                            $scope.xlrTile.title = $scope.xlrTile.title + " : " + policyViolations[secLevel][0].appName;
                            vm.policyViolationsQueryData.data = _.reduce(policyViolations[secLevel], function (result, value) {
                                
                                var state = value.stageId;
                                console.log("We now have a state" + state);
                                vm.policyViolationsQueryData.total += 1;
                                if (result[state]) {
                                    result[state].counter += 1;
                                } else {
                                    result[state] = {
                                        counter: 1,
                                        color: getColor(state),
                                        state: state
                                    };
                                }
                                return result;

                            }, {});
                            _.forEach(vm.policyViolationsQueryData.data, function (value, key) {
                                if (vm.statesCounter < 5) vm.states.push(value);
                                vm.statesCounter++;
                            });
                        }
                    }
                    ).finally(function () {
                        vm.loading = false;

                    });
                }
            }


            function refresh() {
                load({params: {refresh: true}});
            }

            load();

            vm.refresh = refresh;
        };

        NexusiqQueryTileViewController.$inject = ['$scope', 'xlrelease.nexusiq.NexusiqQueryService', 'XlrTileHelper'];

        var NexusiqQueryService = function (Backend) {

            function executeQuery(tileId, config) {
                return Backend.get("tiles/" + tileId + "/data", config);
            }

            return {
                executeQuery: executeQuery
            };
        };

        NexusiqQueryService.$inject = ['Backend'];

        angular.module('xlrelease.nexusiqquery.tile', []);
        angular.module('xlrelease.nexusiqquery.tile').service('xlrelease.nexusiq.NexusiqQueryService', NexusiqQueryService);
        angular.module('xlrelease.nexusiqquery.tile').controller('nexusiq.NexusiqQueryTileViewController', NexusiqQueryTileViewController);

    })();

