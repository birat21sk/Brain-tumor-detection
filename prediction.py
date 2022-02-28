import tensorflow as tf

pred_model = tf.keras.models.load_model("./model/BrainTumorModel-10FoldValidation.h5")
def predict_tumor(image):
    result = pred_model.predict(image)
    return result