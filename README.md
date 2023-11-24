# clean-ocr
Open image -> draw over zone of interest (drag&drop) -> get text.

Sometimes you just don't need to scan the whole image. </br>
And cut it into another file is a bit annoying. </br>
So use this script. </br>

## Usage
1 - Download the whole project </br>
2 - Open the terminal at the project's folder </br>
run ```pip install -r requirements.txt``` </br>

run ```python clean-ocr.py $path_to_your_image_here``` </br>

After your image is loaded, drag and drop forming as many rectangles as you like, selecting the zones of interest </br>

And just press enter!

ESCAPE KEY &nbsp; &nbsp; &nbsp; &nbsp;-> close </br>
ENTER KEY &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-> get text from selected area </br>
BACKSPACE KEY  &nbsp; -> start again</br>

# Uses Tesseract OCR 
Project: https://github.com/tesseract-ocr/tesseract </br>
Windows installer: https://github.com/UB-Mannheim/tesseract/wiki </br>
Other installation methods: https://tesseract-ocr.github.io/tessdoc/Installation.html </br>

