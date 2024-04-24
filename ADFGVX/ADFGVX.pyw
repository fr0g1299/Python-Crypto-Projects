# ADFG(V)X Cipher
# fr0g1299


import re  # removes extra spaces
import sys  # exit
import unicodedata  # removes diacritics
import os  # for .ui path
import random  # for shuffle
import math  # for column space indexes

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSequentialAnimationGroup, QEvent
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

numbers = {'ZEERO' : '0', 'ONNE' : '1', 'TVVO' : '2', 'THHREE' : '3', 'FOOUR' : '4',
            'FIIVE' : '5', 'SIIX' : '6', 'SEEVEN' : '7', 'EIIGHT' : '8', 'NIINE' : '9'}

numbers_contrary = dict((v, k) for (k, v) in numbers.items())

ADFGVX = 'ADFGVX'

ADFGX = 'ADFGX'

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

# StyleSheet for graying out radio buttons
rd_btn_css = ("QRadioButton {{\n"
            "color: rgb({text_color});\n"
            "font-size: 13px;}}\n"
            "QRadioButton::indicator {{\n"
            "width: 11px;\n"
            "height: 11px;\n"
            "border-radius: 5px;}}\n"
            "QRadioButton::indicator::unchecked{{\n"
            "border: 1px solid;\n"
            "border-color: rgb({border_color});\n"
            "border-radius: 2px;\n"
            "background-color: rgba(28, 29, 36, 235);\n"
            "width: 11px;\n"
            "height: 11px;}}\n"
            "QRadioButton::indicator::checked{{\n"
            "border: 4px solid;\n"
            "border-color: rgb({border_color});\n"
            "border-radius: 3px;\n"
            "background-color: rgba(28, 29, 36, 235);\n"
            "width: 6px;\n"
            "height: 6px;}}\n")

inactive_style = rd_btn_css.format(text_color = "150, 150, 150", border_color = "75, 0, 0")

active_style = rd_btn_css.format(text_color = "240, 240, 240", border_color = "150, 0, 0")


