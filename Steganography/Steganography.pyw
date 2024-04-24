# Steganography
# fr0g1299


import re  # removes extra spaces
import sys  # exit
import os  # for .ui path
import cv2  # image read/write
import numpy as np  # modify pixel arrays of images

from PyQt5 import QtCore
from PyQt5.QtCore import QSequentialAnimationGroup, QEvent
from PyQt5.QtGui import QIcon, QColor, QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

chars = {'ě' : 'e', 'Ě' : 'E', 'š' : 's', 'Š' : 'S', 'č' : 'c',
            'Č' : 'C', 'ř' : 'r', 'Ř' : 'R', 'ž' : 'z', 'Ž' : 'Z'}

IMAGE = ''

FNAME = ''

NEWIMG = ''

# StyleSheet for Message boxes
msg_box_css = ("QPushButton {\n"
            "background-color: rgb(150, 0, 0);\n"
            "border: none;\n"
            "padding-top: 10px;\n"
            "padding-bottom: 10px;\n"
            "padding-right: 10px;\n"
            "padding-left: 10px;\n"
            "color: rgb(206, 214, 196);\n"
            "border-left: 2px solid rgb(130, 0, 0);\n"
            "border-right: 1px solid rgb(130, 0, 0);\n"
            "border-bottom: 2px solid rgb(130, 0, 0);\n"
            "border-radius: 10px;}\n"
            "QMessageBox {\n"
            "background-color: rgb(28, 29, 36);\n"
            "border: 1px solid rgb(55, 55, 60);\n"
            "border-bottom-left-radius: 5px;\n"
            "border-bottom-right-radius: 5px;}\n"
            "QMessageBox QLabel{\n"
            "color: white;}\n")


