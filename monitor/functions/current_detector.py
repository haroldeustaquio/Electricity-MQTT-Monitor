from functions import file_handling
import numpy as np
from scipy.stats import iqr, shapiro
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest

def iqr_detection(list_current,rms_current,iqr_factor = 1.5):
    Q1 = np.percentile(list_current, 25)
    Q3 = np.percentile(list_current, 75)
    IQR = iqr(list_current)
    
    lim_inf = Q1 - iqr_factor * IQR
    lim_sup = Q3 + iqr_factor * IQR
    current_alert = (rms_current <= lim_inf) | (rms_current >= lim_sup)
    
    return int(current_alert)

def iso_for_detection(list_current, rms_current):
    iso_for = IsolationForest(contamination=0.03)
    iso_for.fit(np.array(list_current).reshape(-1,1))
    
    value = iso_for.predict([[rms_current]])
    current_alert = True if value == -1 else False
    
    return int(current_alert)

def arima_detection(list_current,rms_current):
    model = ARIMA(list_current, order=(0,1,0))
    model_fit = model.fit()
    y_pred = model_fit.forecast(steps=1)[0]
    error = abs(rms_current - y_pred)
    threshold = 0.25 * y_pred
    
    current_alert = True if error > threshold else False
    
    return int(current_alert)

def current_outliers(rms_current):
    data = file_handling.read_json('current','electrical-data')
    
    list_date = []
    list_current = []
    
    # Select the last hour of data
    for x in data[-31:-1]:
        list_current.append(x['rms_current'])
        list_date.append(x['date'])
    
    iqr_alert = iqr_detection(list_current,rms_current)
        
    iso_alert = iso_for_detection(list_current,rms_current)
    
    arima_alert = arima_detection(list_current,rms_current)
    
    concordance_alert = 0 if min(list_current[-1],list_current[-2]) <= rms_current <= max(list_current[-1],list_current[-2]) else 1
    
    general_alert = ((iqr_alert + iso_alert + arima_alert) >= 2) and concordance_alert
    
    # print('iqr: ',iqr_alert)
    # print('isolation: ',iso_alert)
    # print('arima: ',arima_alert)
    
    if rms_current >= list_current[-1] and general_alert:
        return 1
    elif rms_current < list_current[-1] and general_alert:
        return -1
    else:
        return 0