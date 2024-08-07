class Plot:
    from .fit import Fit

    def __init__(self, fit, filename: str):
        self.fit = fit
        self.fit_results = fit.results
        self.data = fit.data
        self.filename = filename
        self.plot()
        self.plotError()

    def plot(self):
        import matplotlib.pyplot as plt
        plt.plot(self.data['strain'], self.data['stress'])
        plt.xlabel('Strain')
        plt.ylabel('Stress [Pa]')
        plt.title(self.filename)

        self.plotBestFit()

        plt.legend(['Data', 'Young Modulus'])
        plt.subplots_adjust(left=0.15)
        plt.savefig('plots/'+self.filename + '.png')
        plt.close()
        # plt.draw()
        # plt.pause(0.2)

    def plotError(self):
        import matplotlib.pyplot as plt

        y = 1/self.fit.fit_results['error']
        plt.plot(self.fit.fit_results['x'], y)
        plt.axhline(y=y.mean(), color='green', linestyle='--')
        plt.savefig('plots/error_' + self.filename + '.png')
        plt.title(self.filename)
        plt.close()

    def plotBestFit(self):
        import matplotlib.pyplot as plt
        max_stress = self.data['stress'].max()
        max_strain = (
            max_stress - self.fit_results['Intercept [Pa]']) / self.fit_results['Young Modulus [Pa]']

        max_strain = max_strain[0]
        strain_range = self.data[self.data['strain'] < max_strain]['strain']
        line = self.fit_results['Young Modulus [Pa]'][0] * \
            strain_range + self.fit_results['Intercept [Pa]'][0]

        plt.plot(strain_range, line, linestyle='--')