class ADFGVXCipherGui(QDialog):

    def __init__(self):
        # Necessary stuff
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        form_class = os.path.join(ui_path, "ADFGVXCipherGui.ui")
        loadUi(form_class, self)
        self.setWindowTitle("ADFGVX Cipher")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedHeight(728)
        self.setFixedWidth(1060)

        self.fadeQuick(self.lbl_enc_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_dec_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_matr_cp)  # Quickly fades, so the animation works later
        self.CTInput.installEventFilter(self)  # Makes Enter usable
        self.OTInput.installEventFilter(self)  # Makes Enter usable
        self.key_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.matr_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.CTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.OTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.key_input.setTabChangesFocus(True)  # Makes Tab usable
        self.matr_input.setTabChangesFocus(True)  # Makes Tab usable
        self.table_alpha.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Makes it, so Hheader is not draggable
        self.table_alpha.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Makes it, so Vheader is not draggable
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Removes Default Window Frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes QDialog translucent

        self.btn_enc.clicked.connect(self.goToEncrypt)  # Encrypt Button
        self.btn_enc_cp.clicked.connect(lambda: self.copyToClipboard(1))  # Copy Encrypt result Button
        self.btn_enc_res.clicked.connect(self.resetEncrypt)  # Resets Encrypt prep and res text

        self.btn_dec.clicked.connect(self.goToDecrypt)  # Decrypt Button
        self.btn_dec_cp.clicked.connect(lambda: self.copyToClipboard(2))  # Copy Decrypt result Button
        self.btn_dec_res.clicked.connect(self.resetDecrypt)  # Resets Decrypt prep and res text
 
        self.btn_matr_cp.clicked.connect(lambda: self.copyToClipboard(3))  # Copy Matrix Button
        self.btn_tab_res.clicked.connect(self.resetTable)  # Resets Table

        self.chk_5x5.stateChanged.connect(self.update_radio_buttons_state)  # Enables/Disables radio buttons
        
        self.btn_min.clicked.connect(self.minimizeWindow)  # Enables minimize button
        self.btn_cls.clicked.connect(lambda: app.exit())  # Enables close button
        self.title_bar.mouseMoveEvent = self.moveWindow  # Enables Click&Drag on the window

        # Shadow on the frameless window
        shadow_window = QGraphicsDropShadowEffect()
        shadow_window.setBlurRadius(5)
        shadow_window.setOffset(3)
        shadow_window.setColor(QColor(50, 50, 50, 160))
        self.bgwidget.setGraphicsEffect(shadow_window)

    def update_radio_buttons_state(self):
        '''Enables/Disables radio buttons and changes their color.'''
        if self.chk_5x5.isChecked():
            self.rd_btn_czech.setEnabled(True)
            self.rd_btn_english.setEnabled(True)

            self.rd_btn_czech.setStyleSheet(active_style)
            self.rd_btn_english.setStyleSheet(active_style)
        else:
            self.rd_btn_czech.setEnabled(False)
            self.rd_btn_english.setEnabled(False)

            self.rd_btn_czech.setStyleSheet(inactive_style)
            self.rd_btn_english.setStyleSheet(inactive_style)

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
        elif obj is self.matr_input and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                return True
        return super().eventFilter(obj, event)    
    
    def get_key(self):
        '''
        Prepares key.
        Removes repeating spaces. Removes special symbols and diacritics.
        '''
        rd = bool(self.rd_btn_czech.isChecked())
        key = self.key_input.toPlainText().upper()
        key = unicodedata.normalize('NFKD', key)\
                .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
        key = ''.join(letter for letter in key if letter in symbols).strip()
        key = re.sub(r'\s+', '', key, flags=re.UNICODE)

        if len(key) < 4:
           return 0
        return key, rd
    
    def goToEncrypt(self):
        try:
            emp = bool(self.OTInput.toPlainText() == '')
            key, rd = self.get_key()
            chk_adfgx = bool(self.chk_5x5.isChecked())
            chk_matr = bool(self.checkBox_2.isChecked())
            matr_refused = ''
            unique = ''

            if chk_adfgx:
                if chk_matr:
                    if rd:
                        if chk_matr and rd:  # ADFGX-CS, user created matrix
                            ran_table, matr_refused, unique = get_matrix(self.matr_input.toPlainText(), True, True)
                    else:
                        if chk_matr and not rd:  # ADFGX-EN, user created matrix
                            ran_table, matr_refused, unique = get_matrix(self.matr_input.toPlainText(), False, True)
                elif rd:  # ADFGX-CS, random matrix
                    ran_table = generate_non_repeating_strings(True, True)
                else:  # ADFGX-EN, random matrix
                    ran_table = generate_non_repeating_strings(True)

                if matr_refused != '' or unique != '':
                    if matr_refused == '':
                        matr_refused = 'None'
                    if unique == '':
                        unique = 'All characters present'
                    self.showInformationMessageBox(3, matr_refused, unique)
                    return 0

                matr = create_matr(ran_table, 5, 5)
                self.table_alpha.setColumnCount(5)
                self.table_alpha.setRowCount(5)
                for i in range(5):
                    self.table_alpha.setColumnWidth(i, 80)
                    self.table_alpha.setRowHeight(i, 67)

                self.table_alpha.setHorizontalHeaderLabels(['A', 'D', 'F', 'G', 'X'])
                self.table_alpha.setVerticalHeaderLabels(['A', 'D', 'F', 'G', 'X'])
                for i in range(5):
                    for j in range(5):
                        itm = QTableWidgetItem(matr[i][j])
                        itm.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))
            else:
                if chk_matr:
                    ran_table, matr_refused, unique = get_matrix(self.matr_input.toPlainText())
                else:
                    ran_table = generate_non_repeating_strings()

                if matr_refused != '' or unique != '':
                    if matr_refused == '':
                        matr_refused = 'None'
                    if unique == '':
                        unique = 'All characters present'
                    self.showInformationMessageBox(3, matr_refused, unique)
                    return 0
                
                self.table_alpha.setColumnCount(6)
                self.table_alpha.setRowCount(6)
                for i in range(6):
                    self.table_alpha.setColumnWidth(i, 67)
                    self.table_alpha.setRowHeight(i, 56)

                self.table_alpha.setHorizontalHeaderLabels(['A', 'D', 'F', 'G', 'V', 'X'])
                self.table_alpha.setVerticalHeaderLabels(['A', 'D', 'F', 'G', 'V', 'X'])
                font = QFont()
                font.setBold(True)
                self.table_alpha.horizontalHeader().setFont(font)
                self.table_alpha.verticalHeader().setFont(font)
                self.table_alpha.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
                self.table_alpha.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)

                matr = create_matr(ran_table, 6, 6)
                for i in range(6):
                    for j in range(6):
                        itm = QTableWidgetItem(matr[i][j])
                        itm.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))

            if not emp:
                prep = preparation(self.OTInput.toPlainText(), rd, chk_adfgx)
                prep2 = list(prep)

                if len(prep) == 0:
                    self.showInformationMessageBox()

                # Space after row
                i = len(key)
                while i < len(prep2):
                    prep2.insert(i, ' ')
                    i += len(key) + 1

                # Space after column
                # i = math.ceil(len(prep2) * 2 / len(key))
                # while i < len(prep2):
                #     prep2.insert(i, ' ')
                #     i += math.ceil(len(prep2) * 2 / len(key)) + 1

                self.lbl_enc_prep.setText(''.join(prep2))

                enc, matr = encrypt(prep, matr, key, chk_adfgx)
                self.lbl_enc_res.setText(''.join(enc))

                self.matr = matr
            else:
                self.showInformationMessageBox()
        except:
            self.showCriticalMessageBox()

    def goToDecrypt(self):
        try:
            emp = bool(self.CTInput.toPlainText() == '')
            key, rd = self.get_key()
            chk_adfgx = bool(self.chk_5x5.isChecked())
            chk_matr = bool(self.checkBox_2.isChecked())
            matr_refused = ''
            unique = ''
            
            if not chk_matr:
                try:
                    matr = self.matr
                except:
                    self.showInformationMessageBox(2)
                    return 0
            
            if chk_matr:
                if chk_adfgx:
                    if rd:
                        if chk_matr and rd:
                            matr, matr_refused, unique = get_matrix(self.matr_input.toPlainText(), True, True)
                    else:
                        if chk_matr and not rd:
                            matr, matr_refused, unique = get_matrix(self.matr_input.toPlainText(), False, True)
                else:
                    matr, matr_refused, unique = get_matrix(self.matr_input.toPlainText())
            
            if matr_refused != '' or unique != '':
                if matr_refused == '':
                    matr_refused = 'None'
                if unique == '':
                    unique = 'All characters present'
                self.showInformationMessageBox(3, matr_refused, unique)
                return 0

            if not emp:
                prep = self.CTInput.toPlainText().upper()
                prep = prep.replace(' ', '')
                prep = unicodedata.normalize('NFKD', prep)\
            .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
                if chk_adfgx:
                    prep = ''.join(letter for letter in prep if letter in ADFGX or letter.isspace()).strip()
                else:
                    prep = ''.join(letter for letter in prep if letter in ADFGVX or letter.isspace()).strip()

                prep2 = list(prep)

                # Space after row
                i = len(key)
                while i < len(prep2):
                    prep2.insert(i, ' ')
                    i += len(key) + 1

                # Space after column
                # i = math.ceil(len(prep2) * 2 / len(key))
                # while i < len(prep2):
                #     prep2.insert(i, ' ')
                #     i += math.ceil(len(prep2) * 2 / len(key)) + 1
                
                self.lbl_dec_prep.setText(''.join(prep2))

                dec = decrypt(prep, matr, key, chk_adfgx)
                self.lbl_dec_res.setText(''.join(dec))
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
        msg.setText("Key should be longer or you chose a different language...")
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInformationMessageBox(self, chk = 1, matr_refused = '', unique = ''):
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
            case 2:
                msg.setText("You must first encrypt, so the matrix creates itself. Or insert your own...")
            case _:
                msg.setText(f"Matrix refused these characters: {matr_refused}\nMatrix is missing these characters: {unique}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def copyToClipboard(self, num):
        match num:
            case 1:
                if self.lbl_enc_res.toPlainText() != '':
                    cb = QApplication.clipboard()
                    cb.setText(self.lbl_enc_res.toPlainText(), mode=cb.Clipboard)
                    self.fade(self.lbl_enc_cp)
                else: pass
            case 2:
                if self.lbl_dec_res.toPlainText() != '':
                    cb = QApplication.clipboard()
                    cb.setText(self.lbl_dec_res.toPlainText(), mode=cb.Clipboard)
                    self.fade(self.lbl_dec_cp)
                else: pass
            case 3:
                try:
                    matr = ''
                    chk_adfgx = bool(self.chk_5x5.isChecked())
                    tmp = []
                    if chk_adfgx:
                        for i in range(5):
                            for j in range(5):
                                tmp.extend(self.table_alpha.item(i , j).text().upper())
                                matr += tmp[0]
                                tmp = []
                    else:
                        for i in range(6):
                            for j in range(6):
                                tmp.extend(self.table_alpha.item(i , j).text().upper())
                                matr += tmp[0]
                                tmp = []
                    if matr != '':
                        cb = QApplication.clipboard()
                        cb.setText(matr, mode=cb.Clipboard)
                        self.fade(self.lbl_matr_cp)
                    else: pass
                except:
                    return 0
        
    def resetEncrypt(self):
        '''Empties encryption result and preparation.'''
        self.OTInput.clear()
        self.lbl_enc_prep.clear()
        self.lbl_enc_res.clear()

    def resetDecrypt(self):
        '''Empties decryption result and preparation.'''
        self.CTInput.clear()
        self.lbl_dec_prep.clear()
        self.lbl_dec_res.clear()

    def resetTable(self):
        '''Empties table.'''
        for i in range(6):
            for j in range(6):
                itm = QTableWidgetItem()
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_alpha.setItem(i, j, QtWidgets.QTableWidgetItem(itm))

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


def create_matr(alp, a, b):
    '''Creates a matrix with the shuffled/inserted alphabet.'''
    k = 0
    matr = matrix(a, b, 0)
    for i in range(0,b):
        for j in range(0,b):
            matr[i][j] = alp[k]
            k += 1
    return matr


def get_matrix(txt, chk_lang = False, chk_adfgx = False):
    '''Obtains and checks inserted matrix from GUI.'''
    alp_adfgx_cs = set('ABCDEFGHIJKLMNOPQRSTUVXYZ')
    alp_adfgx_en = set('ABCDEFGHIKLMNOPQRSTUVWXYZ')
    alp = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    seen = set()

    matr = txt.strip().upper()
    matr = unicodedata.normalize('NFKD', matr)\
            .encode('ASCII', 'ignore').decode('utf-8', 'ignore')

    if chk_adfgx:
        if chk_lang:
            matr_refused = ''.join(letter for letter in matr if letter not in symbols or letter == 'W' or letter.isdecimal())
            matr = ''.join(letter for letter in matr if letter in alp_adfgx_cs or letter not in matr)
        else:
            matr_refused = ''.join(letter for letter in matr if letter not in symbols or letter == 'J' or letter.isdecimal())
            matr = ''.join(letter for letter in matr if letter in alp_adfgx_en or letter not in matr)
    else:
        matr_refused = ''.join(letter for letter in matr if letter not in symbols)
        matr = ''.join(letter if (letter not in symbols or letter not in seen) and not seen.add(letter) else '' for letter in matr)

    matr = re.sub(r'\s+', '', matr, flags=re.UNICODE)
    
    tmp = len(matr_refused)
    matr_refused = re.sub(r'\s+', '', matr_refused, flags=re.UNICODE)
    if len(matr_refused) != tmp:
        matr_refused += ' [Excess spaces]'

    matr_set = set(matr)
    if chk_adfgx:
        if chk_lang:
            unique = alp_adfgx_cs.difference(matr_set)
        else:
            unique = alp_adfgx_en.difference(matr_set)
    else:
        unique = alp.difference(matr_set)

    unique = ''.join(sorted(unique))

    if chk_adfgx:
        if len(matr) == 26:
            if unique == '':
                return matr, matr_refused, unique
            else:
                return matr, matr_refused, unique
        else:
            return matr, matr_refused, unique
    else:
        if len(matr) == 36:
            if unique == '':
                return matr, matr_refused, unique
            else:
                return matr, matr_refused, unique
        else:
            return matr, matr_refused, unique


def matrix(x,y,initial):
    return [[initial for i in range(x)] for j in range(y)]


def preparation(txt, rd, chk):
    '''
    Removes repeating spaces. Removes special symbols and diacritics.
    Substitutes spaces with 'XQX' symbol for decryption.
    Substitutes 'W'(Czech) or 'J'(English) and numbers,
    if ADFGX checkbox is checked in GUI.
    '''
    prep_str = txt.strip().upper()
    prep_str = unicodedata.normalize('NFKD', prep_str)\
            .encode('ASCII', 'ignore').decode('utf-8', 'ignore')
    prep_str = ''.join(letter for letter in prep_str if letter in symbols or letter.isspace()).strip()
    prep_str = re.sub(r'\s+', ' ', prep_str, flags=re.UNICODE)

    preparation_output = []

    for letter in prep_str:
        if letter.isspace():
            preparation_output.extend(['X', 'Q', 'X'])
        elif letter in numbers.values() and chk:
            preparation_output.extend(numbers_contrary[letter])
        elif letter == 'W' and rd and chk:
            preparation_output.append('V')
        elif letter == 'J' and not rd and chk:
            preparation_output.append('I')
        else:
            preparation_output.append(letter)
        
    return preparation_output


def generate_non_repeating_strings(chk = False, chk2 = False):
    if chk:
        if chk2:
            res = list('ABCDEFGHIJKLMNOPQRSTUVXYZ')  # ADFGX-CS
            random.shuffle(res)
        elif not chk2:
            res = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')  # ADFGX-EN
            random.shuffle(res)
    else:
        res = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        random.shuffle(res)
    return res


def encrypt(msg, matr, key, chk):
    n = len(key)
    k = sorted(range(n), key=lambda i: key[i])

    matr_str = ''
    for i in range(len(matr[0])):
        matr_str += ''.join(matr[i])
    msg = ''.join(msg)

    s = []
    for c in msg:
        if chk:
            row, col = divmod(matr_str.index(c), 5)
            s += [ADFGX[row], ADFGX[col]]
        else:
            row, col = divmod(matr_str.index(c), 6)
            s += [ADFGVX[row], ADFGVX[col]]

    res = ''.join(s[j] for i in k for j in range(i, len(s), n))
    res = list(res)

    # Space after row
    i = n
    while i < len(res):
        res.insert(i, ' ')
        i += n + 1

    # Space after column
    # i = math.ceil(len(res) / n)
    # while i < len(res):
    #     res.insert(i, ' ')
    #     i += math.ceil(len(res) / n) + 1

    return res, matr_str


def decrypt(msg, matr, key, chk):
    n = len(key)
    k = sorted(range(n), key=lambda i: key[i])

    msg = ''.join(msg)
    
    m = len(msg)
    x = [j for i in k for j in range(i, m, n)]

    y = ['']*m
    for i, c in zip(x, msg): y[i] = c
    s = []
       
    if chk:
        for i in range(0, m, 2):
            row, col = y[i:i+2]
            s.append(matr[5 * ADFGX.index(row) + ADFGX.index(col)])
    else:
        for i in range(0, m, 2):
            row, col = y[i:i+2]
            s.append(matr[6 * ADFGVX.index(row) + ADFGVX.index(col)])

    cipher_text = []
    i = 0
    while i < len(s):
        if s[i:i+3] == ['X', 'Q', 'X']:
            cipher_text += ' '
            i = i + 3
        else:
            cipher_text += s[i]
            i = i + 1

    output_list = []
    i = 0
    while i < len(cipher_text):
        found = False
        for key in numbers:
            if ''.join(cipher_text[i:i+len(key)]) == key:
                output_list.append(numbers[key])
                i += len(key)
                found = True
                break
        if not found:
            output_list.append(cipher_text[i])
            i += 1

    return output_list


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = ADFGVXCipherGui()
    gui.show()

    try:
        sys.exit(app.exec())
    except:
        print("Successfully Exited")