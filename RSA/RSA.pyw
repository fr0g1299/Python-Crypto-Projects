# RSA Cipher
# fr0g1299


import re  # removes extra spaces
import sys  # exit
import os  # for .ui path
import random  # for shuffle
import math  # for column space indexes

from PyQt5 import QtCore
from PyQt5.QtCore import QSequentialAnimationGroup, QEvent
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

numbers = '0123456789'

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

# StyleSheet for graying out decryption input
dec_input_css = ("QTextEdit {{\n"
            "border: 2px solid rgba({border_color});\n"
            "border-radius: 20px;\n"
            "color: {text_color};\n"
            "font-size: 12px;\n"
            "padding-left: 10px;\n"
            "padding-right: 10px;\n"
            "background-color: rgba({back_color});}}\n"
        "QTextEdit:hover {{\n"
            "border: 2px solid rgb(48, 50, 62);}}\n"
        "QTextEdit:focus {{\n"
            "border: 2px solid rgb(85, 170, 255);\n"
            "background-color: rgba(43, 45, 56, 235);}}\n")

# StyleSheet for graying out decryption keys
dec_css = ("QTextBrowser {{\n"
	"border: 2px solid rgba({border_color});\n"
	"border-radius: 20px;\n"
	"background-color: rgba({back_color});\n"
	"font-size: 12px;\n"
	"padding-left: 10px;\n"
	"padding-right: 10px;\n"
	"color: rgb({text_color});}}\n")

# StyleSheet for graying out decryption buttons
dec_btn_css = ("QPushButton {{\n"
	    "background-color: rgb({back_color});\n"
	    "border: none;\n"
	    "padding-top: 5px;\n"
	    "padding-bottom: 5px;\n"
	    "color: rgb({text_color});\n"
	    "border-left: 2px solid rgb({border_color});\n"
	    "border-right: 1px solid rgb({border_color});\n"
	    "border-bottom: 2px solid rgb({border_color});\n"
	    "border-radius: {border};}}\n"
    "QPushButton:hover {{\n"
	    "background-color: rgb(170, 0, 0);\n"
	    "border-left: 2px solid rgb(130, 0, 0);\n"
	    "border-right: 1px solid rgb(130, 0, 0);\n"
	    "border-bottom: 2px solid rgb(130, 0, 0);}}\n"
    "QPushButton:pressed {{\n"
	    "background-color: rgb(140, 0, 0);\n"
	    "border-left: 1px solid rgb(130, 0, 0);\n"
	    "border-right: 2px solid rgb(130, 0, 0);\n"
	    "border-top: 2px solid rgb(130, 0, 0);\n"
	    "padding-top: -5px;\n"
	    "padding-bottom: -5px;\n"
	    "padding-left: 5px;\n"
	    "border-bottom: none;}}\n")

inactive_style_btn = dec_btn_css.format(back_color = "85, 0, 0", border_color = "70, 0, 0", text_color = "150, 160, 140", border = "12.4px")
active_style_btn = dec_btn_css.format(back_color = "150, 0, 0", border_color = "130, 0, 0", text_color = "206, 214, 196", border = "12.4px")

inactive_style_btn_other = dec_btn_css.format(back_color = "85, 0, 0", border_color = "70, 0, 0", text_color = "150, 160, 140", border = "5px")
active_style_btn_other =  dec_btn_css.format(back_color = "150, 0, 0", border_color = "130, 0, 0", text_color = "206, 214, 196", border = "5px")

inactive_style_in = dec_input_css.format(back_color = "22, 24, 32, 125", border_color = "30, 32, 40, 200", text_color = "#646464")
active_style_in = dec_input_css.format(back_color = "34, 36, 44, 225", border_color = "37, 39, 48, 255", text_color = "#FFF")

inactive_style_out = dec_css.format(back_color = "22, 24, 32, 125", border_color = "30, 32, 40, 200", text_color = "90, 90, 90")
active_style_out = dec_css.format(back_color = "34, 36, 44, 225", border_color = "37, 39, 48, 255", text_color = "200, 200, 200;")
active_style_out_res = dec_css.format(back_color = "34, 36, 44, 225", border_color = "37, 39, 48, 255", text_color = "255, 255, 255;")


