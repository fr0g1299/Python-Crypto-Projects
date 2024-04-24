# Playfair Cipher
# fr0g1299


import re  # removes extra spaces
import sys  # exit
import unicodedata  # removes diacritics
import os  # for .ui path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSequentialAnimationGroup, QEvent
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = {'ZEERO' : '0', 'ONNE' : '1', 'TVVO' : '2', 'THHREE' : '3', 'FOOUR' : '4',
            'FIIVE' : '5', 'SIIX' : '6', 'SEEVEN' : '7', 'EIIGHT' : '8', 'NIINE' : '9'}

numbers_contrary = dict((v, k) for (k, v) in numbers.items())

# StyleSheet for Message boxes
msg_box_css = ("QPushButton {\n"
        "    background-color: rgb(150, 0, 0);\n"
        "    border: none;\n"
        "    padding-top: 10px;\n"
        "    padding-bottom: 10px;\n"
        "    padding-right: 10px;\n"
        "    padding-left: 10px;\n"
        "    color: rgb(206, 214, 196);\n"
        "    border-left: 2px solid rgb(130, 0, 0);\n"
        "    border-right: 1px solid rgb(130, 0, 0);\n"
        "    border-bottom: 2px solid rgb(130, 0, 0);\n"
        "    border-radius: 10px;}\n"
        "    QMessageBox {\n"
        "    background-color: rgb(28, 29, 36);\n"
        "    border: 1px solid rgb(55, 55, 60);\n"
        "    border-bottom-left-radius: 5px;\n"
        "    border-bottom-right-radius: 5px;}\n"
        "    QMessageBox QLabel{\n"
        "    color: white;}\n")


