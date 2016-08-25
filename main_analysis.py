import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import blaze as blz
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# prepare data for analysis

data = blz.by(blz.merge(ds1.Carrier, ds1.Origin, ds1.Month, ds1.Year), 
              ndelay=ds1.DepDel15.sum(), nflights=ds1.Flights.sum())
data = blz.into(pd.DataFrame, data)
data['ym'] = data['Year'] + 0.01*data['Month']
data['AATWA'] = 1*(data['ym']>=2001.04)
data['USAW'] = 1*(data['ym']>=2005.09)
data['DLNW'] = 1*(data['ym']>=2009.12)
data['UACA'] = 1*(data['ym']>=2010.10)
data['AAUS'] = 1*(data['ym']>=2013.12)
data['AAUScomplete'] = 1*(data['ym']>=2015.10)

# run OLS on data

model = smf.ols(formula = 'ndelay ~ AATWA + USAW + DLNW + UACA + AAUS + AAUScomplete + nflights + C(Carrier) + C(Origin) + C(Year) + C(Month)', data=data)
results = model.fit()

# graph heterogeneous effects by carrier

heterogeneous = pd.DataFrame()
heterogeneous['carrier'] = ['B6', 'B6', 'WN', 'WN', 'F9', 'F9', 'AA', 'AA', 'DL', 'DL', 'UA', 'UA']
heterogeneous['merge'] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
heterogeneous['ndelay'] = [np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="B6"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="B6"]),
                          np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="WN"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="WN"]),
                          np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="F9"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="F9"]),
                          np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="AA"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="AA"]),
                          np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="DL"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="DL"]),
                          np.mean(data['ndelay'][data['AAUS']==0][data['Carrier']=="UA"]),
                          np.mean(data['ndelay'][data['AAUS']==1][data['Carrier']=="UA"])]
sns.barplot(x="carrier", y="ndelay", hue="merge", data=heterogeneous)
plt.ylabel('Number of delays per month and airport')
plt.xlabel('Carrier')
