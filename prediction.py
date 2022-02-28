import tensorflow as tf

pred_model = tf.keras.models.load_model("./model/TumorModel10Epochs.h5")
def predict_tumor(image):
    result = pred_model.predict(image)
    return result