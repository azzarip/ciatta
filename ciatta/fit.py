class Fit:
    import pandas as pd

    def __init__(self, data):

        self.data = data
        self.max_stress_index = data['stress'].idxmax()
        self.cutOffData()

        self.fit_step = 0.09
        self.fstep_fraction = 5

        self.fit_results = self.get_fits()
        self.results = self.getResults()

    def getResults(self) -> pd.DataFrame:
        import pandas as pd

        maxValues = self.data.iloc[self.max_stress_index]

        best_result = self.fit_results.loc[self.fit_results['slope'].idxmax()]

        return pd.DataFrame({
            'Max Stress [Pa]': [maxValues['stress']],
            'Max Strain': [maxValues['strain']],
            'Max Force [N]': [maxValues['force']],
            'Young Modulus [Pa]': [best_result['slope']],
            'Intercept [Pa]': [best_result['intercept']],
            'pValue': [best_result['p_value']]
        })

    def cutOffData(self):
        self.data = self.data.iloc[0:self.max_stress_index + 1]
        self.data = self.data[(self.data['stress'] >= 0)
                              & (self.data['strain'] >= 0)]
        return None

    def fit(self, df):
        import pandas as pd
        from scipy.stats import linregress

        x = df['strain']
        y = df['stress']
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        error = y - (slope * x + intercept)
        result = pd.DataFrame({
            'slope': [slope],
            'intercept': [intercept],
            'p_value': [p_value],
            'error': [error.pow(2).sum()]
        })
        return results

    def find_step_index(self, start_index):
        start_strain = self.data.loc[start_index, 'strain']
        for i in range(start_index + 1, len(self.data)):
            if self.data.loc[i, 'strain'] - start_strain >= self.fit_step:
                return i
        return len(df)

    def get_fits(self):
        index = 0
        results = pd.DataFrame()

        while index < len(df):
            end_index = find_step_index(index)
            df = self.data.iloc[index:end_index]

            if len(df) < 2:
                break

            result = fit(df)
            results = pd.concat([results, result], ignore_index=True)

            step_size = (end_index - index) / self.step_fraction
            index = int(current_index + step_size)

        return results
