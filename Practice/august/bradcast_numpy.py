import numpy as np

A= np.array([[1,2,3,4],
             [5,6,7,8],
             [9,10,11,12]])

b = np.array([10,20,30,40])

c = A + b


json_data = {"type": "FeatureCollection",
             "features": "test"}

models.objects.filter(json_data__type = "CustomFeatureCollection")