class PlayfairCipherGui(QDialog):

    def __init__(self):
        # Necessary stuff
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        form_class = os.path.join(ui_path, "PlayfairCipherGui.ui")
        loadUi(form_class, self)
        self.setWindowTitle("Playfair Cipher")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedHeight(708)
        self.setFixedWidth(1010)

        self.fadeQuick(self.lbl_enc_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_dec_cp)  # Quickly fades, so the animation works later
        self.CTInput.installEventFilter(self)  # Makes Enter usable
        self.OTInput.installEventFilter(self)  # Makes Enter usable
        self.key_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.CTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.OTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.key_input.setTabChangesFocus(True)  # Makes Tab usable
        self.table_alpha.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Makes it, so Hheader is not draggable
        self.table_alpha.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Makes it, so Vheader is not draggable
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Removes Default Window Frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes QDialog translucent

        self.btn_enc.clicked.connect(self.goToEncrypt)  # Encrypt Button
        self.btn_enc_cp.clicked.connect(self.copyToClipboardEncrypt)  # Copy Encrypt result Button
        self.btn_enc_res.clicked.connect(self.resetEncrypt)  # Resets Encrypt prep and res text

        self.btn_dec.clicked.connect(self.goToDecrypt)  # Decrypt Button
        self.btn_dec_cp.clicked.connect(self.copyToClipboardDecrypt)  # Copy Decrypt result Button
        self.btn_dec_res.clicked.connect(self.resetDecrypt)  # Resets Decrypt prep and res text
 
        self.btn_tab_res.clicked.connect(self.resetTable)  # Resets Table

        self.btn_min.clicked.connect(self.minimizeWindow)  # Enables minimize button
        self.btn_cls.clicked.connect(lambda: app.exit())  # Enables close button
        self.title_bar.mouseMoveEvent = self.moveWindow  # Enables Click&Drag on the window

        # Shadow on the frameless window
        shadow_window = QGraphicsDropShadowEffect()
        shadow_window.setBlurRadius(5)
        shadow_window.setOffset(3)
        shadow_window.setColor(QColor(50, 50, 50, 160))
        self.bgwidget.setGraphicsEffect(shadow_window)

        # Sets flags to the Table cells, so it's editable
        for i in range(5):
            for j in range(5):
                itm = QTableWidgetItem()
                itm.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable)
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))

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
        if (obj is self.CTInput or obj is self.OTInput) and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                if obj is self.CTInput:
                    self.goToDecrypt()
                    return True
                elif obj is self.OTInput:
                    self.goToEncrypt()
                    return True
        elif obj is self.key_input and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                return True
        return super().eventFilter(obj, event)
    
    def create_matr(self, key):
        '''Creates a matrix with whole alphabet and key.'''
        k = 0
        matr = matrix(5, 5, 0)
        for i in range(0,5):
            for j in range(0,5):
                matr[i][j] = key[k]
                k += 1
        return matr

    def resetTable(self):
        '''Empties table.'''
        for i in range(5):
            for j in range(5):
                itm = QTableWidgetItem()
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))

    def get_key(self):
        '''
        Prepares key.
        Removes repeating spaces. Removes special symbols and diacritics.
        Substitutes 'W'(Czech) or 'J'(English), because those are not in the alphabet.
        Fills in the alphabet after the key.
        '''
        res = []
        rd = bool(self.rd_btn_czech.isChecked())  # True, if Czech radio button is checked
        chk = bool(self.checkBox.isChecked())  # True, if CheckBox is checked, inserts key from Table

        if not chk:
            key = self.key_input.toPlainText().upper()
            key = unicodedata.normalize('NFKD', key)\
                    .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
            key = ''.join(letter for letter in key if letter in symbols).strip()
            key = re.sub(r'\s+', ' ', key, flags=re.UNICODE)
            for letter in key:
                if letter == 'W' and rd and 'V' not in res:
                    res.append('V')
                elif letter == 'W' and not rd and 'V' in res:
                    pass
                elif letter == 'J' and not rd and 'I' not in res:
                    res.append('I')
                elif letter == 'J' and not rd and 'I' in res:
                    pass
                elif letter not in res and not letter.isspace():
                    res.append(letter)
            if len(res) < 4:
                return 0

            for i in range(65,91):
                if chr(i) not in res:
                    if i == 87 and rd:
                        pass
                    elif i == 74 and not rd:
                        pass
                    else:
                        res.append(chr(i))
        else:
            key = ''
            tmp = []
            for i in range(5):
                for j in range(5):
                    if self.table_alpha.item(i , j).text() == '':
                        break
                    tmp.extend(self.table_alpha.item(i , j).text().upper())
                    key += tmp[0]
                    tmp = []
                else:
                    continue
                break

            key = unicodedata.normalize('NFKD', key)\
                    .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
            key = ''.join(letter for letter in key if letter in symbols).strip()
            key = re.sub(r'\s+', ' ', key, flags=re.UNICODE)
            for letter in key:
                if letter == 'W' and rd and 'V' not in res:
                    res.append('V')
                elif letter == 'W' and not rd and 'V' in res:
                    pass
                elif letter == 'J' and not rd and 'I' not in res:
                    res.append('I')
                elif letter == 'J' and not rd and 'I' in res:
                    pass
                elif letter not in res and not letter.isspace():
                    res.append(letter)
            if len(res) < 4:
                return 0

            for i in range(65,91):
                if chr(i) not in res:
                    if i == 87 and rd:
                        pass
                    elif i == 74 and not rd:
                        pass
                    else:
                        res.append(chr(i))
        return res, rd
    
    def goToEncrypt(self):
        try:
            emp = bool(self.OTInput.toPlainText() == '')
            key, rd = self.get_key()
            matr = self.create_matr(key)

            if not emp:
                prep = preparation(self.OTInput.toPlainText(), rd)
                # self.lbl_enc_prep.setText(''.join(prep))
                prep2 = list(prep)
                prep3 = ''
                i = 0
                for letter in prep2:
                    if i == 2:
                        prep3 += ' '
                        prep3 += str(letter)
                        i = 1
                    else:
                        prep3 += str(letter)
                        i += 1
                
                self.lbl_enc_prep.setText(''.join(prep3))

                enc = encrypt(prep, matr)
                self.lbl_enc_res.setText(''.join(enc))


                for i in range(5):
                    for j in range(5):
                        itm = QTableWidgetItem(matr[i][j])
                        itm.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))
            else:
                self.showInformationMessageBox()
        except:
            self.showCriticalMessageBox()

    def goToDecrypt(self):
        try:
            emp = bool(self.CTInput.toPlainText() == '')
            key, rd = self.get_key()
            matr = self.create_matr(key)

            if not emp:
                prep = self.CTInput.toPlainText().upper()
                prep = prep.replace(' ', '')
                prep = unicodedata.normalize('NFKD', prep)\
            .encode('ASCII', 'ignore').decode('utf-8', 'ignore')

                # self.lbl_dec_prep.setText(prep)
                prep2 = list(prep)
                prep3 = ''
                i = 0
                for letter in prep2:
                    if i == 2:
                        prep3 += ' '
                        prep3 += str(letter)
                        i = 1
                    else:
                        prep3 += str(letter)
                        i += 1
                
                self.lbl_dec_prep.setText(''.join(prep3))

                dec = decrypt(prep, matr)
                self.lbl_dec_res.setText(''.join(dec))

                for i in range(5):
                    for j in range(5):
                        itm = QTableWidgetItem(matr[i][j])
                        itm.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))
            else:
                self.showInformationMessageBox()
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
        msg.setText("Inserted wrong key, key should be longer or chose a different language...")
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInformationMessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)
        
        msg.setWindowTitle("Information")
        msg.setWindowIcon(QIcon('icon.png'))
        msg.setText("Nothing was inserted...")
       
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def copyToClipboardEncrypt(self):
        if self.lbl_enc_res.toPlainText() != '':
            cb = QApplication.clipboard()
            cb.setText(self.lbl_enc_res.toPlainText(), mode=cb.Clipboard)
            self.fade(self.lbl_enc_cp)
        else: pass

    def copyToClipboardDecrypt(self):
        if self.lbl_dec_res.toPlainText() != '':
            cb = QApplication.clipboard()
            cb.setText(self.lbl_dec_res.toPlainText(), mode=cb.Clipboard)
            self.fade(self.lbl_dec_cp)
        else: pass

    def resetEncrypt(self):
        self.OTInput.clear()
        self.lbl_enc_prep.clear()
        self.lbl_enc_res.clear()

    def resetDecrypt(self):
        self.CTInput.clear()
        self.lbl_dec_prep.clear()
        self.lbl_dec_res.clear()

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


