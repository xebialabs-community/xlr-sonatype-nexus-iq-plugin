# Preface #

This document describes the functionality provided by the xlr-sonatype-nexus-iq-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

# CI status #

[![Build Status][xlr-sonatype-nexus-iq-travis-image] ][xlr-sonatype-nexus-iq-travis-url]
[![Build Status][xlr-sonatype-nexus-iq-codacy-image] ][xlr-sonatype-nexus-iq-codacy-url]
[![Build Status][xlr-sonatype-nexus-iq-code-climate-image] ][xlr-sonatype-nexus-iq-code-climate-url]


[xlr-sonatype-nexus-iq-travis-image]: https://travis-ci.org/vanstoner/xlr-sonatype-nexus-iq-plugin.svg?branch=master
[xlr-sonatype-nexus-iq-travis-url]: https://travis-ci.org/vanstoner/xlr-sonatype-nexus-iq-plugin
[xlr-sonatype-nexus-iq-codacy-image]: https://api.codacy.com/project/badge/Grade/b78313b1eb1b4b058dc4512b4d48c26f
[xlr-sonatype-nexus-iq-codacy-url]: https://www.codacy.com/app/rvanstone/xlr-sonatype-nexus-iq-plugin
[xlr-sonatype-nexus-iq-code-climate-image]: https://codeclimate.com/github/vanstoner/xlr-sonatype-nexus-iq-plugin/badges/gpa.svg
[xlr-sonatype-nexus-iq-code-climate-url]: https://codeclimate.com/github/vanstoner/xlr-sonatype-nexus-iq-plugin


# Overview #

The xlr-sonatype-nexus-iq-plugin is a XL Release plugin that enables the evaluation of a binary within Nexus IQ

## Installation ##

Place the latest released version under the `plugins` dir.

This plugin (0.0.1+) requires XLR 6.1x+

## Types ##

+ Evaluate Binary

   `<property name="binaryUrl"        category="input" description="Location of the binary to be evaluated" />
    <property name="nexusiqApp"       category="input" description="Name of Application in Nexus IQ" />
    <property name="nexusiqStage"     category="input" description="Stage of release" kind="enum">`

## Tiles ##

+ Summary Report of Evaluations

  ![image](images/SonatypeNexusTile.png)
