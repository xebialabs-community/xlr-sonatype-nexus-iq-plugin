/**
 * Copyright 2019 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
 'use strict';

let browserName = process.env.KARMA_BROWSER;
if (!browserName) {
    browserName = 'firefox';
}

exports.config = {
    capabilities: {
        browserName: browserName.toLowerCase()
    },
    baseUrl: 'http://localhost:5516',
    directConnect: true,
    specs: [
        './e2e/scenario/**/*.js'
    ],
    jasmineNodeOpts: {
        showColors: true,
        defaultTimeoutInterval: 60 * 1000
    },
    framework: 'jasmine2',
    onPrepare: function () {
        global.requestPromise = require('request-promise');
        global._ = require('lodash');

        let SpecReporter = require('jasmine-spec-reporter');
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: true}));

        require('./e2e/dsl/fixtures-ci-builder.js');

        let dslFiles = require("glob").sync("./e2e/dsl/**/*.js", {cwd: __dirname});
        _.each(dslFiles, require);

        Browser.open();
        Browser.setSize(1024, 768);
        browser.manage().timeouts().setScriptTimeout(60 * 1000);
    }
};