def matrix(x,y,initial):
    return [[initial for i in range(x)] for j in range(y)]
    

def preparation(txt, rd):
    '''
    Removes repeating spaces. Removes special symbols and diacritics.
    Substitutes spaces with 'XQX' symbol for decryption.
    If there are two of the same chars, it appends 'XQZ', later is removed.
    Substitutes 'W'(Czech) or 'J'(English), because those are not in the alphabet.
    '''
    prep_str = txt.strip().upper()
    prep_str = unicodedata.normalize('NFKD', prep_str)\
            .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
    prep_str = ''.join(letter for letter in prep_str if letter in symbols or letter in numbers.values() or letter.isspace()).strip()
    prep_str = re.sub(r'\s+', ' ', prep_str, flags=re.UNICODE)

    prep_str_2 = []

    for letter in prep_str:
        if letter.isspace():
            prep_str_2.extend(['X', 'Q', 'X'])
        elif letter in numbers.values():
            prep_str_2.extend(numbers_contrary[letter])
        elif letter == 'W' and rd:
            prep_str_2.append('V')
        elif letter == 'J' and not rd:
            prep_str_2.append('I')
        else:
            prep_str_2.append(letter)

    preparation_output = []
    for i in range(0, len(prep_str_2) + 1, 2):
        if i < len(prep_str_2) - 1:
            if prep_str_2[i] == prep_str_2[i + 1]:
                if prep_str_2[i] == 'X':
                    preparation_output.append(prep_str_2[i])
                    preparation_output.extend('ZXQ')
                    preparation_output.append(prep_str_2[i + 1])
                else:
                    preparation_output.append(prep_str_2[i])
                    preparation_output.extend('XQZ')
                    preparation_output.append(prep_str_2[i + 1])
            else:
                if prep_str_2[i] == prep_str_2[i - 1] and prep_str_2[i] != 'X':#
                    preparation_output.extend('XQZ')#
                    preparation_output.append(prep_str_2[i])#
                    preparation_output.append(prep_str_2[i + 1])#
                else:#
                    preparation_output.append(prep_str_2[i])
                    preparation_output.append(prep_str_2[i + 1])
        else:
            if len(prep_str_2) % 2 != 0:
                if prep_str_2[-2] == 'X' and prep_str_2[-1] == 'X':#
                    preparation_output.extend('ZXQ')#
                    preparation_output.append(prep_str_2[-1])#
                else:#
                    preparation_output.append(prep_str_2[-1])
    if len(preparation_output) % 2 != 0:
        if preparation_output[-1] == 'X':
            preparation_output.extend('ZXQ')
        else:
            preparation_output.extend('XQZ')
        
    return preparation_output


