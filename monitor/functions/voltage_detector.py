from functions import file_handling
import numpy as np
from scipy.stats import iqr, shapiro
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest

def iqr_detection(list_voltage,instant_energy,iqr_factor = 1.5):
    Q1 = np.percentile(list_voltage, 25)
    Q3 = np.percentile(list_voltage, 75)
    IQR = iqr(list_voltage)
    
    lim_inf = Q1 - iqr_factor * IQR
    lim_sup = Q3 + iqr_factor * IQR
    
    voltage_alert = (instant_energy <= lim_inf) | (instant_energy >= lim_sup)
    
    return int(voltage_alert)

def z_score_detection(list_voltage, instant_energy, threshold = 3):
    _, p_value = shapiro(list_voltage)
    
    if p_value > 0.05:
        mean = np.mean(list_voltage)
        std = np.std(list_voltage)
        
        z_score = abs((instant_energy - mean)/std)
        voltage_alert = z_score > threshold
    else:
        voltage_alert = False
    
    return int(voltage_alert)

def iso_for_detection(list_voltage, instant_energy):
    iso_for = IsolationForest(contamination=0.03)
    iso_for.fit(np.array(list_voltage).reshape(-1,1))
    
    value = iso_for.predict([[instant_energy]])
    voltage_alert = True if value == -1 else False
    
    return int(voltage_alert)

def arima_detection(list_voltage,instant_energy):
    model = ARIMA(list_voltage, order=(0,1,0))
    model_fit = model.fit()

    y_pred = model_fit.forecast(steps=1)[0]
    error = abs(instant_energy - y_pred)
    threshold = 0.05 * y_pred
    
    voltage_alert = True if error > threshold else False
    
    return int(voltage_alert)

def volt_outliers(instant_energy):
    data = file_handling.read_json('voltage','electrical-data')
    
    list_date = []
    list_voltage = []
    
    # Select the last hour of data
    for x in data[-31:-1]:
        list_voltage.append(x['instant_energy'])
        list_date.append(x['date'])
    
    iqr_alert = iqr_detection(list_voltage,instant_energy)
    
    z_alert = z_score_detection(list_voltage, instant_energy, threshold = 3)
    
    iso_alert = iso_for_detection(list_voltage,instant_energy)
    
    arima_alert = arima_detection(list_voltage,instant_energy)
    
    concordance_alert = 0 if min(list_voltage[-1],list_voltage[-2]) <= instant_energy <= max(list_voltage[-1],list_voltage[-2]) else 1
    
    general_alert = ((iqr_alert + z_alert + iso_alert + arima_alert) >= 2) and concordance_alert
    
    # print('iqr: ',iqr_alert)
    # print('z: ',z_alert)
    # print('isolation: ',iso_alert)
    # print('arima: ',arima_alert)
    
    if instant_energy >= list_voltage[-1] and general_alert:
        return 1
    elif instant_energy < list_voltage[-1] and general_alert:
        return -1
    else:
        return 0
