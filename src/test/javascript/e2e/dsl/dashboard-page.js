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

class DashboardPage {
    constructor() {
        Browser.waitFor('.xlr-dashboard');
    }

    static openDashboardOfRelease(releaseId) {
        browser.setLocation(`/releases/${releaseId}/summary`);
        return new DashboardPage();
    }

    getTile(content) {
        return new Tile(content);
    }
}

class Tile {
    constructor(title) {
        this.tileLocator = () => By.cssContainingText('.gridster-item', title);
        this.tile = () => element(this.tileLocator());
        expect(this.tile().isDisplayed()).toBe(true, `No tile displayed with title "${title}"`);
        this.clickButtonByTooltip = (tooltip) => {
            this.tile().element(By.css(`.panel-heading span[tooltip="'${tooltip}'"]`)).click();
            return this;
        }
    }

    expectContent(text) {
        expect(this.tile().element(By.cssContainingText('.panel-body', text)).isDisplayed())
            .toBe(true, `No tile displayed with content "${text}"`);
        return this;
    }

    openDetailsView() {
        this.clickButtonByTooltip('View details');
        return this;
    }

}

global.DashboardPage = DashboardPage;
global.Tile = Tile;
