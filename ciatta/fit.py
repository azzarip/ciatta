class Fit:
    import pandas as pd
    
    def __init__(self, data):
        
        self.data = data
        self.max_stress_index = data['stress'].idxmax()
        self.cutOffData()
        
        self.fit_step = round(self.max_stress_index / 10)
        self.fit_results = self.fit()
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
        return None
    
    def fit(self):
        import pandas as pd
        from scipy.stats import linregress
        
    
        results = pd.DataFrame()
        for i in range(8):
            df = self.data.loc[self.fit_step*i:self.fit_step*(i+2)]
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
            results = pd.concat([results, result], ignore_index=True)
        return results