class RSACipherGui(QDialog):

    def __init__(self):
        # Necessary stuff
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        form_class = os.path.join(ui_path, "RSACipherGui.ui")
        loadUi(form_class, self)
        self.setWindowTitle("RSA Cipher")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedHeight(728)
        self.setFixedWidth(1060)

        self.fadeQuick(self.lbl_enc_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_dec_cp)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_enc_cp_to)  # Quickly fades, so the animation works later
        self.CTInput.installEventFilter(self)  # Makes Enter usable
        self.OTInput.installEventFilter(self)  # Makes Enter usable

        self.publ_key_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.priv_key_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.n_key_input.installEventFilter(self)  # Disables Enter, so it doesn't skip
        self.CTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.OTInput.setTabChangesFocus(True)  # Makes Tab usable
        self.publ_key_input.setTabChangesFocus(True)  # Makes Tab usable
        self.priv_key_input.setTabChangesFocus(True)  # Makes Tab usable
        self.n_key_input.setTabChangesFocus(True)  # Makes Tab usable

        self.publ_key_input.setAlignment(QtCore.Qt.AlignCenter)  # Text Align for keys
        self.priv_key_input.setAlignment(QtCore.Qt.AlignCenter)  # Text Align for keys
        self.n_key_input.setAlignment(QtCore.Qt.AlignCenter)  # Text Align for keys

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Removes Default Window Frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes QDialog translucent

        self.btn_enc.clicked.connect(self.goToEncrypt)  # Encrypt Button
        self.btn_enc_cp.clicked.connect(lambda: self.copyToClipboard(1))  # Copy Encrypt result Button
        self.btn_enc_res.clicked.connect(self.resetEncrypt)  # Resets Encrypt keys and res text

        self.btn_dec.clicked.connect(self.goToDecrypt)  # Decrypt Button
        self.btn_dec_cp.clicked.connect(lambda: self.copyToClipboard(2))  # Copy Decrypt result Button
        self.btn_dec_res.clicked.connect(self.resetDecrypt)  # Resets Decrypt keys and res text

        self.btn_enc_cp_to.clicked.connect(self.pasteKeys)  # Pastes keys from encrypt to inputs
        self.checkBox.stateChanged.connect(self.updateDecState)  # Enables/Disables decrypt

        self.btn_min.clicked.connect(self.minimizeWindow)  # Enables minimize button
        self.btn_cls.clicked.connect(lambda: app.exit())  # Enables close button
        self.title_bar.mouseMoveEvent = self.moveWindow  # Enables Click&Drag on the window

        # Shadow on the frameless window
        shadow_window = QGraphicsDropShadowEffect()
        shadow_window.setBlurRadius(5)
        shadow_window.setOffset(3)
        shadow_window.setColor(QColor(50, 50, 50, 160))
        self.bgwidget.setGraphicsEffect(shadow_window)

    def updateDecState(self):
        '''Enables/Disables radio buttons and changes their color.'''
        widgets = [
            (self.CTInput, active_style_in, inactive_style_in),
            (self.lbl_dec_nkey, active_style_out, inactive_style_out),
            (self.lbl_dec_privkey, active_style_out, inactive_style_out),
            (self.lbl_dec_res, active_style_out_res, inactive_style_out),
            (self.btn_dec, active_style_btn, inactive_style_btn),
            (self.btn_dec_cp, active_style_btn_other, inactive_style_btn_other),
            (self.btn_dec_res, active_style_btn_other, inactive_style_btn_other)]

        state = self.checkBox.isChecked()

        for widget, active_style, inactive_style in widgets:
            widget.setEnabled(state)
            widget.setStyleSheet(active_style if state else inactive_style)

    def pasteKeys(self):
        '''Copies and Pastes keys from encryption to custom input.'''
        n = self.lbl_enc_nkey.toPlainText()[7::]
        e = self.lbl_enc_publkey.toPlainText()[12::]
        d = self.lbl_enc_privkey.toPlainText()[13::]
        if n != '':
            self.n_key_input.setPlainText(n)
            self.publ_key_input.setPlainText(e)
            self.priv_key_input.setPlainText(d)
            self.publ_key_input.setAlignment(QtCore.Qt.AlignCenter)
            self.priv_key_input.setAlignment(QtCore.Qt.AlignCenter)
            self.n_key_input.setAlignment(QtCore.Qt.AlignCenter)
            self.fade(self.lbl_enc_cp_to)

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
        elif obj is self.publ_key_input and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                return True
        elif obj is self.priv_key_input and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                return True
        elif obj is self.n_key_input and event.type() == QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                return True
        return super().eventFilter(obj, event)

    def getKey(self, chk) -> int:
        '''
        Prepares key.
        Removes repeating spaces. Removes special symbols and diacritics.
        '''
        try:
            match chk:
                case 1:
                    publ_key = self.publ_key_input.toPlainText()
                    n = self.n_key_input.toPlainText()
                    publ_key, n = prepare_key(publ_key, n)
                    if (publ_key == '' or n == '') or not (22 <= len(str(publ_key)) <= 24) or not (23 <= len(str(n)) <= 24):
                        return 0
                    return publ_key, n
                case 2:
                    priv_key = self.priv_key_input.toPlainText()
                    n = self.n_key_input.toPlainText()
                    priv_key, n = prepare_key(priv_key, n)
                    if (priv_key == '' or n == '') or not (21 <= len(str(priv_key)) <= 24) or not (23 <= len(str(n)) <= 24):
                        return 0
                    return priv_key, n
                case 3:
                    publ_key, priv_key = generate_keys()
                    return publ_key, priv_key
        except:
            return 0

    def goToEncrypt(self):
        try:
            emp = bool(self.OTInput.toPlainText() == '')
            rd = bool(self.checkBox.isChecked())
            chk = False

            if not emp:
                if rd:
                    try:
                        key, n = self.getKey(1)
                    except:
                        chk = True
                        self.showInformationMessageBox(2)
                else:
                    publ_key, priv_key = self.getKey(3)

                prep = self.OTInput.toPlainText()
                prep = generate_msg(prep)
                if prep == '':
                    self.showInformationMessageBox()
                    return 0
                
                if rd:
                    c = encrypt(prep, key, n)
                else:
                    c = encrypt(prep, publ_key[1], publ_key[0])

                if rd:
                    self.lbl_enc_nkey.setText(f'N Key:\n{''.join(str(n))}')
                    self.lbl_enc_publkey.setText(f'Public Key:\n{''.join(str(key))}')
                    self.lbl_enc_privkey.setText('Private Key:\n')
                else:
                    self.lbl_enc_nkey.setText(f'N Key:\n{str(publ_key[0])}')
                    self.lbl_enc_publkey.setText(f'Public Key:\n{str(publ_key[1])}')
                    self.lbl_enc_privkey.setText(f'Private Key:\n{str(priv_key[1])}')
                self.lbl_enc_res.setText(''.join(c))
            else:
                self.showInformationMessageBox()
        except:
            if not chk:
                self.showCriticalMessageBox()

    def goToDecrypt(self):
        try:
            emp = bool(self.CTInput.toPlainText() == '')
            chk = False

            if not emp:
                try:
                    key, n = self.getKey(2)
                except:
                    chk = True
                    self.showInformationMessageBox(2)

                prep = self.CTInput.toPlainText()
                prep = ''.join(number for number in prep if number in numbers).strip()
                prep = re.sub(r'\s+', '', prep, flags=re.UNICODE)
                if prep == '':
                    self.showInformationMessageBox()
                    return 0

                _, res = decrypt(prep, key, n)

                self.lbl_dec_nkey.setText(f'N Key:\n{''.join(str(n))}')
                self.lbl_dec_privkey.setText(f'Private Key:\n{''.join(str(key))}')
                self.lbl_dec_res.setText(''.join(res))
            else:
                self.showInformationMessageBox()
        except:
            if not chk:
                self.showCriticalMessageBox()

    def showCriticalMessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)

        msg.setWindowTitle("Error")
        msg.setWindowIcon(QIcon('icon.png'))
        msg.setText("Something's wrong, I can feel it...")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInformationMessageBox(self, chk = 1):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)

        msg.setWindowTitle("Information")
        msg.setWindowIcon(QIcon('icon.png'))
        match chk:
            case 1:
                msg.setText("Message was not inserted...")
            case 2:
                msg.setText("Keys not inserted, or they are not coprime...")
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
        return 0

    def resetEncrypt(self):
        '''Empties encryption result and keys.'''
        self.OTInput.clear()
        self.lbl_enc_nkey.setText('N Key:\n')
        self.lbl_enc_publkey.setText('Public Key:\n')
        self.lbl_enc_privkey.setText('Private Key:\n')
        self.lbl_enc_res.clear()

    def resetDecrypt(self):
        '''Empties decryption result and keys.'''
        self.CTInput.clear()
        self.lbl_dec_nkey.setText('N Key:\n')
        self.lbl_dec_privkey.setText('Private Key:\n')
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

        match widget:
            case self.lbl_enc_cp:
                self.anim_group = QSequentialAnimationGroup()
                self.anim_group.addAnimation(self.anim)
                self.anim_group.addPause(2000)
                self.anim_group.addAnimation(self.anim_2)
                self.anim_group.start()
            case self.lbl_enc_cp_to:
                self.anim_group_2 = QSequentialAnimationGroup()
                self.anim_group_2.addAnimation(self.anim)
                self.anim_group_2.addPause(2000)
                self.anim_group_2.addAnimation(self.anim_2)
                self.anim_group_2.start()
            case self.lbl_dec_cp:
                self.anim_group_3 = QSequentialAnimationGroup()
                self.anim_group_3.addAnimation(self.anim)
                self.anim_group_3.addPause(2000)
                self.anim_group_3.addAnimation(self.anim_2)
                self.anim_group_3.start()

    def fadeQuick(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(0)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


def prepare_key(key, n) -> int:
    key = ''.join(number for number in key if number in numbers).strip()
    key = re.sub(r'\s+', '', key, flags=re.UNICODE)

    n = ''.join(number for number in n if number in numbers).strip()
    n = re.sub(r'\s+', '', n, flags=re.UNICODE)

    key = int(key)
    n = int(n)

    if math.gcd(key, n) != 1:
        return 0
    return key, n


def generate_keys():
    p = generate_coprime_prime()
    while True:
        q = generate_coprime_prime()
        if p != q:
            break

    n = p * q
    eu = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, eu - 1)
        if e < eu and math.gcd(e, eu) == 1 and (22 <= len(str(e)) <= 24):
            break
    d = pow(e, -1, eu)

    return (n, e), (n, d)


