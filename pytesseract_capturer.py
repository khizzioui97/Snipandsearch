import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2
import pytesseract
import time 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import bs4 as bs
import urllib.request



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        # img.save('capture.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)          
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                        cv2.CHAIN_APPROX_NONE)         
        im2 = img.copy()
        for cnt in contours: 
            x, y, w, h = cv2.boundingRect(cnt)     

            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)     

            cropped = im2[y:y + h, x:x + w]            
            global text
            text = str(pytesseract.image_to_string(cropped)) 
            

        


        message = text.strip()

        url = ('https://html.duckduckgo.com/html?q='+message)

        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        a = soup.body.b
        print(a)
        global abc
        
        abc=""
        for i in soup.find_all('a', class_='result__snippet'):
    
            # print(i.get_text(separator=' - ', strip=True))
            abc += (i.get_text(separator=' - ', strip=True))
            
        global abc_clean
        abc_clean = ""
        char_list = [abc[j] for j in range(len(abc)) if ord(abc[j]) in range(65536)]
        for j in char_list:
            abc_clean+=j
                    

        def show(root):
            root.update()
            root.deiconify()

        def hide(root):
            root.withdraw()
            
        root = tk.Tk()
        hide(root)
        
        S = tk.Scrollbar(root)
        T = tk.Text(root, height=4, width=50)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        T.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(tk.END, abc_clean)
        show(root)
        tk.mainloop()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

