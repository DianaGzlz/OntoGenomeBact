#IMPORT
import tensorflow as tf



############### CNN A ###############
#define model
batch_size = 3000
num_classes = 4206
epochs = 5
input_shape = (4, 13, 1)
lot_ar = 'CNNA-3'

#model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(100, (5,5), padding='same', activation='relu', input_shape=input_shape),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

#compilacion
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])


############### CNN B ###############
#define model
batch_size = 3000
num_classes = 4206
epochs = 5
input_shape = (4, 13, 1)
lot_ar = 'CNNB-3'

#Modelo
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(100, (5,5), padding='same', activation='relu', input_shape=input_shape),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(500, (3,3), padding='same', activation='relu'),
    tf.keras.layers.MaxPool2D(strides=(2,2)),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2000, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

#compilacion
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])


############### CNN C ###############
#define model
batch_size = 3000
num_classes = 4206 
epochs = 10
input_shape = (4, 13, 1)
lot_ar = 'CNNC-3'

#model DANQ
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=input_shape),
    tf.keras.layers.Conv2D(100, (5,5), padding='same', activation='relu'),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Reshape((12,100)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(1000)),
    tf.keras.layers.Dense(2000, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
#compilacion
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])


############### CNN D ###############
#define model
batch_size = 3000
num_classes = 4206 
epochs = 5
input_shape = (4, 13, 1)
lot_ar = 'CNND-3'

#model
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=input_shape),
    tf.keras.layers.ConvLSTM1D(200, 5, padding='same', activation='relu'),
    tf.keras.layers.MaxPool1D(),
    tf.keras.layers.Bidirectional(tf.keras.layers.GRU(1000)),
    tf.keras.layers.Dense(2000, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

#compilacion
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.AUC()])


############### RNN A ###############
#define model
batch_size = 3000
num_classes = 4206
epochs = 5
input_shape = (1, 52)
lot_ar = 'RNN1-1'

#model
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(100, input_shape=(input_shape), return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(1000),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2000, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation = 'softmax')
])

#compilacion
model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=[tf.keras.metrics.AUC()])
