import tensorflow as tf

model = tf.keras.models.load_model("keras_model.h5", compile=False)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # smaller & faster
tflite_model = converter.convert()

with open("fruit_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Done! fruit_model.tflite created.")