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

Vs_data = np.array([[404,1.3850],
                    [458.5,1.0050],
                    [509.3,0.7360],
                    [591.1,0.3430],
                    [624.1,0.2790]])
energy_df = create_energy_df(Vs_data)
h_exp = plot_energy_data(energy_df)
print('\n')
error = get_h_error(h_exp)
