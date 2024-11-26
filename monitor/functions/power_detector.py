from functions import file_handling
import numpy as np
from scipy.stats import iqr, shapiro
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest

def iqr_detection(list_power,active_power,iqr_factor = 1.5):
    Q1 = np.percentile(list_power, 25)
    Q3 = np.percentile(list_power, 75)
    IQR = iqr(list_power)
    
    lim_inf = Q1 - iqr_factor * IQR
    lim_sup = Q3 + iqr_factor * IQR
    power_alert = (active_power <= lim_inf) | (active_power >= lim_sup)
    
    return int(power_alert)

def z_score_detection(list_power, active_power, threshold = 3):
    _, p_value = shapiro(list_power)
    
    if p_value > 0.05:
        mean = np.mean(list_power)
        std = np.std(list_power)
        
        z_score = abs((active_power - mean)/std)
        power_alert = z_score > threshold
    else:
        power_alert = False
    
    return int(power_alert)

def iso_for_detection(list_power, active_power):
    iso_for = IsolationForest(contamination=0.03)
    iso_for.fit(np.array(list_power).reshape(-1,1))
    
    value = iso_for.predict([[active_power]])
    power_alert = True if value == -1 else False
    
    return int(power_alert)

def arima_detection(list_power,active_power):
    model = ARIMA(list_power, order=(0,1,0))
    model_fit = model.fit()
    y_pred = model_fit.forecast(steps=1)[0]
    error = abs(active_power - y_pred)
    threshold = 0.25 * y_pred
    
    power_alert = True if error > threshold else False
    
    return int(power_alert)

def power_outliers(active_power):
    data = file_handling.read_json('potency','electrical-data')
    
    list_date = []
    list_power = []
    
    # Select the last hour of data
    for x in data[-31:-1]:
        list_power.append(x['total-active-power'])
        list_date.append(x['date'])
    
    iqr_alert = iqr_detection(list_power,active_power)
    z_alert = z_score_detection(list_power,active_power)
    iso_alert = iso_for_detection(list_power,active_power)
    arima_alert = arima_detection(list_power,active_power)
    
    concordance_alert = 0 if min(list_power[-1],list_power[-2]) <= z_alert <= max(list_power[-1],list_power[-2]) else 1
    general_alert = ((iqr_alert + z_alert + iso_alert + arima_alert) >= 2) and concordance_alert
    
    if active_power >= list_power[-1] and general_alert:
        return 1
    elif active_power < list_power[-1] and general_alert:
        return -1
    else:
        return 0