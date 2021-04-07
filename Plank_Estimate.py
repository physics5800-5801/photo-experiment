import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

# create_energy_df:
#   Vs_data - TODO
#
#   returns the TODO
def create_energy_df(Vs_data):
  c = 299792458
  n_air = 1.000293
  e = -1.602176634e-19

  energy_df = pd.DataFrame([], columns=['λ', 'ν', 'V_s', 'E'])
  energy_df['λ'] = (Vs_data[:,0] * 1e-09)
  energy_df['ν'] = c / (n_air * energy_df['λ'])
  energy_df['V_s'] = Vs_data[:,1]
  energy_df['E'] = abs(e) * energy_df['V_s']
  return energy_df.sort_values(by=['λ'])

# plot_energy_data:
#   energy_df - TODO
#
#   returns the TODO
def plot_energy_data(energy_df, margin=1e-20):
  frequency = np.array(energy_df['ν'], dtype='float').reshape(-1,1)
  energy = np.array(energy_df['E'], dtype='float').reshape(-1,1)
  led_color = get_colors(energy_df['λ'])

  led_model = LinearRegression()
  led_model.fit(frequency, energy)
  weights = np.array([led_model.intercept_, led_model.coef_], dtype=object).flatten()

  Y_pred = weights[1]*frequency + weights[0]
  plt.scatter(frequency, energy, color=led_color)
  print(min(Y_pred), max(Y_pred))
  plt.plot([min(frequency), max(frequency)], [min(Y_pred), max(Y_pred)], linestyle='dashed', color='darkgray')
  plt.title('Plank\'s Constant', fontsize=18)
  plt.xlabel('Frequency (Hz)', fontsize=14)
  plt.ylabel('Energy (J)', fontsize=14)
  plt.ylim(min(Y_pred)-margin, max(Y_pred)+margin)
  plt.grid()
  plt.show()
  print('w0 = {}, w1 = {}\n'.format(weights[0], weights[1]))
  print('h = {:.8e} J⋅s'.format(weights[1]))
  return weights[1]

# get_h_error:
#   h_exp - TODO
#
#   returns the TODO
def get_h_error(h_exp):
  h = 6.62607015e-34
  error = abs((h - h_exp) / h) * 100
  print('h     =', h, '\nh_exp = {:.8e}'.format(h_exp))
  print('\n% error = {:.4f}%'.format(error))
  return error

### MAIN ###
Vs_led1a = np.array([[404,1.3850],
                    [458.5,1.0050],
                    [509.3,0.7360],
                    [591.1,0.3430],
                    [624.1,0.2790]])
Vs_led1b = np.array([[404,1.3850],
                    [458.5,1.0050],
                    [509.3,0.7360]])
Vs_led2 = np.array([[404,1.3210],
                    [458.5,0.9840],
                    [509.3,0.7380]])
Vs_laser1 = np.array([[405.8,1.4380],
                    [530.3,0.7510],
                    [654.9,0.3780]])
Vs_led3 = np.array([[404,1.3850],
                    [458.5,1.0050],
                    [509.3,0.7360],
                    [591.1,0.3990],
                    [624.1,0.3400]])
Vs_data = np.array([[404,1.3850],
                    [458.5,1.0050],
                    [509.3,0.7360],
                    [591.1,0.3990],
                    [624.1,0.3400]])
energy_df = create_energy_df(Vs_data)
h_exp = plot_energy_data(energy_df)
print('\n')
error = get_h_error(h_exp)
