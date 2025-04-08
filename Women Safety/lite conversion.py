import tensorflow as tf
from tensorflow.keras import backend as K

# Define focal loss function for handling class imbalance during training
def focal_loss(gamma=2., alpha=.25):
    """
    Creates a focal loss function.

    Parameters:
    - gamma (float): Focusing parameter to reduce the relative loss for well-classified examples.
    - alpha (float): Balancing factor to address class imbalance.

    Returns:
    - focal_loss_fixed: A function to be used as a custom loss in Keras models.
    """
    def focal_loss_fixed(y_true, y_pred):
        epsilon = K.epsilon()  # Small constant to avoid log(0)
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)  # Ensure predictions are in (0,1)
        pt = tf.where(K.equal(y_true, 1), y_pred, 1 - y_pred)  # Get pt for each class
        loss = -alpha * K.pow(1. - pt, gamma) * K.log(pt)  # Focal loss formula
        return K.mean(loss)  # Return average loss

    return focal_loss_fixed

# Load the pre-trained Keras model with custom focal loss
model = tf.keras.models.load_model(
    "speech_distress_model.h5",
    custom_objects={'focal_loss_fixed': focal_loss()}
)

print("Model loaded successfully.")

# Initialize the TFLite converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Enable advanced features for TFLite conversion
converter.experimental_enable_resource_variables = True
converter._experimental_lower_tensor_list_ops = False  # Prevent lowering tensor list ops (used for complex models)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,     # Enable standard TFLite ops
    tf.lite.OpsSet.SELECT_TF_OPS        # Allow some TensorFlow ops for compatibility
]

# Apply default optimization for performance/size improvement
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert the model to TFLite format
tflite_model = converter.convert()

# Save the converted TFLite model to a file
with open("speech_distress_model.tflite", "wb") as f:
    f.write(tflite_model)

print("TFLite model saved as 'speech_distress_model.tflite'")
