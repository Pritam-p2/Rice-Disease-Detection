import tensorflow
import keras
from PIL import Image,ImageOps
import numpy as np


bacterial=0
brown=0
leaf=0

#Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model =keras.models.load_model('models\keras_model.h5')

#create the array of the right shape to feed into the keras model
#the 'length' or number of images you can put into the array is
#determined by the firs position in the shape tuple
data=np.ndarray(shape=(1, 224, 224,3),dtype=np.float32)

def predict():
    # replace this with the path to your image
    image = Image.open('static/images/test_image.jpg')
    
    #resize the image to a 224X224 with the same strategy as in Teachable machine
    #resizing the image to be at least 224X224 and then cropping from the center
    size=(224,224)
    image=ImageOps.fit(image,size,Image.ANTIALIAS)
    image_array=np.asarray(image)
    normalized_image_array=(image_array.astype(np.float32)/127.0)-1
    data[0]=normalized_image_array
    #run the inference
    prediction=model.predict(data)
    idx=np.argmax(prediction)
    
    if idx==0:
        global bacterial
        return "Bacterial Leaf Blight"
    elif idx==1:
        global brown
        return "Brown Spot"
    else:
        global leaf
        return "Leaf Smut"
    

