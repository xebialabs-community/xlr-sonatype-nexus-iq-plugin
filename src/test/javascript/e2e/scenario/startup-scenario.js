describe('NexusIqReport', () => {

    it("should let XL Release start normally", () => {
        LoginPage.login('admin', 'admin');
    });

    afterAll(() => {
        LoginPage.logout();
    });

});
