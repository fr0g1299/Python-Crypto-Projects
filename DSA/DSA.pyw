# DSA Cipher
# fr0g1299


import re  # removes extra spaces
import sys  # exit
import os  # for .ui path
import datetime  # for date and time formating
import random  # for shuffle
import math  # for gcd
import hashlib  # for hashing
import base64  # for base64 encoding
import cv2  # for image and video file information
import numpy as np  # for cv2 image reading
import magic  # for file type
import mutagen  # for audio file information
import zipfile  # for zip file reading and writing

from PyQt5 import QtCore
from PyQt5.QtCore import QSequentialAnimationGroup
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

PUBL = ''  # Public key
PRIV = ''  # Private key
N = ''  # Modulus
HASH_ORIG = ''  # Original hash
ENC = ''  # Encrypted hash
HASH_SIGN = ''  # Signed hash
FNAME = ''  # Original file path

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
            "color: white;}")

# StyleSheet for .txt preview
browser_css = ("QTextBrowser {{\n"
	"border: 2px solid rgba(37, 39, 48, 255);\n"
	"border-radius: 20px;\n"
	"background-color: rgba(34, 36, 44, {back_color});\n"
	"font-size: 12px;\n"
	"padding-left: 10px;\n"
	"padding-right: 10px;\n"
	"color: rgba(230, 230, 230, {text_color});}}")

# StyleSheet for validation label
result_css = ("QLabel {{\n"
    "border: none;\n"
    "border-radius: 8px;\n"
    "background-color: rgba({back_color});\n"
    "color: rgba(255, 255, 255, {text_color});\n"
    "border-left: 2px solid rgba({border_color});\n"
    "border-right: 1px solid rgba({border_color});\n"
	"border-bottom: 2px solid rgba({border_color});}}")

# StyleSheet for buttons
btn_css = ("QPushButton {{\n"
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
	    "background-color: rgb(180, 0, 0);\n"
	    "border-left: 2px solid rgb(130, 0, 0);\n"
	    "border-right: 1px solid rgb(130, 0, 0);\n"
	    "border-bottom: 2px solid rgb(130, 0, 0);}}\n"
    "QPushButton:pressed {{{pre}}}")

press_css = "background-color: rgb(135, 0, 0);"\
	        "border: none;"\
	        "border-left: 1px solid rgb(110, 0, 0);"\
	        "border-right: 2px solid rgb(110, 0, 0);"\
	        "border-top: 2px solid rgb(110, 0, 0);",\
        "background-color: rgb(135, 0, 0);"\
        "border: none;"


inactive_style_out_browser = browser_css.format(back_color = "0", text_color = "0")
active_style_out_browser = browser_css.format(back_color = "225", text_color = "255")

invalid_style_out_res = result_css.format(back_color = "255, 0, 0, 255",
                                           border_color = "155, 0, 0, 255", text_color = "240")
valid_style_out_res = result_css.format(back_color = "0, 120, 0, 255",
                                         border_color = "0, 80, 0, 255", text_color = "240")
inactive_style_out_res = result_css.format(back_color = "0, 120, 0, 0",
                                            border_color = "0", text_color = "0")

inactive_style_btn = btn_css.format(back_color = "75, 0, 0", border_color = "55, 0, 0",
                                     text_color = "150, 160, 140", border = "12.4px", pre = press_css[0])
active_style_btn = btn_css.format(back_color = "150, 0, 0", border_color = "130, 0, 0",
                                   text_color = "206, 214, 196", border = "12.4px", pre = press_css[0])

inactive_style_btn_other = btn_css.format(back_color = "75, 0, 0", border_color = "55, 0, 0",
                                           text_color = "150, 160, 140", border = "5px", pre = press_css[1])
active_style_btn_other = btn_css.format(back_color = "150, 0, 0", border_color = "130, 0, 0",
                                         text_color = "206, 214, 196", border = "5px", pre = press_css[1])


