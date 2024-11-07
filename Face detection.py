import cv2

# Load the Haar Cascade Classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Attempt to read the image
img = cv2.imread('1920_stock-photo-mosaic-of-satisfied-people-157248584.jpg')  # Update this path as necessary

# Check if the image loaded successfully
if img is None:
    print("Error: Could not load image. Please check the file path.")
    exit()  # Exit the script if the image is not loaded

# Convert the image to grayscale
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    area = w * h
    print(area)



# Display the resulting image
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()  # Close all OpenCV windows after a key press
