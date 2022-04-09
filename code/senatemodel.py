from sklearn import datasets, linear_model
import numpy as np

def dotproduct(a,b):
    product = 0
    try:
        for i in range(len(a)):
            product += a[i]*b[i]
        return product
    except:
        print("Unable to take dotproduct - check if the lists are all numbers or of equal length. Using simple mean instead")
        return 0


xs = []

xs.append([38.55,29.82,8.73,4.96])
xs.append([35.9,31.1,10.62,2.85])
xs.append([38.9,22.6,9.9,10.3])
xs.append([40.9,27.6,11.8,5.9])
xs.append([37.8,30.4,10.9,4.9])

xs = np.array(xs)

ys = []

ys.append([3,2,1,0])
ys.append([3,2,1,0])
ys.append([3,1,1,1])
ys.append([3,2,1,0])
ys.append([3,2,1,0])

ys = np.array(ys)


model =  linear_model.LinearRegression().fit(xs, ys)



print(model.predict(np.array([[38.1,41.7,9.9,2.2]])))