def locs(ch, ch2, matr):
        loc = []
        loc2 = []
        for i, j in enumerate(matr):
            for k, l in enumerate(j):
                if ch == l:
                    loc.append(i)
                    loc.append(k)
                if ch2 == l:
                    loc2.append(i)
                    loc2.append(k)
                if loc and loc2:
                    break
            else:
                continue
            return loc, loc2


def encrypt(msg, matr):
    res = []
    h = 0
    while h < len(msg):
        loc, loc2 = locs(msg[h], msg[h + 1], matr)

        if loc[1] == loc2[1]:
            res.append(matr[(loc[0] + 1) % 5][loc[1]])
            res.append(matr[(loc2[0] + 1) % 5][loc2[1]])
        elif loc[0] == loc2[0]:
            res.append(matr[loc[0]][(loc[1] + 1) % 5])
            res.append(matr[loc2[0]][(loc2[1] + 1) % 5])
        else:
            res.append(matr[loc[0]][loc2[1]])
            res.append(matr[loc2[0]][loc[1]])
        h += 2

    i = 5
    while i < len(res):
        res.insert(i, ' ')
        i += 6

    return res


def decrypt(msg, matr):
    res = []
    h = 0
    while h < len(msg):
        loc, loc2 = locs(msg[h], msg[h + 1], matr)

        if loc[1] == loc2[1]:
            res.append(matr[(loc[0] - 1) % 5][loc[1]])
            res.append(matr[(loc2[0] - 1) % 5][loc2[1]])
        elif loc[0] == loc2[0]:
            res.append(matr[loc[0]][(loc[1] - 1) % 5])
            res.append(matr[loc2[0]][(loc2[1] - 1) % 5])
        else:
            res.append(matr[loc[0]][loc2[1]])
            res.append(matr[loc2[0]][loc[1]])
        h += 2

    CT = []
    i = 0
    while i < len(res):

        if res[i:i+3] == ['X', 'Q', 'X']:
            CT.append(' ')
            i = i + 3
        elif res[i:i+3] == ['X', 'Q', 'Z']:#
            i = i + 3
        elif res[i:i+3] == ['Z', 'X', 'Q']:#
            i = i + 3
        else:
            CT.append(res[i])
            i = i + 1
    output_list = list()
    i = 0
    while i < len(CT):
        found = False
        for key in numbers:
            if ''.join(CT[i:i+len(key)]) == key:
                output_list.append(numbers[key])
                i += len(key)
                found = True
                break
        if not found:
            output_list.append(CT[i])
            i += 1

    return output_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = PlayfairCipherGui()
    gui.show()

    try:
        sys.exit(app.exec())
    except:
        print("Successfully Exited")