/*
 * Copyright 2019 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
'use strict';

(function () {

    var NexusiqQueryTileViewController = function ($scope, NexusiqQueryService, XlrTileHelper) {
        var vm = this;

        vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;

        var tile;
        var secLevel;
        var application;

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
            "develop"       : "powderblue",
            "build"         : "lightblue",
            "stage-release" : "blue",
            "release"       : "darkblue"

          }
         
        }

       if ($scope.xlrDashboard) {
            // summary page
            vm.release = $scope.xlrDashboard.release;
            vm.tile = $scope.xlrTile.tile;
            if (vm.tile.properties == null) {
                vm.config = vm.tile.configurationProperties;
            } else {
                // new style since 7.0
                vm.config = vm.tile.properties;
            }
            secLevel = vm.config.secLevel;
            application = vm.config.application;
        }

        function tileConfigurationIsPopulated() {
            return !_.isEmpty(vm.config.nexusiqServer);
        }


        function getColor(value) {
            if (Object.keys(predefinedColors).indexOf(secLevel) > -1)
              return predefinedColors[secLevel][value];
            else
              return predefinedColors["default"][value];
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
                NexusiqQueryService.executeQuery(vm.tile.id, config).then(
                    function (response) {
                        var nexusiqPolicyViolationsArray = [];
                        var policyViolations = JSON.parse(response.data.data);
                        console.log(policyViolations);
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
                            vm.policyViolationsQueryData.data = _.reduce(policyViolations[secLevel], function (result, value) {
                                var state = value.stageId;
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

