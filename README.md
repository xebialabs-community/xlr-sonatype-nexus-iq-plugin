# Preface #

This document describes the functionality provided by the xlr-sonatype-nexus-iq-plugin-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

# CI status #

[![Build Status][xlr-sonatype-nexus-iq-plugin-travis-image] ][xlr-sonatype-nexus-iq-plugin-travis-url]
[![Build Status][xlr-sonatype-nexus-iq-plugin-codacy-image] ][xlr-sonatype-nexus-iq-plugin-codacy-url]
[![Build Status][xlr-sonatype-nexus-iq-plugin-code-climate-image] ][xlr-sonatype-nexus-iq-plugin-code-climate-url]
[![License: MIT][xlr-sonatype-nexus-iq-plugin-license-image] ][xlr-sonatype-nexus-iq-plugin-license-url]
[![Github All Releases][xlr-sonatype-nexus-iq-plugin-downloads-image] ]()


[xlr-sonatype-nexus-iq-plugin-travis-image]: https://travis-ci.org/vanstoner/xlr-sonatype-nexus-iq-plugin-plugin.svg?branch=master
[xlr-sonatype-nexus-iq-plugin-travis-url]: https://travis-ci.org/vanstoner/xlr-sonatype-nexus-iq-plugin-plugin
[xlr-sonatype-nexus-iq-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/b78313b1eb1b4b058dc4512b4d48c26f
[xlr-sonatype-nexus-iq-plugin-codacy-url]: https://www.codacy.com/app/rvanstone/xlr-sonatype-nexus-iq-plugin-plugin
[xlr-sonatype-nexus-iq-plugin-code-climate-image]: https://codeclimate.com/github/vanstoner/xlr-sonatype-nexus-iq-plugin-plugin/badges/gpa.svg
[xlr-sonatype-nexus-iq-plugin-code-climate-url]: https://codeclimate.com/github/vanstoner/xlr-sonatype-nexus-iq-plugin-plugin
[xlr-sonatype-nexus-iq-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-sonatype-nexus-iq-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-sonatype-nexus-iq-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-sonatype-nexus-iq-plugin/total.svg


# Overview #

The xlr-sonatype-nexus-iq-plugin is a XL Release plugin that enables the evaluation of a binary within Nexus IQ

## Dependencies ##
You need to install the [NexusIQ command line interface (CLI)](https://books.sonatype.com/sonatype-clm-book/html/book/cli.html) local to your XL Release Server

## Installation ##

Place the latest released version under the `plugins` dir.

This plugin (1.0.0+) requires XLR 6.1x+

## Types ##

+ Evaluate Binary

   - binaryUrl - Location of the binary to be evaluated (Could be local to XLR or a URL (e.g. Jenkins workspace)
   - nexusiqApp - Name of Application in Nexus IQ
   - nexusiqStage - Stage of release [develop|build|stage-release|release|operate]

  ![evaluate binary](images/evaluateBinary.png)
   
## Tiles ##

+ Summary Report of Evaluations

  ![evaluation report](images/latestEvaluationReport.png)
