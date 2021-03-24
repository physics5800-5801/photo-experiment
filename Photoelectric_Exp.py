import piplates.DAQC2plate as DAQC2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import LinearRegression

# create_energy_df:
#   wavelengths - TODO
#
#   returns the TODO
def get_colors(wavelengths):
  colors = []
  wavelengths_nm = (wavelengths / 1e-09) if (wavelengths.size > 1) else np.array([wavelengths / 1e-09])
  for λ in (wavelengths_nm):
    if (λ >= 400 and λ < 450):
      colors.append('darkviolet')
    elif (λ >= 450 and λ < 500):
      colors.append('blue')
    elif (λ >= 500 and λ < 570):
      colors.append('forestgreen')
    elif (λ >= 570 and λ < 590):
      colors.append('gold')
    elif (λ >= 590 and λ < 610):
      colors.append('darkorange')
    elif (λ >= 610 and λ <= 700):
      colors.append('red')
    else:
      colors.append('black')
  return colors if (len(colors) > 1) else colors[0]
  
# create_LED_df:
#   led_data - TODO
#
#   returns the TODO
def create_LED_df(led_data):
  led_df = pd.DataFrame([], columns=['V_r', 'I_ub', 'I_b', 'I_φ'])
  led_df['V_r'] = led_data[:,0]
  led_df['I_ub'] = led_data[:,1]
  led_df['I_b'] = led_data[:,2]
  led_df['I_φ'] = led_data[:,1] + led_data[:,2]
  return led_df.sort_values(by=['V_r'])

# get_train_data:
#   X - TODO
#   Y - TODO
#   mode - 

#   returns the TODO
def get_train_data(X, Y, mode=None):
  X_train = X.copy()
  Y_train = Y.copy()
  if (mode is 'linear'):
    m_sec = np.zeros(X.size-1)
    for i in range(m_sec.size):
      m_sec[i] = (Y[i+1]-Y[i])/((X[i+1]-X[i]))
    m_sec = m_sec[m_sec > (m_sec.max()/2)]
    X_train = X_train[:m_sec.size+1]
    Y_train = Y_train[:m_sec.size+1]
  return (X_train, Y_train)

# plot_LED_data:
#   led_df - TODO
#   wavelength_nm - TODO
#   line_color - TODO
#
#   returns the TODO
def plot_LED_data(led_df, wavelength_nm):
  retarding_voltage = np.array(led_df['V_r'], dtype='float').reshape(-1,1)
  photocurrent = np.array(led_df['I_φ'], dtype='float').reshape(-1,1)

  #train_voltage, train_current = get_train_data(retarding_voltage, photocurrent, None)

  #led_model = LinearRegression()
  #led_model.fit(train_voltage, train_current)
  #weights = np.array([led_model.intercept_, led_model.coef_], dtype=object).flatten()

  #Y_pred = weights[1]*retarding_voltage + weights[0]
  plt.scatter(retarding_voltage, photocurrent, color='black')
  #plt.plot([min(retarding_voltage), max(retarding_voltage)], [min(Y_pred), max(Y_pred)], linestyle='dashed', color=get_colors(wavelength_nm*1e-09))
  #plt.plot([min(retarding_voltage), max(retarding_voltage)], [0, 0], linestyle='dashed', color='gray')
  plt.title('{λ}nm LED Stopping Voltage'.format(λ=wavelength_nm), fontsize=18)
  plt.xlabel('Retarding Voltage (V)', fontsize=14)
  plt.ylabel('Photocurrent (µA)', fontsize=14)
  plt.gca().invert_yaxis()
  plt.grid()
  plt.show()
  #print('w0 = {}, w1 = {}\n'.format(weights[0], weights[1]))
  index = -1
  for i in range(photocurrent.size):
      if (photocurrent[i] >= 0):
          index = i
          break

  V_s = retarding_voltage[index][0]
  print('V_s = {:.4f} V'.format(V_s))
  return V_s

### MAIN
voltages = np.arange(0, 1, 0.001)
np.random.shuffle(voltages)
led_data = np.zeros((voltages.size,3))
dark_current = 1.3e-03

for i in range(voltages.size):
    Vr = voltages[i]
    led_data[i,0] = Vr
    DAQC2.setDAC(0,0,Vr)
#   time.sleep(1)
    Vp = DAQC2.getADC(0,0) - DAQC2.getADC(0,1)
    led_data[i,1] = Vp
    led_data[i,2] = dark_current

wavelength = 654
led_df = create_LED_df(led_data)
plot_LED_data(led_df, np.array(wavelength))