class DSACipherGui(QDialog):

    def __init__(self):
        # Necessary stuff
        super().__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        form_class = os.path.join(ui_path, "DSACipherGui.ui")
        loadUi(form_class, self)
        self.setWindowTitle("DSA Cipher")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedHeight(594)
        self.setFixedWidth(1035)

        self.fadeQuick(self.lbl_sign)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_save)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_save_2)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_gen_keys)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_br_keys_s)  # Quickly fades, so the animation works later
        self.fadeQuick(self.lbl_br_keys_v)  # Quickly fades, so the animation works later

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Removes Default Window Frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes QDialog translucent

        self.btn_sign.clicked.connect(self.goToSign)  # Sign Button
        self.btn_ver.clicked.connect(self.goToVerify)  # Verify Button
        self.btn_res_s.clicked.connect(lambda: self.resetForm('Sign'))  # Resets Sign buttons and labels
        self.btn_res_v.clicked.connect(lambda: self.resetForm('Verify'))  # Resets Verify buttons and labels

        self.btn_min.clicked.connect(self.minimizeWindow)  # Enables minimize button
        self.btn_cls.clicked.connect(lambda: app.exit())  # Enables close button
        self.title_bar.mouseMoveEvent = self.moveWindow  # Enables Click&Drag on the window

        self.btn_browse.clicked.connect(self.getFile)  # Browse File Button, sign side
        self.btn_browse_zip.clicked.connect(self.getZip)  # Browse Zip File Button, verify side
        self.btn_browse_keys_s.clicked.connect(lambda: self.getKeys('Sign'))  # Browse Keys Button, sign side
        self.btn_browse_keys_v.clicked.connect(lambda: self.getKeys('Verify'))  # Browse Keys Button, verify side
        self.btn_gen_keys.clicked.connect(self.generateKeys)  # Generate Keys Button

        self.btn_save.clicked.connect(self.saveSignedFile)  # Save Button, saves signed (.zip) file
        self.btn_save_keys.clicked.connect(self.saveKeys)  # Save Button, saves keys

        # Shrink icons when pressed on small buttons
        self.btn_res_s.pressed.connect(lambda: self.resizeIcon('btn_res_s', True))
        self.btn_res_s.released.connect(lambda: self.resizeIcon('btn_res_s', False))
        self.btn_res_v.pressed.connect(lambda: self.resizeIcon('btn_res_v', True))
        self.btn_res_v.released.connect(lambda: self.resizeIcon('btn_res_v', False))
        self.btn_save.pressed.connect(lambda: self.resizeIcon('btn_save', True))
        self.btn_save.released.connect(lambda: self.resizeIcon('btn_save', False))
        self.btn_save_keys.pressed.connect(lambda: self.resizeIcon('btn_save_keys', True))
        self.btn_save_keys.released.connect(lambda: self.resizeIcon('btn_save_keys', False))
        
        # Shadow on the frameless window
        shadow_window = QGraphicsDropShadowEffect()
        shadow_window.setBlurRadius(5)
        shadow_window.setOffset(3)
        shadow_window.setColor(QColor(50, 50, 50, 160))
        self.bgwidget.setGraphicsEffect(shadow_window)

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

    def resizeIcon(self, btn, chk):
        """
        Resizes the icon of a button based on the given parameters.

        Parameters:
        btn (str): The name of the button.
        chk (bool): A flag indicating whether the icon should shrink (True), or return to default size (False).
        """

        icon_sizes = {
            'btn_res_s': (19, 19) if chk else (22, 22),
            'btn_res_v': (19, 19) if chk else (22, 22),
            'btn_save': (16, 16) if chk else (19, 19),
            'btn_save_keys': (16, 16) if chk else (19, 19)}
        
        btn_dict = { 'btn_res_s': self.btn_res_s,
                     'btn_res_v': self.btn_res_v,
                     'btn_save': self.btn_save,
                     'btn_save_keys': self.btn_save_keys}
        try:
            if btn in icon_sizes:
                btn_dict[btn].setIconSize(QtCore.QSize(*icon_sizes[btn]))
        except:
            pass

    def generateKeys(self):
        """
        Generates public and private keys for DSA encryption.

        Returns:
            None
        """

        global PUBL, PRIV, N
        publ, priv = generate_keys()
        publ_str = str(publ[1])
        priv_str = str(priv[1])
        n_str = str(publ[0])
        PRIV = priv_str
        PUBL = publ_str
        N = n_str

        # This is just for the preview of the public key
        publ_str = publ_str + ' ' + n_str
        sample_string_bytes = publ_str.encode("ascii") 
        base64_bytes = base64.b64encode(sample_string_bytes) 
        base64_string = base64_bytes.decode("ascii") 
        self.lbl_publ_s.setText('Public Key\n' + "\u200b".join(base64_string))

        # This is just for the preview of the private key
        priv_str = priv_str + ' ' + n_str
        sample_string_bytes = priv_str.encode("ascii") 
        base64_bytes = base64.b64encode(sample_string_bytes) 
        base64_string = base64_bytes.decode("ascii") 
        self.lbl_priv_s.setText('Private Key\n' + "\u200b".join(base64_string))

        # Enable the `Save Keys` button
        self.btn_save_keys.setEnabled(True)
        self.btn_save_keys.setStyleSheet(active_style_btn_other)
        # Enable the sign button if the file is already selected
        if FNAME:
            self.btn_sign.setEnabled(True)
            self.btn_sign.setStyleSheet(active_style_btn)

        self.fade(self.lbl_gen_keys)

    def getKeys(self, chk):
        """
        Retrieves the public and private keys from a selected directory.

        Args:
            chk (str): The type of operation to perform ('Sign' or 'Verify').

        Returns:
            int: Returns 0 if the keys are not found or an error occurs.
        """

        path = os.path.dirname(os.path.abspath(__file__))  # Gets the current directory
        # Opens the file dialog, default directory is `path`
        folder = QFileDialog.getExistingDirectory(self, "Select a Directory where the keys are located", str(path))  

        if not folder:
            return 0
            
        try:
            # If the public key is not found, create an empty string
            with open(folder + '\\Public_key.pub', 'rb') as f:
                publ = f.read()
        except:
            publ = ''

        try:
            # If the private key is not found, create an empty string
            with open(folder + '\\Private_key.priv', 'rb') as f:
                priv = f.read()
        except:
            priv = ''

        # If the private key was not found and we are signing the file, display a message box
        if not priv and chk == 'Sign':
            self.showInformationMessageBox(2)
            return 0
        
        # If the public key was not found and we are verifying the file, display a message box
        if not publ and chk == 'Verify':
            self.showInformationMessageBox(3)
            return 0

        global PUBL, PRIV, N
        try:
            # If the public key was found, decode it and get the modulus and public key
            if publ:
                publ = publ.split(b' ')[1]
                publ = publ.decode("ascii")
                tmp_publ = publ
                publ = base64.b64decode(publ)
                publ = publ.decode("ascii")
                n = publ.split(' ')[1]
                PUBL = publ.split(' ')[0]
                N = n
                tmp_1 = n
            else:
                tmp_1 = 'None'

            # If the private key was found, decode it and get the modulus and private key
            if priv:
                priv = priv.split(b' ')[1]
                priv = priv.decode("ascii")
                tmp_priv = priv
                priv = base64.b64decode(priv)
                priv = priv.decode("ascii")
                n = priv.split(' ')[1]
                PRIV = priv.split(' ')[0]
                N = n
                tmp_2 = n
            else:
                tmp_2 = 'None'
        except:
            self.showInformationMessageBox(7)
            return 0

        # If the modulus of the public and private key are not the same, display a message box and continue
        if tmp_1 != tmp_2 and tmp_1 != 'None' and tmp_2 != 'None':
            self.showInformationMessageBox(6)

        # Fade labels
        if chk == 'Sign':
            self.fade(self.lbl_br_keys_s)
        elif chk == 'Verify':
            self.fade(self.lbl_br_keys_v)

        # Show keys and if the file is already selected, enable the Sign button
        if chk == 'Sign':
            self.lbl_priv_s.setText('Private Key\n' + "\u200b".join(tmp_priv))
            try:
                self.lbl_publ_s.setText('Public Key\n' + "\u200b".join(tmp_publ))
            except:
                pass
            if FNAME:
                self.btn_save.setEnabled(True)
                self.btn_save.setStyleSheet(active_style_btn_other)
        # Show keys and if the file is already selected, enable the Verify button
        elif chk == 'Verify':
            self.lbl_publ_v.setText('Public Key\n' + "\u200b".join(tmp_publ))
            try:
                self.lbl_priv_v.setText('Private Key\n' + "\u200b".join(tmp_priv))
            except:
                pass
            if HASH_ORIG and HASH_SIGN:
                self.btn_ver.setEnabled(True)
                self.btn_ver.setStyleSheet(active_style_btn)

    def getZip(self):
        """
        Opens a file dialog to select a zip file.
        Reads the contents of the zip file.
        Gets original hash and signed hash.
        If keys are already stored, the Verify button is enabled.

        Returns:
            int: Returns 0 if no file is selected (User pressed `Esc` on the Dialog option).
        """

        # Gets the current directory
        path = os.path.dirname(os.path.abspath(__file__))
        # Opens the file dialog, default directory is `path`
        fname = QFileDialog.getOpenFileName(self, 'Open Zip file', str(path), self.tr('Zip files (*.zip)'))[0]

        if not fname:
            return 0
        
        s = os.stat(fname).st_size
        # Reads the contents of the zip file
        variable_data = b''
        i = 0
        with zipfile.ZipFile(fname, 'r') as zip_file:
            file_list = zip_file.namelist()
            info_list = zip_file.infolist()
            sign_file = None
            variable_file = None

            # Checks if the zip file contains only 2 files
            if len(file_list) != 2:
                self.showInformationMessageBox(1)
                return 0

            for file_name in file_list:
                if file_name.endswith('.sign'):
                    sign_file = file_name
                else:
                    variable_file = file_name

            # Reads the .sign file, if its not found, displays a message box
            if sign_file is not None:
                with zip_file.open(sign_file) as f:
                    sign_data = f.read()
            else:
                self.showInformationMessageBox(4)
                return 0

            self.progressBar_v.setFormat('%p%')
            self.progressBar_v.setTextVisible(True)

            # Reads the original file, if its not found, displays a message box
            if variable_file is not None:
                with zip_file.open(variable_file) as f:
                    if s >= 1000000000:  # If the file is bigger than 1000MB, read chunks with buffer size of 100MB
                        while chunk := f.read(102760448):
                            variable_data += chunk
                            i += len(chunk)
                            progress = int((i / s) * 100)
                            self.progressBar_v.setValue(progress)
                    elif s >= 100000000:  # If the file is bigger than 100MB, read chunks with buffer size of 13MB
                        while chunk := f.read(13107200):
                            variable_data += chunk
                            i += len(chunk)
                            progress = int((i / s) * 100)
                            self.progressBar_v.setValue(progress)
                    elif s <= 100000000:  # If the file is smaller than 100MB, read chunks with buffer size of 65KB
                        while chunk := f.read(65536):
                            variable_data += chunk
                            i += len(chunk)
                            progress = int((i / s) * 100)
                            self.progressBar_v.setValue(progress)
                        
            else:
                self.showInformationMessageBox(5)
                return 0

        self.progressBar_v.setValue(100)
        self.progressBar_v.setFormat('Done!')
        # Updates labels about the Zip file information
        self.updateFileInfo(fname, True, info_list)
                    
        # Gets the hash of the original file
        sha3_512 = hashlib.sha3_512()
        sha3_512.update(variable_data)
        hash_value = sha3_512.hexdigest()

        # Gets the signed hash from .sign file
        hash = sign_data.split(b' ')[1]
        hash = hash.decode("ascii")

        # Enable the Verify button if the public key is already picked from GUI (on the verify side)
        try:
            global HASH_SIGN, HASH_ORIG
            HASH_SIGN = hash
            HASH_ORIG = hash_value

            if PUBL:
                self.btn_ver.setEnabled(True)
                self.btn_ver.setStyleSheet(active_style_btn)

        except Exception as error:
            self.showCriticalMessageBox(error)


    def getFile(self):
        """
        Opens a file dialog to select a file and updates the labels with file information.
        If a file is selected, it enables the Sign button and displays the private and public keys.

        Returns:
            int: Returns 0 if no file is selected (User pressed `Esc` on the Dialog option).
        """

        path = os.path.dirname(os.path.abspath(__file__))
        fname = QFileDialog.getOpenFileName(self, 'Open file', str(path), self.tr('All files (*.*);;'))[0]
            
        if not fname:
            return 0
        
        # Update labels about the file information
        self.updateFileInfo(fname)

        # Enable the Sign button if the file is selected from the GUI (on the sign side)
        try:
            global HASH_ORIG, FNAME
            HASH_ORIG = hashSha512(fname, self)
            FNAME = fname

            if PRIV:
                self.btn_sign.setEnabled(True)
                self.btn_sign.setStyleSheet(active_style_btn)

        except Exception as error:
            self.showCriticalMessageBox(error)

    def updateFileInfo(self, fname, chk=False, info_list=[]):
        """
        Update the file information labels based on the given file type.

        Parameters:
        - fname (str): The path to the file.
        - chk (bool): Optional. Indicates whether the file is a zip file and additional information is provided.
        - info_list (list): Optional. A list of additional information about the files in the zip file.
        """

        # Reset all labels, disable text browser and result label
        self.lbl_created.setText('Created: ')
        self.lbl_modified.setText('Modified: ')
        self.lbl_siz.setText('Size: ')
        self.lbl_ext.setText('File type: ')
        self.lbl_loc.setText('Location: ')

        self.lbl_bit_dim.setText('')
        self.lbl_pix_fps.setText('')
        self.lbl_len_res.setText('')
        self.lbl_art.setText('')
        self.lbl_alb.setText('')

        self.textBrowser.setEnabled(False)
        self.textBrowser.setStyleSheet(inactive_style_out_browser)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.lbl_result.setEnabled(False)
        self.lbl_result.setStyleSheet(inactive_style_out_res)

        self.lbl_len_res.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_pix_fps.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_bit_dim.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_art.setAlignment(QtCore.Qt.AlignLeft)

        # Get file type, example: [PNG File]
        file_type = magic.from_buffer(open(fname, "rb").read(2048))
        # Get file type with mime, example: [image]
        ext_type = magic.from_buffer((open(fname, "rb").read(2048)), mime=True)
        # Get file extension, example: [.png]
        ext = os.path.splitext(fname)[1]

        if ext_type != None and file_type != None:
            file_type = file_type.split(',')[0]
            ext_type = ext_type.split('/')[0]

        # Update labels about the files information
        self.lbl_loc.setText(f'Location: {fname}')

        create_date = datetime.datetime.fromtimestamp(os.path.getctime(fname))
        create_date = create_date.strftime('%d.%m.%Y  %H:%M:%S')
        self.lbl_created.setText(f'Created: {create_date}')

        modify_date = datetime.datetime.fromtimestamp(os.path.getmtime(fname))
        modify_date= modify_date.strftime('%d.%m.%Y  %H:%M:%S')
        self.lbl_modified.setText(f'Modified: {modify_date}')

        s = human_size(os.stat(fname).st_size)
        self.lbl_siz.setText(f'Size: {s}')
        self.lbl_ext.setText(f'File type: {file_type} ({ext})')   

        # Update labels based on the file type
        if ext_type == 'image':
            img = cv2.imdecode(np.fromfile(fname, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            h, w, _ = img.shape
            pix = h * w
            pix_f = format(pix, ',d').replace(',',' ')
            
            self.lbl_len_res.setText(f'Resolution: {w}x{h}')
            self.lbl_pix_fps.setText(f'Pixels: {pix_f} px')

        elif ext_type == 'video':
            vid = cv2.VideoCapture(fname)
            fps = int(vid.get(cv2.CAP_PROP_FPS))
            h = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            w = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = int((frame_count / fps))

            self.lbl_len_res.setText(f'Length: {str(datetime.timedelta(seconds=duration))}')
            self.lbl_bit_dim.setText(f'Dimensions: {w}x{h}')
            self.lbl_pix_fps.setText(f'Frame rate: {fps} frames/second')
            vid.release()
            cv2.destroyAllWindows()

        elif ext_type == 'audio' or ext == '.mp3':
            audio = mutagen.File(fname, easy=True)
            duration = audio.info.length
            self.lbl_len_res.setText(f'Length: {str(datetime.timedelta(seconds=duration))[:-7]}')
            try:
                self.lbl_bit_dim.setText(f'Bitrate: {int(audio.info.bitrate / 1000)} kbps')
                self.lbl_pix_fps.setText(f'Sample rate: {audio.info.sample_rate} Hz')
                self.lbl_art.setText(f'Artist - Title: {audio["artist"][0]} - {audio["title"][0]}')
                self.lbl_alb.setText(f'Album: {audio["album"][0]}')
            except:
                pass

        elif ext_type == 'text':
            self.textBrowser.setEnabled(True)
            self.textBrowser.setStyleSheet(active_style_out_browser)
            self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            try:
                text = ''
                with open(fname, 'r', encoding='utf-8') as f:
                    while chunk := f.read(6000):
                        text += chunk
                        if len(text) >= 12000:
                            text = 'Preview of first 12000 characters...\n\n' + text
                            break
                self.textBrowser.setText(text)
            except:
                self.textBrowser.setText('File is too big to preview or has unexpected characters...')
            
        # This is executed only when the user clicks on the `Browse Zip` button
        elif ext == '.zip' and chk:
            self.lbl_len_res.setAlignment(QtCore.Qt.AlignHCenter)
            self.lbl_pix_fps.setAlignment(QtCore.Qt.AlignHCenter)
            self.lbl_bit_dim.setAlignment(QtCore.Qt.AlignHCenter)
            self.lbl_art.setAlignment(QtCore.Qt.AlignHCenter)

            self.lbl_len_res.setText(f'Original File:  {info_list[0].filename}  -  {human_size(info_list[0].file_size)}')
            self.lbl_pix_fps.setText(f'Modified:  {datetime.datetime(*info_list[0].date_time).strftime('%d.%m.%Y  %H:%M:%S')}')
            self.lbl_bit_dim.setText(f'Signed File:  {info_list[1].filename}  -  {human_size(info_list[1].file_size)}')
            self.lbl_art.setText(f'Modified:  {datetime.datetime(*info_list[1].date_time).strftime('%d.%m.%Y  %H:%M:%S')}')
        else:
            pass

    def saveKeys(self):
        """
        Saves the public and private keys to files.

        If any exception occurs during the process, a critical message box is displayed with the error message.
        """

        try:
            publ = PUBL
            priv = PRIV
            n = N

            # Convert public key to base64 format
            publ = str(publ) + ' ' + str(n)
            sample_string_bytes = publ.encode("ascii") 
            base64_bytes = base64.b64encode(sample_string_bytes) 
            base64_string = base64_bytes.decode("ascii") 
            publ = 'RSA ' + base64_string

            # Convert private key to base64 format
            priv = str(priv) + ' ' + str(n)
            sample_string_bytes = priv.encode("ascii") 
            base64_bytes = base64.b64encode(sample_string_bytes) 
            base64_string = base64_bytes.decode("ascii") 
            priv = 'RSA ' + base64_string

            # Get the directory where to save the keys
            folder = self.whereToSave()
            if not folder:
                return 0
            
            # Save public key to file
            with open(folder + '\\Public_key.pub', 'wb') as f:
                f.write(publ.encode())

            # Save public key to file
            with open(folder + '\\Private_key.priv', 'wb') as f:
                f.write(priv.encode())

            self.fade(self.lbl_save_2)  # Fades in the label

        except Exception as error:
            self.showCriticalMessageBox(error)

    def whereToSave(self):
        """
        Opens a file dialog to select a directory for saving.

        Returns:
            str: The selected directory path.
        """

        # Gets the current directory
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            # Opens the file dialog, default directory is `path`
            folder = QFileDialog.getExistingDirectory(self, "Select Directory", str(path))
            return folder
        except Exception as error:
            self.showCriticalMessageBox(error)
        
    def saveSignedFile(self):
        """
        Saves the file by creating a zip archive and adding the
        original file and its hash to the archive.

        Returns:
            int: If something goes wrong, nothing happens and returns 0.
        """

        try:
            hash = ENC.encode()
            folder_path = self.whereToSave()

            if not folder_path:
                return 0
            
            fname = FNAME
            # Create the zip file
            with zipfile.ZipFile(folder_path + '/signed_file.zip', mode='w') as zf:
                # Add the original file to the zip
                zf.write(fname, arcname=os.path.basename(fname), compress_type=zipfile.ZIP_DEFLATED)
                # Add the .sign file to the zip
                zf.writestr('signed.sign', hash)
                
            self.fade(self.lbl_save)  # Fades in the label
        except Exception as error:
            self.showCriticalMessageBox(error)

    def goToSign(self):
        """
        This method is used to sign a file using a private key and hash.

        Retrieves the private key, modulus, and original hash.
        Calls the `sign_file` function to sign the file.
        Fades the `lbl_sign` label.

        If any exception occurs during the process, a critical message box is displayed with the error message.
        """
        try:
            priv = PRIV
            n = N
            hash = HASH_ORIG
            global ENC
            ENC = sign_file(hash, priv, n)

            self.btn_save.setEnabled(True)
            self.btn_save.setStyleSheet(active_style_btn_other)

            self.fade(self.lbl_sign)
        except Exception as error:
            self.showCriticalMessageBox(error)

    def goToVerify(self):
        """
        Decrypts the hash and verifies the signature.

        This method decrypts the original hash using the provided public key and modulus.
        It then verifies the decrypted hash against the signed hash using the verify_signature function.
        The decrypted and signed hashes are displayed in the GUI labels.
        If the signature is valid, the result label is enabled and set to 'Signature is valid'.
        If the signature is invalid, the result label is enabled and set to 'Signature is invalid'.
        If an exception occurs during the decryption or verification process, a critical message box is shown.
        """
        try:
            hash_orig = HASH_ORIG
            hash_sign = HASH_SIGN
            publ = PUBL
            n = N
            self.lbl_hash_orig.setEnabled(True)
            self.lbl_hash_sign.setEnabled(True)

            ver, hash_sign = verify_signature(hash_orig, hash_sign, publ, n)
            self.lbl_hash_orig.setText('Original hash: ' + "\u200b".join(hash_orig))

            if len(hash_sign) > 130:
                hash_sign = hash_sign[:130] + '...'

            self.lbl_hash_sign.setText('Signed hash: ' + "\u200b".join(hash_sign))
            if ver:
                self.lbl_result.setEnabled(True)
                self.lbl_result.setStyleSheet(valid_style_out_res)
                
                self.lbl_result.setText('Signature is valid')
            else:
                self.lbl_result.setEnabled(True)
                self.lbl_result.setStyleSheet(invalid_style_out_res)

                self.lbl_result.setText('Signature is invalid')
        except Exception as error:
            self.showCriticalMessageBox(error)

    def showCriticalMessageBox(self, error):
        '''Shows message box with error.'''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)

        msg.setWindowTitle("Error")
        msg.setWindowIcon(QIcon('icon.png'))
        msg.setText(f"An error occurred: {error}")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def showInformationMessageBox(self, chk = 1):
        '''Shows message box with information.'''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setFixedWidth(120)
        msg.setFixedHeight(50)

        msg.setStyleSheet(msg_box_css)

        msg.setWindowTitle("Information")
        msg.setWindowIcon(QIcon('icon.png'))
        match chk:
            case 1:
                msg.setText("Zip file contains only 1 file or more than 2.\n"
                            "It should only have the original file and the .sign file...")
            case 2:
                msg.setText("Private key (.priv) not found in the directory...")
            case 3:
                msg.setText("Public key (.pub) not found in the directory...")
            case 4:
                msg.setText("Signed (.sign) file not located in the zip...")
            case 5:
                msg.setText("Original file not located in the zip...")
            case 6:
                msg.setText("Public and private key have different modulus (n)...")
            case 7:
                msg.setText("Keys are not in the correct format...")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def resetForm(self, chk):
        """
        Resets all visible labels.
        Disables buttons and changes their color.

        Args:
            chk (str): The type of side to reset ('Sign' or 'Verify').
        """
        self.lbl_created.setText('Created: ')
        self.lbl_modified.setText('Modified: ')
        self.lbl_siz.setText('Size: ')
        self.lbl_ext.setText('File type: ')
        self.lbl_loc.setText('Location: ')

        self.lbl_bit_dim.setText('')
        self.lbl_pix_fps.setText('')
        self.lbl_len_res.setText('')
        self.lbl_art.setText('')
        self.lbl_alb.setText('')

        self.textBrowser.setEnabled(False)
        self.textBrowser.setStyleSheet(inactive_style_out_browser)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.lbl_len_res.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_pix_fps.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_bit_dim.setAlignment(QtCore.Qt.AlignLeft)
        self.lbl_art.setAlignment(QtCore.Qt.AlignLeft)

        global PUBL, PRIV, HASH_ORIG, ENC, HASH_SIGN, FNAME
        if chk == 'Sign':
            PRIV = ''
            PUBL = ''
            HASH_ORIG = ''
            ENC = ''
            FNAME = ''
            self.lbl_publ_s.setText('Public Key')
            self.lbl_priv_s.setText('Private Key')
            self.btn_sign.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_save_keys.setEnabled(False)
            self.btn_sign.setStyleSheet(inactive_style_btn)
            self.btn_save.setStyleSheet(inactive_style_btn_other)
            self.btn_save_keys.setStyleSheet(inactive_style_btn_other)
            self.progressBar_s.setTextVisible(False)
            self.progressBar_s.setValue(0)

        elif chk == 'Verify':
            PUBL = ''
            PRIV = ''
            HASH_ORIG = ''
            ENC = ''
            HASH_SIGN = ''
            FNAME = ''
            self.lbl_hash_orig.setText('')
            self.lbl_hash_sign.setText('')
            self.btn_ver.setEnabled(False)
            self.btn_ver.setStyleSheet(inactive_style_btn)
            self.lbl_hash_orig.setEnabled(False)
            self.lbl_hash_sign.setEnabled(False)
            self.lbl_result.setEnabled(False)
            self.lbl_result.setStyleSheet(inactive_style_out_res)
            self.lbl_publ_v.setText('Public Key')
            self.lbl_priv_v.setText('Private Key')
            self.progressBar_v.setTextVisible(False)
            self.progressBar_v.setValue(0)

    def fade(self, widget):
        '''Fades in/out the labels.'''
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
            case self.lbl_sign:
                self.anim_group = QSequentialAnimationGroup()
                self.anim_group.addAnimation(self.anim)
                self.anim_group.addPause(2000)
                self.anim_group.addAnimation(self.anim_2)
                self.anim_group.start()
            case self.lbl_gen_keys:
                self.anim_group_2 = QSequentialAnimationGroup()
                self.anim_group_2.addAnimation(self.anim)
                self.anim_group_2.addPause(2000)
                self.anim_group_2.addAnimation(self.anim_2)
                self.anim_group_2.start()
            case self.lbl_save:
                self.anim_group_3 = QSequentialAnimationGroup()
                self.anim_group_3.addAnimation(self.anim)
                self.anim_group_3.addPause(2000)
                self.anim_group_3.addAnimation(self.anim_2)
                self.anim_group_3.start()
            case self.lbl_save_2:
                self.anim_group_4 = QSequentialAnimationGroup()
                self.anim_group_4.addAnimation(self.anim)
                self.anim_group_4.addPause(2000)
                self.anim_group_4.addAnimation(self.anim_2)
                self.anim_group_4.start()
            case self.lbl_br_keys_s:
                self.anim_group_5 = QSequentialAnimationGroup()
                self.anim_group_5.addAnimation(self.anim)
                self.anim_group_5.addPause(2000)
                self.anim_group_5.addAnimation(self.anim_2)
                self.anim_group_5.start()
            case self.lbl_br_keys_v:
                self.anim_group_6 = QSequentialAnimationGroup()
                self.anim_group_6.addAnimation(self.anim)
                self.anim_group_6.addPause(2000)
                self.anim_group_6.addAnimation(self.anim_2)
                self.anim_group_6.start()

    def fadeQuick(self, widget):
        '''Instantly fades, so the animation works later.'''
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(0)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()


def generate_keys():
    """
    Generates a pair of public and private keys for encryption and decryption.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple containing the public key (n, e) and the private key (n, d).
    """
 
    # Generate two random prime numbers
    p = generate_coprime_prime()
    while True:
        q = generate_coprime_prime()
        if p != q:
            break

    n = p * q  # Calculate modulus
    eu = (p - 1) * (q - 1)  # Calculate Euler's totient function

    # Generate a random public key
    while True:
        e = random.randint(2, eu - 1)
        if e < eu and math.gcd(e, eu) == 1 and (22 <= len(str(e)) <= 24):
            break

    # Generate a private key
    d = pow(e, -1, eu)

    return (n, e), (n, d)


def generate_coprime_prime():
    """
    Generates a random prime number that is coprime with 10^11.

    Returns:
        int: A prime number that is coprime with 10^11 and its length is 12.
    """

    while True:
        num = random.randint(10**11, 10**12 - 1)
        if math.gcd(num, 10**11) == 1:
            # Check if the number is prime
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    break
            else:
                return num


def generate_msg(txt):
    """
    Generate a list of decimal values representing the ASCII codes of characters in the input text.

    Args:
        txt (str): The input text.

    Returns:
        list: A list of decimal values.
    """

    prep_str = txt.strip()
    prep_str = re.sub(r'\s+', ' ', prep_str, flags=re.UNICODE)

    # If the message was only spaces, return an empty string
    if prep_str == '' or prep_str == ' ':
        return ''

    # Split the message into blocks of 6 characters
    prep_split = []
    while True:
        prep_split.append(prep_str[:6])
        prep_str = prep_str[6:]
        if len(prep_str) == 0:
            break

    # Add 'Ͽ' characters to the last block if it is shorter than 6 characters
    tmp = ''
    if len(str(prep_split[-1])) != 6:
        tmp += prep_split[-1]
        tmp += 'Ͽ' * (6 - len(str(prep_split[-1])))
        prep_split[-1] = tmp

    # Convert each block to binary and add leading zeros
    binary_data = []
    for block in prep_split:
        tmp = ''
        for char in block:
            ascii_value = ord(char)
            # Skip characters with ASCII values greater than 1023
            if ascii_value <= 1023:
                tmp += format(ascii_value, "010b")
        binary_data.append(tmp)

    # Convert each block to decimal
    msg_dec = []
    for block in binary_data:
        msg_dec.append(int(block, 2))

    return msg_dec


def encrypt(msg, priv, n):
    """
    Encrypts a message using the RSA encryption algorithm.

    Parameters:
    msg (list): The message to be encrypted, represented as a list of integers.
    priv (int): The private key for encryption.
    n (int): The modulus for encryption.

    Returns:
    str: The encrypted message as a string.
    """

    # Encrypt each block    
    enc = []
    for block in msg:
        enc.append(pow(block, priv, n))

    # Add leading zeros to each block
    res_fin = [str(block).zfill(24) for block in enc]

    res_fin = ''.join(res_fin)  # Convert list to string
    res_fin = ' '.join(res_fin[i:i+6] for i in range(0,len(res_fin),6))  # Insert spaces every 6 characters
    
    return res_fin


def decrypt(msg, publ, n):
    """
    Decrypts a message using the public key and modulus.

    Args:
        msg (str): The encrypted message to be decrypted.
        publ (int): The public key.
        n (int): The modulus.

    Returns:
        str: The decrypted message.
    """
        
    msg_split = [msg[i:i + 24] for i in range(0, len(msg), 24)]  # Split the message into blocks of 24 characters
    int_list = [int(x) for x in msg_split]  # Convert each block to an integer

    # Decrypt each block
    dec = []
    for block in int_list:
        dec.append(pow(block, publ, n))

    # Convert each block to binary
    w = []
    for block in dec:
        w.append(bin(block)[2::])

    # Add leading zeros to each block
    new_w = []
    for block in w:
        while len(block) % 10 != 0:
            block = '0' + block
        new_w.append(block)


    # Convert binary to ASCII
    res = ''
    for block in new_w:
        while len(block) != 0:
            res += chr(int(block[:10], 2))
            block = block[10:]

    # Iterate thru 'res' and remove all 'Ͽ' characters
    res_fin = ''
    res_fin = res_fin.join([letter for letter in res if letter != 'Ͽ'])

    return res_fin


def sign_file(hash, private_key, n):
    """
    Sign a file using RSA_SHA3-512 encryption.

    Args:
        hash (str): The hash of the file.
        private_key (int): The private key for encryption.
        n (int): The modulus for encryption.

    Returns:
        str: The signed file in the format "RSA_SHA3-512 <base64_encoded_encryption>".
    """
    
    # Transform the hash into a list of decimal values
    hash = generate_msg(hash)

    # If the message was only spaces, return an empty string
    if hash == '':
        return ''

    enc = encrypt(hash, int(private_key), int(n))

    # Encode the encrypted message to base64
    enc_string_bytes = enc.encode("ascii")
    base64_bytes = base64.b64encode(enc_string_bytes)
    base64_string = 'RSA_SHA3-512 ' + base64_bytes.decode("ascii")

    return base64_string


def verify_signature(base64_string, signature, public_key, n):
    """
    Verifies the signature of a base64 encoded string using DSA encryption.

    Args:
        base64_string (str): The base64 encoded string to verify.
        signature (str): The signature to verify.
        public_key (str): The public key used for decryption.
        n (str): The modulus used for decryption.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """

    # Decode the base64 string
    sign = signature.encode("ascii")
    sign = base64.b64decode(sign)
    sign = sign.decode("ascii")

    # Remove all whitespaces from the signature
    sign = re.sub(r'\s+', '', sign, flags=re.UNICODE)

    dec = decrypt(sign, int(public_key), int(n))

    return bool(dec == base64_string), dec


def hashSha512(fname, obj):
    '''Generates SHA3-512 hash value of a file.'''

    s = os.stat(fname).st_size
    i = 0
    obj.progressBar_s.setTextVisible(True)
    obj.progressBar_s.setFormat('%p%')

    with open(fname, 'rb') as f:
        sha3_512 = hashlib.sha3_512()
        if s >= 1000000000:  # If the file is bigger than 1000MB, read chunks with buffer size of 13MB
            while chunk := f.read(13107200):
                sha3_512.update(chunk)
                i += len(chunk)
                progress = int((i / s) * 100)
                obj.progressBar_s.setValue(progress)
        elif s >= 100000000:  # If the file is bigger than 100MB, read chunks with buffer size of 3MB
            while chunk := f.read(3276800):
                sha3_512.update(chunk)
                i += len(chunk)
                progress = int((i / s) * 100)
                obj.progressBar_s.setValue(progress)
        elif s <= 100000000:  # If the file is smaller than 100MB, read chunks with buffer size of 65KB
            while chunk := f.read(65536):
                sha3_512.update(chunk)
                i += len(chunk)
                progress = int((i / s) * 100)

    obj.progressBar_s.setValue(100)
    obj.progressBar_s.setFormat('Done!')
    hash_value = sha3_512.hexdigest()
    
    return hash_value


def human_size(num: int) -> str:
    """
    Converts a number representing a file size in bytes to a human-readable format.

    Args:
        num (int): The number representing the file size in bytes.

    Returns:
        str: The human-readable file size.

    """

    base = 1
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        n = num / base
        if n < 9.95 and unit != 'B':
            # Less than 10 then keep 2 decimal places
            value = "{:.2f} {}".format(n, unit)
            return value
        if round(n) < 1000:
            # Less than 4 digits
            value = "{} {}".format(round(n), unit)
            return value
        base *= 1024
    value = "{} {}".format(round(n), unit)

    return value


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = DSACipherGui()
    gui.show()

    try:
        sys.exit(app.exec())
    except:
        print("Successfully Exited")