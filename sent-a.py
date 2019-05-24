import numpy as np
import json
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

def convert_text_to_index_array(text):
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)]

# Prepare our data
training_data = np.genfromtxt('s-a-d.csv', delimiter=',', skip_header=1, usecols=(1,3), dtype=None)
train_x = [x[1] for x in training_data]
train_y = np.asarray([x[0] for x in training_data])

# max_words is the maximum number of words that will be taken into account, dictionary is where we will be storing them
max_words = 1000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_x)
dictionary = tokenizer.word_index

# write out dictionary for later use
with open('dictionary.json', 'w') as dict_file:
    json.dump(dictionary, dict_file)

print('Converting text to index array...')

# Create list of word indices
allWordIndices = []

for data in train_x:
    wordIndices = convert_text_to_index_array(data)
    allWordIndices.append(wordIndices)

# Remove those variables which are no longer needed
print('Wrote dictionary.json, removing variable...')
del dictionary
del training_data

# Create numpy array
allWordIndices = np.asarray(allWordIndices)

# Prepare data for training (train_x is our data, train_y is our labels) 
train_x = tokenizer.sequences_to_matrix(allWordIndices, mode='binary')
train_y = keras.utils.to_categorical(train_y, 2)

# Create our model
model = Sequential()
model.add(Dense(512, input_shape=(max_words,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train for 5 epochs, keep 10% of data back for validation
model.fit(train_x, train_y, batch_size=32, epochs=5, verbose=1, validation_split=0.1, shuffle=True)

# Save the model for later use
model_json = model.to_json()

with open('sentiment-model.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights('sentiment-model.h5')