class SteganographyGui(QDialog):

    def __init__(self):
        # Necessary stuff
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        form_class = os.path.join(ui_path, "SteganographyGui.ui")
        loadUi(form_class, self)
        self.setWindowTitle("Steganography")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedHeight(928)
        self.setFixedWidth(1560)

        self.fadeQuick(self.lbl_dec_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_enc_save)  # Quickly fades, so the animation works later

        self.OTInput.installEventFilter(self)  # Makes Enter usable
        self.OTInput.setTabChangesFocus(True)  # Makes Tab usable

        self.btn_enc.clicked.connect(self.goToEncrypt)  # Encrypt Button
        self.btn_enc_res.clicked.connect(lambda: self.reset(1))  # Resets Encrypt

        self.btn_img.clicked.connect(self.getfile)  # Browse Image Button
        self.btn_img_res.clicked.connect(lambda: self.reset(3))  # Resets Images
        self.btn_save.clicked.connect(self.saveFile)  # Save Button

        self.btn_dec.clicked.connect(self.goToDecrypt)  # Decrypt Button
        self.btn_dec_res.clicked.connect(lambda: self.reset(2))  # Resets Decrypt
        self.btn_dec_cp.clicked.connect(self.copyToClipboard)  # Copy Decrypt result Button
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Removes Default Window Frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes QDialog translucent

        self.btn_min.clicked.connect(self.minimizeWindow)  # Enables minimize Button
        self.btn_cls.clicked.connect(lambda: app.exit())  # Enables close Button
        self.title_bar.mouseMoveEvent = self.moveWindow  # Enables Click&Drag on the window

        # Shadow on the frameless window
        shadow_window = QGraphicsDropShadowEffect()
        shadow_window.setBlurRadius(5)
        shadow_window.setOffset(3)
        shadow_window.setColor(QColor(50, 50, 50, 160))
        self.bgwidget.setGraphicsEffect(shadow_window)

    def copyToClipboard(self):
        if self.lbl_dec_res.toPlainText() != '':
            cb = QApplication.clipboard()
            cb.setText(self.lbl_dec_res.toPlainText(), mode=cb.Clipboard)
            self.fade(self.lbl_dec_cp)
        else: return 0

    def minimizeWindow(self):
        '''Enables minimize button.'''
        self.showMinimized()

    def moveWindow(self, event):
        '''Calculates Click&Drag.'''
        if self.isMaximized() == False:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
            pass

    def mousePressEvent(self, event):
        '''Get global position for Click&Drag.'''
        self.clickPosition = event.globalPos()
        pass

    def eventFilter(self, obj, event):
        '''Remaps Enter button for Enc, Dec and Key inputs.'''
        if (obj is self.OTInput) and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if obj is self.OTInput:
                    self.goToEncrypt()
                    return True

        return super().eventFilter(obj, event)

    def getfile(self):
        path = os.path.dirname(os.path.abspath(__file__))
        fname = QFileDialog.getOpenFileName(self, 'Open file', str(path), self.tr('Image files (*.png *.jpg *.jpeg *.bmp *tif *tiff);;'
                                                                                  'PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)'))

        if fname[0] == '':
             return 0
        pixmap_scale = QPixmap(fname[0])

        global IMAGE
        global FNAME
        IMAGE = cv2.imdecode(np.fromfile(fname[0], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        IMAGE = IMAGE[:,:,:3]
        FNAME = fname[0]

        self.img_in.setPixmap(pixmap_scale.scaled(725, 650, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.img_out.clear()

        h, w, _ = IMAGE.shape
        p = fname[0]
        s = human_size(os.stat(fname[0]).st_size)
        pix = h * w
        pix_f = format(pix, ',d').replace(',',' ')
        m = format(pix * 3 // 8 - 6, ',d').replace(',',' ')
        
        self.lbl_res.setText(f'Resolution: {w}x{h}')
        self.lbl_pix.setText(f'Pixels: {pix_f} px')
        self.lbl_max.setText(f'Max Length of Message: {m}')
        self.lbl_loc.setText(f'File: {p}')
        self.lbl_siz.setText(f'Size: {s}')
    
    def whereToSave(self):
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save file', str(path), self.tr('Image files (*.png *.bmp *tif *tiff);;'
                                                                                  'PNG (*.png);;BMP (*.bmp);;TIFF (*.tif *.tiff)'))
            return fname
        except:
            return 0
        
    def saveFile(self):
        try:
            newimg = NEWIMG
            new_img_name = newimg.copy()
            new_img_name = self.whereToSave()
            cv2.imwrite(str(new_img_name[0]), newimg)
            self.fade(self.lbl_enc_save)
        except:
            return 0

    def goToEncrypt(self):
        try:
            enc = self.OTInput.toPlainText()
            if enc == '':
                self.showInformationMessageBox()
                return 0
        
            enc = preparation(enc)

            fname = FNAME
            if fname == '':
                 self.showCriticalMessageBox()
                 return 0
            image = IMAGE

            l = format(len(enc), ',d').replace(',',' ')
            h, w, _ = image.shape
            pix = h * w

            self.lbl_len.setText(f'Length of the Message: {l}')

            if len(enc) + 6 > pix * 3 // 8:
                  self.showInformationMessageBox(2)
                  return 0

            newimg = image.copy()
            newimg, l = encrypt(newimg, enc)

            l = format(l, ',d').replace(',',' ')
            self.lbl_len.setText(f'Length of the Message: {l}')

            pixmap_scale = QPixmap(QImage(newimg.data, w, h, 3 * w, QImage.Format_RGB888).rgbSwapped())
            self.img_out.setPixmap(pixmap_scale.scaled(725, 650, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

            global NEWIMG
            NEWIMG = newimg
        except:
            self.showCriticalMessageBox()

    def goToDecrypt(self):
        try:
            self.img_out.clear()
            fname = FNAME
            if fname[0] == '':
                 self.showCriticalMessageBox()
                 return 0

            image = IMAGE
            dec = ''
            bin_str = '' 

            br = False

            for row in image:
                if br:
                    break
                for pixel in row:
                    if br:
                        break
                    pixels = [value % 2 for value in pixel[:3]]
                    bin_str += ''.join(map(str, pixels))

                    while len(bin_str) >= 8:
                        dec += chr(int(bin_str[:8], 2))
                        bin_str = bin_str[8:]
                        if dec[-6:] == 'XQVQCX':
                            br = True
                            break

            l = format(len(dec[:-6]), ',d').replace(',',' ')
            self.lbl_len.setText(f'Length of the Message: {l}')
            self.lbl_dec_res.setText(''.join(dec[:-6]))
        except:
            self.showCriticalMessageBox()

    def showCriticalMessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)
        
        msg.setWindowTitle("Error")
        msg.setWindowIcon(QIcon('icon.png'))
        msg.setText("You need to pick an image first by using the \'Browse image\' button.\n"
                    " Or There is no message in the picture...")
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInformationMessageBox(self, chk=1):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)
        
        msg.setWindowTitle("Information")
        msg.setWindowIcon(QIcon('icon.png'))
        match chk:
            case 1:
                msg.setText("Nothing was inserted...")
                msg.setStandardButtons(QMessageBox.Ok)
            case 2:
                msg.setText("You've inserted too much characters, see \'Max Length of Message\'...")
                msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def reset(self, chk: int):
        '''
        Empties encryption input, if chk = 1.
        Empties decryption result, if chk = 2.
        Empties Images and labels, if chk = 3.
        '''
        match chk:
            case 1:
                self.OTInput.clear()
            case 2:
                self.lbl_dec_res.clear()
            case 3:
                self.img_in.clear()
                self.img_out.clear()

                global NEWIMG
                global IMAGE
                NEWIMG = ''
                IMAGE = ''

                self.lbl_res.setText(f'Resolution: ')
                self.lbl_pix.setText(f'Pixels: ')
                self.lbl_max.setText(f'Max Length of Message: ')
                self.lbl_len.setText(f'Length of the Message: ')
                self.lbl_loc.setText(f'File: ')
                self.lbl_siz.setText(f'Size: ')

    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.anim = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setDuration(550)

        self.anim_2 = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.anim_2.setStartValue(1)
        self.anim_2.setEndValue(0)
        self.anim_2.setDuration(2000)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addPause(2000)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.start()

    def fadeQuick(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(0)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


def human_size(num: int) -> str:
    '''Stolen, I can't care.'''
    base = 1
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        n = num / base
        if n < 9.95 and unit != 'B':
            # Less than 10 then keep 2 decimal places
            value = "{:.2f} {}".format(n, unit)
            return value
        if round(n) < 1000:
            # Less than 4 digits so use this
            value = "{} {}".format(round(n), unit)
            return value
        base *= 1024
    value = "{} {}".format(round(n), unit)

    return value


def preparation(txt):
    '''
    Removes repeating spaces.
    Substitutes ['ěščřž'], so decryption doesn't put blank spaces.
    '''
    prep_str = txt.strip()
    prep_str = ''.join(chars[letter] if letter in chars else letter for letter in prep_str).strip()
    prep_str = re.sub(r'\s+', ' ', prep_str, flags=re.UNICODE)

    return prep_str


def generateData(txt):
    '''Convert data into 8-bit binary using ASCII values.'''
    if type(txt) == str:
        binary_data = ''
        for char in txt:
            ascii_value = ord(char)
            # Skip characters with ASCII values greater than 255
            if ascii_value <= 255:
                binary_data += format(ascii_value, "08b")
        return binary_data
    elif type(txt) == np.ndarray:
        return [format(i, "08b") for i in txt]
    

def encrypt(image, msg):
    msg += 'XQVQCX'
    msg_index = 0
    bin_msg = generateData(msg)
    msg_len = len(bin_msg)
    br = False
    
    for row in image:
        if br:
            break
        for pixel in row:
            r, g, b = generateData(pixel)
            if msg_index < msg_len:
                pixel[0] = int(r[:-1] + bin_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                pixel[1] = int(g[:-1] + bin_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                pixel[2] = int(b[:-1] + bin_msg[msg_index], 2)
                msg_index += 1
            if msg_index >= msg_len:
                br = True
                break
    return image, int(msg_len / 8 - 6)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = SteganographyGui()
    gui.show()

    try:
        sys.exit(app.exec())
    except:
        print("Successfully Exited")