def generate_coprime_prime():
    while True:
        num = random.randint(10**11, 10**12 - 1)
        if math.gcd(num, 10**11) == 1:
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    break
            else:
                    return num


def generate_msg(txt):
    prep_str = txt.strip()
    prep_str = re.sub(r'\s+', ' ', prep_str, flags=re.UNICODE)

    if prep_str == '':                     
        return ''

    h = []
    while True:
        h.append(prep_str[:8])
        prep_str = prep_str[8:]
        if len(prep_str) == 0:
            break

    tmp = ''
    if len(str(h[-1])) != 8:
        tmp += h[-1]
        tmp += 'Ͽ'*(8 - len(str(h[-1])))
        h[-1] = tmp

    binary_data = []
    for block in h:
        temp = ''
        for char in block:
            ascii_value = ord(char)
            # Skip characters with ASCII values greater than 1023
            if ascii_value <= 1023:
                temp += format(ascii_value, "010b")
        binary_data.append(temp)

    msg_dec = []
    for block in binary_data:
        msg_dec.append(int(block, 2))
    return msg_dec


def encrypt(msg, publ, n):
    c = []
    for block in msg:
        c.append(pow(block, publ, n))

    res_c = []
    max = 24
    
    for block in c:
        while len(str(block)) % max != 0:
            block = '0' + str(block)
        res_c.append(str(block))

    res_c = ''.join(map(str, res_c))
    res_c = ' '.join(res_c[i:i+8] for i in range(0,len(res_c),8))
    
    return res_c


def decrypt(msg, priv, n):
    s = [msg[i:i + 24] for i in range(0, len(msg), 24)]
    int_list = [int(x) for x in s]

    d = []
    for block in int_list:
            d.append(pow(block, priv, n))

    w = []
    for block in d:
        w.append(bin(block)[2::])

    new_w = []
    for block in w:
        while len(block) % 10 != 0:
            block = '0' + block
        new_w.append(block)

    res = ''
    for block in new_w:
        while len(block) != 0:
            res += chr(int(block[:10], 2))
            block = block[10:]

    res_2 = ''
    for letter in res:
        if letter != 'Ͽ':
            res_2 += letter

    return d, res_2


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = RSACipherGui()
    gui.show()

    try:
        sys.exit(app.exec())
    except:
        print("Successfully Exited")