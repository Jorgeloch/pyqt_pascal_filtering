from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from AP03 import Ui_MainWindow
from pascal import piramidePascal
import numpy as np 
from scipy.signal import convolve2d
import sys
import cv2 

class MainWindow (QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow,self).__init__ (*args, **kwargs)
        self.setupUi (self)
        self.setWindowTitle ("Box Filter")
        self.cap = cv2.VideoCapture(0) # objeto que representa a webcam    
        self.timer = QTimer() # objeto que representa um cronometro
        self.timer.timeout.connect (self.processar_frame) # ligacao dos disparos do cronometro a uma funcao em Python
        self.timer.start (50) # start do cronometro com disparos regulares a cada 50 ms
        self.mascaras = piramidePascal(39) # pre-computando as linhas do triangulo de pascal para usarmos posteriormente 

    def processar_frame(self):
        ret, frame = self.cap.read() # leitura de um frame do video
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # transforma a imagem colorida em uma imagem em grayscale
        filtered_image = np.zeros_like(gray_frame).astype('uint8') # criando imagem onde será armazenada a imagem filtrada

        mask_size =  self.filterSize.value() # definindo o tamanho da mascara a ser utilizada

        if(mask_size % 2 == 0):
            mask_size += 1 # determinando que todas as mascaras aplicadas serão de tamanho impar
            self.filterSize.setValue(mask_size) # alterando o valor dentro da GUI

        mask = ((1/2) ** (mask_size - 1))*np.array(self.mascaras[mask_size - 1]).reshape(1,mask_size) # definindo a mascara a ser utilizada a partir
                                                                                                      # da piramide de pascal pre computada
        crop_size = mask_size//2 # definindo tamanho a ser cortado da imagem após convolução

        if (self.filtragem1D.isChecked()):
            # filtragem 1D, quando for verificado que o tipo de filtragem selecionado é a filtragem 1D

            # filtragem das colunas
            filtered_image = convolve2d(gray_frame, mask)
            filtered_image = filtered_image[:,crop_size:-crop_size]

            # filtragem das linhas
            filtered_image = convolve2d(gray_frame, mask.T)
            filtered_image = filtered_image[crop_size:-crop_size, :]

            filtered_image = filtered_image.astype('uint8')

        elif (self.filtragem2D.isChecked()):    
            # filtragem 2D, quando for verificado que o tipo de filtragem selecionado é a filtragem 2D
            mask2D = convolve2d(mask, mask.T) # criação da máscara bi-dimensional

            filtered_image = convolve2d(gray_frame, mask2D)
            filtered_image = filtered_image[crop_size:-crop_size, crop_size:-crop_size]

            filtered_image = filtered_image.astype('uint8')

        else:
            filtered_image += gray_frame

        pixmap = self.convert_cv_qt (filtered_image) # conversao de uma imagem do opencv para o formato qt
        self.label.setPixmap (pixmap) # atribuicao do novo valor do pixmap do label

    def convert_cv_qt(self, cv_img): # funcao usada para converter opencv para qt
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(convert_to_Qt_format)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()
