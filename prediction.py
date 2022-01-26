from keras.models import load_model

pred_model = load_model("./model/TumorModel10Epochs.h5")

def predict_tumor(image):
    # result = pred_model.predict(image)
    result = (pred_model.predict(image) > 0.5).astype("int32")
    return result