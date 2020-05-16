import pandas as pd


class Process:

    def __init__(self, path):
        self.df = pd.read_csv(path)
        # self.df_test_features = pd.read_csv(testfeatures)
        # self.df_test_features.drop(columns = ['jobId', 'companyId'], axis = 1, inplace = True)
        # self.df_test_features.rename(columns={
        #                           'jobType':'Job Type','degree':'Degree','major':'Major',
        #                           'industry':'Industry','yearsExperience':'Experience (Years)',
        #                          'milesFromMetropolis':'Miles from Metropolis'}, inplace = True)

    def getMergedData(self):
        return self.df

    def getPredictionColumns(self):
        features = [
            'Job Type_CEO',
            'Job Type_CFO',
            'Job Type_CTO',
            'Job Type_JANITOR',
            'Job Type_JUNIOR',
            'Job Type_MANAGER',
            'Job Type_SENIOR',
            'Job Type_VICE_PRESIDENT',
            'Degree_BACHELORS',
            'Degree_DOCTORAL',
            'Degree_HIGH_SCHOOL',
            'Degree_MASTERS',
            'Degree_NONE',
            'Major_BIOLOGY',
            'Major_BUSINESS',
            'Major_CHEMISTRY',
            'Major_COMPSCI',
            'Major_ENGINEERING',
            'Major_LITERATURE',
            'Major_MATH',
            'Major_NONE',
            'Major_PHYSICS',
            'Industry_AUTO',
            'Industry_EDUCATION',
            'Industry_FINANCE',
            'Industry_HEALTH',
            'Industry_OIL',
            'Industry_SERVICE',
            'Industry_WEB']

        return features


    def getJobTypes(self):
        return [
            'CEO',
            'CFO',
            'CTO',
            'JANITOR',
            'JUNIOR',
            'MANAGER',
            'SENIOR',
            'VICE PRESIDENT'
        ]

    def getDegree(self):
        return [
            'BACHELORS',
            'DOCTORAL',
            'HIGH SCHOOL',
            'MASTER',
            'NONE'
        ]

    def getMajor(self):
        return ['BIOLOGY', 'BUSINESS', 'CHEMISTRY', 'COMPSCI', 'ENGINEERING',
       'LITERATURE', 'MATH', 'NONE']

    def getIndustry(self):
        return ['AUTO', 'EDUCATION', 'FINANCE', 'HEALTH', 'OIL', 'SERVICE', 'WEB']


    def ExpSalary(self):
        _df = self.df.groupby('Job Type').mean()[['Experience (Years)', 'Salary']]
        return _df, _df.index
# plt.scatter(x = df['Experience (Years)'], y = df['Salary'])