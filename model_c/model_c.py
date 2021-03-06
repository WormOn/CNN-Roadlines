import numpy as np

from keras.models import Model
from keras.layers import Activation, Dropout
from keras.layers import Conv2D, Deconv2D
from keras.layers import MaxPool2D, UpSampling2D
from keras.layers import Input, Concatenate
from keras.layers.normalization import BatchNormalization

input_shape = (80, 160, 3)
pool_size = (2, 2)

### Model ###

u = Input(shape=input_shape)

# Normalizes incoming inputs. First layer needs the input shape to work
i = BatchNormalization(input_shape=input_shape)(u)

i = Conv2D(16, 3, padding='valid', activation='relu', name='Conv0')(i)

# A

a = Conv2D(16, 3, padding='valid', activation='relu', name='Conv1A')(i)

a = Dropout(0.1)(a)

a = MaxPool2D(pool_size=pool_size, name='Pooling1A')(a)

# B

b = Conv2D(16, 3, padding='valid', activation='relu', name='Conv1B')(i)

b = MaxPool2D(pool_size=pool_size, name='Pooling1B')(b)

b = Conv2D(32, 3, padding='valid', activation='relu', name='Conv2B')(b)

b = Dropout(0.1)(b)

b = MaxPool2D(pool_size=pool_size, name='Pooling2B')(b)

# C

c = Conv2D(16, 3, padding='valid', activation='relu', name='Conv1C')(i)

c = MaxPool2D(pool_size=pool_size, name='Pooling1C')(c)

c = Conv2D(32, 3, padding='valid', activation='relu', name='Conv2C')(c)

c = Dropout(0.1)(c)

c = MaxPool2D(pool_size=pool_size, name='Pooling2C')(c)

c = Conv2D(64, 3, padding='valid', activation='relu', name='Conv3C')(c)

c = Dropout(0.1)(c)

c = MaxPool2D(pool_size=pool_size, name='Pooling3C')(c)

# D

d = Conv2D(16, 11, padding='valid', activation='relu', name='Conv1D')(i)

d = Dropout(0.1)(d)

d = MaxPool2D(pool_size=pool_size, name='Pooling1D')(d)

# E

e = Conv2D(16, 11, padding='valid', activation='relu', name='Conv1E')(i)

e = MaxPool2D(pool_size=pool_size, name='Pooling1E')(e)

e = Conv2D(32, 11, padding='valid', activation='relu', name='Conv2E')(e)

e = Dropout(0.1)(e)

e = MaxPool2D(pool_size=pool_size, name='Pooling2E')(e)

# F

f = Conv2D(16, 11, padding='valid', activation='relu', name='Conv1F')(i)

f = MaxPool2D(pool_size=pool_size, name='Pooling1F')(f)

f = Conv2D(32, 11, padding='valid', activation='relu', name='Conv2F')(f)

f = Dropout(0.1)(f)

f = MaxPool2D(pool_size=pool_size, name='Pooling2F')(f)

f = Conv2D(64, 11, padding='valid', activation='relu', name='Conv3F')(f)

f = Dropout(0.1)(f)

f = MaxPool2D(pool_size=pool_size, name='Pooling3F')(f)

# Reverse

# F

f = UpSampling2D(size=pool_size, name='UpSampling1F')(f)

f = Deconv2D(64, 11, padding='valid', activation='relu', name='Deconv1F')(f)

f = Dropout(0.1)(f)

f = UpSampling2D(size=pool_size, name='UpSampling2F')(f)

f = Deconv2D(32, 11, padding='valid', activation='relu', name='Deconv2F')(f)

f = Dropout(0.1)(f)

f = UpSampling2D(size=pool_size, name='UpSampling3F')(f)

f = Deconv2D(16, 11, padding='valid', activation='relu', name='Deconv3F')(f)

# E

e = UpSampling2D(size=pool_size, name='UpSampling1E')(e)

e = Deconv2D(32, 11, padding='valid', activation='relu', name='Deconv1E')(e)

e = Dropout(0.1)(e)

e = UpSampling2D(size=pool_size, name='UpSampling2E')(e)

e = Deconv2D(16, 11, padding='valid', activation='relu', name='Deconv2E')(e)

# D

d = UpSampling2D(size=pool_size, name='UpSampling1D')(d)

d = Deconv2D(16, 11, padding='valid', activation='relu', name='Deconv1D')(d)

d = Dropout(0.1)(d)

# C

c = UpSampling2D(size=pool_size, name='UpSampling1C')(c)

c = Deconv2D(64, 3, padding='valid', activation='relu', name='Deconv1C')(c)

c = Dropout(0.1)(c)

c = UpSampling2D(size=pool_size, name='UpSampling2C')(c)

c = Deconv2D(32, 3, padding='valid', activation='relu', name='Deconv2C')(c)

c = Dropout(0.1)(c)

c = UpSampling2D(size=pool_size, name='UpSampling3C')(c)

c = Deconv2D(16, 3, padding='valid', activation='relu', name='Deconv3C')(c)

# B

b = UpSampling2D(size=pool_size, name='UpSampling1B')(b)

b = Deconv2D(32, 3, padding='valid', activation='relu', name='Deconv1B')(b)

b = Dropout(0.1)(b)

b = UpSampling2D(size=pool_size, name='UpSampling2B')(b)

b = Deconv2D(16, 3, padding='valid', activation='relu', name='Deconv2B')(b)

# A

a = UpSampling2D(size=pool_size, name='UpSampling1A')(a)

a = Deconv2D(16, 3, padding='valid', activation='relu', name='Deconv1A')(a)

a = Dropout(0.1)(a)

j = Concatenate(axis=3)([a, b, c, d, e, f])

j = Deconv2D(1, 3, padding='valid', activation='relu', name='Deconv0')(j)

# Model

model = Model(inputs=u, outputs=j)

### End of network ###
model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])
model.summary()

model.save('model_c.json')
