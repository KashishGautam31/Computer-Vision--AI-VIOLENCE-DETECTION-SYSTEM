from tensorflow.keras.models import load_model

model = load_model("model/violence_model.h5")

def predict_violence(frame):
    
    prediction = model.predict(frame)

    if prediction > 0.5:
        return "Violence"

    return "Non-Violence"