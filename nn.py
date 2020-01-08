import numpy as np
import keras as keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from numpy import genfromtxt

x = genfromtxt('ratios.csv', delimiter=',')
x = x[:,:-2]
y = x[:,-1]
print(x)
exit()
Xmean = np.mean(x,axis=0)
X_norm = np.subtract(x,Xmean)
Xstdev = np.std(X_norm,axis=0)
X_norm = np.true_divide(X_norm,Xstdev)
x = X_norm[:,:]
x[:,4] = np.zeros(36)

model = Sequential()
model.add(Dense(input_dim=9,units=10, activation='tanh', use_bias=True, kernel_initializer ='RandomUniform', bias_initializer='ones'))

model.add(Dense(units=10, activation='tanh', use_bias=True, kernel_initializer = 'RandomUniform', bias_initializer='ones'))

model.add(Dense(1, activation='tanh', use_bias=True, kernel_initializer = 'RandomUniform',bias_initializer='ones'))

model.compile(optimizer='Adam', loss='mean_absolute_error')

model.fit(x, y, epochs=10, validation_data = (x,y), batch_size=2)

ynew = model.predict(x)
print(ynew)
