describe('Nexus IQ Report Tile', () => {

    beforeAll(() => {
        fixtures().release({
            id: 'ReleaseWithNexusIqReport',
            status: 'planned',
            summary: {
                tiles: [{
                    type: 'nexusiq.NexusIqReport',
                    title: 'Nexus IQ Report Tile',
                    greetingName: 'sample tile'
                }]
            }
        });

        LoginPage.login('admin', 'admin');
    });

    afterAll(() => {
        LoginPage.logout();
        fixtures().clean();
    });

    it("should display Nexus IQ Report Tile with greetings in capital case", () => {
        DashboardPage.openDashboardOfRelease('ReleaseWithNexusIqReport')
            .getTile('Nexus IQ Report Tile')
            .expectContent('Sample tile');
    });

});
