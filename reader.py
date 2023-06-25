''' 
    COMP 4102 Final Project - QR Code Reader
    Wenwen Chen
    100882644
'''

# Libraries
import cv2, os, random
import numpy as np

# color(blue, green, red)
green = (36,255,12)
blue  = (255, 184, 77)

# initialize cv2 detector
detector = cv2.QRCodeDetector()

'''
    QRCode Detecting

    Referrence: https://stackoverflow.com/questions/60359398/python-detect-a-qr-code-from-an-image-and-crop-using-opencv
'''
def detect(image, name):
    kernel_size = (5,5)

    draw = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, kernel_size, 0)

    # Otsu's threshold
    # transforms a grayscale image to a binary image
    # only consist of two peaks(0 and 255) to enhance contrast and reduce noise. 
    # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

    # Morph close 
    # for closing small holes inside the foreground objects
    # or small black points on the object.
    # https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    morph_close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, morph_kernel, iterations=2)

    # Find contours on code
    # https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
    contours, hierarchy = cv2.findContours(morph_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initial corner array and index
    corners = np.zeros((3,3))
    i = 0

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)

        # filter for Squares
        # len(approx) == 4 if the detected polygon is produced by 4 edges, it's a rectangle
        # area > 1000 filter out the small size rectangles since we are looking for the largest
        # 0.85 < ar < 1.3 given a range of the proportion of h and w to make sure it is a square
        if len(approx) == 4 and area > 1000 and 0.85 < ar < 1.3 and i < 3:
            corners[i] = [x,y,x+y]

            # draw QR rectangles in GREEN
            cv2.rectangle(draw, (x, y), (x + w, y + h), green, 3)
            square = image[y:y+h, x:x+w]

            # implementing index
            i = i + 1

    if i < 2:
        return False
    else:
        corners = corners[corners[:, 2].argsort()]

        # Square error reduction
        if corners[0][0] <= corners[1][0]:
            corners[1][0] = corners[0][0]
        else:
            corners[0][0] = corners[1][0]

        if corners[0][1] <= corners[2][1]:
            corners[2][1] = corners[0][1]
        else:
            corners[0][1] = corners[2][1]

        # image corner
        code_corners = np.zeros((1,4,2))
        code_corners[0][0] = [corners[0][0], corners[0][1]]
        code_corners[0][1] = [corners[2][0]+w, corners[0][1]]
        code_corners[0][2] = [corners[2][0]+w, corners[1][1]+h]
        code_corners[0][3] = [corners[0][0], corners[1][1]+h]

        # draw corners on image in BLUE
        for i in range(code_corners[0].shape[0]):
            x = int(code_corners[0][i][0])
            y = int(code_corners[0][i][1])
            cv2.circle(draw, (y,x), 5, blue, cv2.FILLED)

        # show image with green squares and blue cornors
        file_name = 'drawn image: ' + name
        cv2.imshow(file_name, draw)

        return code_corners

'''
    QRCode Decoding

    Referrence: https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html#a64373f7d877d27473f64fe04bb57d22b
'''
def decode(image, corners):
    # decode by cv2 detector
    info, binary_code = detector.decode(image, corners)
    return info


'''
    QRCode Dectect and Decode
'''
def detectAndDecode(image, name):
    corners = detect(image, name)

    if type(corners) == type(False):
        return "No QRCode detected."
    else:
        return decode(image, corners)


'''
    Testing by Dataset
'''
# pick random number of test files
# https://numpy.org/doc/1.13/reference/generated/numpy.random.randint.html
n = random.randint(10, 15)

for i in range(n):
    # pick random file from folder
    # https://www.codegrepper.com/code-examples/python/random+pick+any+file+from+directory+python
    image_name = random.choice(os.listdir("./qr_dataset//"))
    image_path = "./qr_dataset/" + image_name

    print("======== REDAING FILE : " + image_name + " ========")
    image = cv2.imread(image_path)

    # detect and decode by cv2
    cvData, cvCorners, cvBinaryCode = detector.detectAndDecode(image)
    print("data get by cv2        : " + str(cvData))

    # detect and decode by self method
    data = detectAndDecode(image, image_name)
    print("data get by self method: " + str(data))

    if cvData == data:
        print("+++ SUCCESS +++")
    else:
        print("--- ERROR ---")

print("\n Finished running " + str(n) + " test cases")

# distry image
cv2.waitKey(0)
cv2.destroyAllWindows()
