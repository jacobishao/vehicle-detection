from detect import *

if USE_SAMPLE == True:
    cars = cars[0:SAMPLE_SIZE]
    notcars = notcars[0:SAMPLE_SIZE]

car_features = extract_features(cars, COLOR_SPACE, ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, HOG_CHANNEL)
notcar_features = extract_features(notcars, COLOR_SPACE, ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, HOG_CHANNEL)

X = np.vstack((car_features, notcar_features)).astype(np.float64)
X_scaler = StandardScaler().fit(X)
scaled_X = X_scaler.transform(X)

y = np.hstack((np.ones(len(car_features)), np.zeros(len(notcar_features))))

rand_state = np.random.randint(0, 100)
X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, test_size = 0.2, random_state = rand_state)

print('Using spatial binning of:', SPATIAL,
    'and', NBINS,'histogram bins with', ORIENT,
    'orientations', PIX_PER_CELL, 'pixels per cell and',
    CELL_PER_BLOCK, 'cells per block')
print('Feature vector length:', len(X_train[0]))
# Parameter Tuning
parameters = {'dual':(True, False), 'C':[0.1, 1.0, 10]}
# Use a linear SVC
svc = LinearSVC()
# Run Grid Search
clf = GridSearchCV(svc, parameters)
# Check the training time for the SVC
t=time.time()
clf.fit(X_train, y_train)
t2 = time.time()
print(round(t2-t, 2), 'Seconds to train SVC...')
# Check the score of the SVC
print('Test Accuracy of SVC = ', round(clf.score(X_test, y_test), 4))
# Check the prediction time for a single sample
t=time.time()
n_predict = 10
print('My SVC predicts: ', clf.predict(X_test[0:n_predict]))
print('For these',n_predict, 'labels: ', y_test[0:n_predict])
t2 = time.time()
print(round(t2-t, 5), 'Seconds to predict', n_predict,'labels with SVC')

image = mpimg.imread('test_images/test1.jpg')

ystart = 350
ystop = None
scale = 1.5

out_img = find_cars(image, ystart, ystop, scale, clf, X_scaler)

plt.imshow(out_img)
plt.show()

# ind = np.random.randint(0, len(cars))
#
# image = mpimg.imread(notcars[ind])
# hls_img = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
#
# features, hog_image_h_channel = get_hog_features(hls_img[:,:,0], ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, VIS_HOG, False)
# features, hog_image_l_channel = get_hog_features(hls_img[:,:,1], ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, VIS_HOG, False)
# features, hog_image_s_channel = get_hog_features(hls_img[:,:,2], ORIENT, PIX_PER_CELL, CELL_PER_BLOCK, VIS_HOG, False)

# fig, ax = plt.subplots(nrows = 1, ncols = 4)
# plt.rc('font', size = 5)
# fig.tight_layout()
# plt.subplot(1, 4, 1)
# plt.imshow(image, cmap = 'gray')
# plt.title('Original')
# plt.subplot(1, 4, 2)
# plt.imshow(hog_image_h_channel, cmap = 'gray')
# plt.title('H-Channel HOG Visualization')
# plt.subplot(1, 4, 3)
# plt.imshow(hog_image_l_channel, cmap = 'gray')
# plt.title('L-Channel HOG Visualization')
# plt.subplot(1, 4, 4)
# plt.imshow(hog_image_s_channel, cmap = 'gray')
# plt.title('S-Channel HOG Visualization')
# plt.show()