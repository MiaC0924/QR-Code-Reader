# QR-Code-Reader

The project uses cv2 version: 4.5.5.62, random, os and numpy

Code:
reader.py		 
This is the project Python code document
By running this project code in terminal with “Python reader.py” or “Python3 reader.py”, the project will be excited with some test cases.

Paper:
Project Report.pdf		 
This is the report paper which includes the introduction of the project and the result analysis

Example input:
- in folder './qr_dataset'
- This folder contains some 40 qr code images which are provided by https://www.kaggle.com/coledie/qr-codes
- If you want to have more test cases, you could download the whole dataset from the above link and make sure that all QRCode images are saved in folder "./qr_dataset"

Example output:
- in folder './result'
- This folder contains the testing result images. All images are discussed in the Project Report and listed as below.
		 - '7209-v4 original.png'    - the orginal 7209-v4 qr code
		 - '7209-v4 blur.jpg'        - 7209-v4 qr code after gaussian blur
		 - '7209-v4 thresh.jpg'      - 7209-v4 qr code after Otsu's threshold
		 - '7209-v4 morph_close.jpg' - 7209-v4 qr code after Morph Close
		 - '7209-v4 contours.jpg'    - 7209-v4 qr code contours
		 - '7209-v4 result.jpg'      - 7209-v4 qr code detecting result

		 - 'message - case 0 both success.png'  - output example when all test cases success
		 - 'message - case 1 cv2 fail.png'      - output example when cv2 detector fails
		 - 'message - case 2 project fail.png'  - output example when project detector fails
