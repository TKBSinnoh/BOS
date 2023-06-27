# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:13:02 2023

@author: Master
"""

import cv2 as cv
import numpy as np
import os.path as path

class video:
    
    def __init__(self,diretorio_input):
        
        if not path.isfile(diretorio_input):
            raise Exception("Caminho não é um arquivo")            
        
        self.cap = cv.VideoCapture(diretorio_input)	
        self.width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
        self.height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count/self.fps
        self.crop = [0,0]
        self.resize = [1,1]
        self.contrast = 50
        self.brightness = 6
        self.filtro = None
        self.filtro_code = None
        self.color = None
        self.alpha = 0.5	
        self.ret = 0
        self.img = 0
        self.background_fixo = 0
        self.background_variado = 0
        
    # def crop_coeff(self,crop_height, crop_width, crop_cx, crop_cy):
    #     self.crop[0] = crop_cx
    #     self.crop[1] = crop_cy
    #     if crop_height > 0:
    #         self.height = crop_height
    #     else:
    #         self.crop[1] = -1                   #ARRUMAR ERRO DE CROP
    #     if crop_width > 0:
    #         self.width = crop_width
    #     else:
    #         self.crop[0] = -1
        
    #     return;
    
    def resize_coeff(self, altura_imagem, comprimento_imagem,n_image):
        
        if n_image == 1:
            n_i = 1
            n_j = 1
        elif n_image < 3:
            n_i = 2
            n_j = 1
        elif n_image < 5:
            n_i = 2
            n_j = 2
        elif n_image < 9:
            n_i = 4
            n_j = 2
        else:
            n_i = 4
            n_j = 3
            
        rc_h = altura_imagem /self.height 
        rc_w = comprimento_imagem /self.width
        self.height = int(self.height * rc_h)
        self.width  = int(self.width  * rc_w)
        self.resize[0] = rc_h/ n_j
        self.resize[1] = rc_w/ n_i
        
        return;
    
    def brilho(self,CON,BRI):
        self.contrast = CON
        self.brightness = BRI
        return;
    
    def apply_filter(self,filtro_code):
        
        self.filtro_code = filtro_code
        
        if filtro_code == "Blur":
            self.filtro = lambda x: cv.blur(x,(5,5))
        elif filtro_code == "Gaussian":
            self.filtro = lambda x: cv.GaussianBlur(x,(5,5),0,0)
        elif filtro_code == "Median":
            self.filtro = lambda x: cv.medianBlur(x,5)
        elif filtro_code == "Bilateral":
            self.filtro = lambda x: cv.bilateralFilter(x,5,5,5)
        else:
            filtro_code = ""
        return;
        
    def apply_color(self,color_code):
        self.color = color_code
        color_dict = {"AUTUMN" : 0,"BONE" : 1,"JET" : 2,"WINTER" : 3,"RAINBOW" : 4,
                          "OCEAN" : 5,"SUMMER" : 6,"SPRING" : 7,"COOL" : 8,"HSV" : 9,
                          "PINK" : 10,"HOT" : 11,"PARULA" : 12,"MAGMA" : 13,"INFERNO" : 14,
                          "PLASMA" : 15,"VIRIDIS" : 16,"CIVIDIS" : 17,"TWILIGHT" : 18,
                          "TWILIGHT_SHIFTED" : 19,"TURBO" : 20,"DEEPGREEN" : 21}
        self.color_index = color_dict[color_code]
        
    def composition_transparency(self,new_alpha):
        #colocar um assert no alpha
        self.alpha = new_alpha
        return;
    
    
    def output(self,lista_imagens):
        
        imagens = []
            
        n_images = 0
        #img_edited = cropped_image(self.img, self.height, self.width, self.crop[0], self.crop[1])
        img_edited = cv.resize(np.copy(self.img),[int(self.img.shape[1]*self.resize[1]),int(self.img.shape[0]*self.resize[0])])
        img_edited_label = cv.putText(np.copy(img_edited),"Imagem Original",(0,30),cv.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),thickness = 1)

        if lista_imagens[0].get() == 1:
            imagens.append(img_edited_label)
            n_images +=1
            
        fixo = cv.absdiff(self.img,self.background_fixo)
        #fixo = cropped_image(fixo, self.height, self.width, self.crop[0], self.crop[1])
        fixo = cv.resize(fixo,[int(fixo.shape[1]*self.resize[1]),int(fixo.shape[0]*self.resize[0])])
        fixo = cv.convertScaleAbs(fixo,alpha = self.contrast, beta = self.brightness)
        fixo_label = cv.putText(np.copy(fixo),"Background_Fixo",(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
        if lista_imagens[1].get() == 1:    
            imagens.append(fixo_label)
            n_images +=1
            
        variado = cv.absdiff(self.img,self.background_variado)
        #variado = cropped_image(variado, self.height, self.width, self.crop[0], self.crop[1])
        variado = cv.resize(variado,[int(variado.shape[1]*self.resize[1]),int(variado.shape[0]*self.resize[0])])            
        variado = cv.convertScaleAbs(variado,alpha = self.contrast, beta = self.brightness)
        variado_label = cv.putText(np.copy(variado),"Background_Variado",(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
        if lista_imagens[2].get() == 1:
            imagens.append(variado_label)
            n_images +=1
            
        composition = cv.addWeighted(fixo,self.alpha,variado,1-self.alpha,0)
        composition_label = cv.putText(np.copy(composition),"Composition",(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
        if lista_imagens[3].get() == 1:
            imagens.append(composition_label)
            n_images +=1
        
        if lista_imagens[4].get() == 1:
            img_filtro = self.filtro(img_edited)
            img_filtro = cv.putText(img_filtro,self.filtro_code,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(img_filtro)
            n_images +=1
        if lista_imagens[5].get() == 1:
            fixo_filtro = self.filtro(fixo)
            fixo_filtro = cv.putText(fixo_filtro,"fixo"+self.filtro_code,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(fixo_filtro)
            n_images +=1
        if lista_imagens[6].get() == 1:
            variado_filtro = self.filtro(variado)
            variado_filtro = cv.putText(variado_filtro,"variado "+self.filtro_code,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(variado_filtro)
            n_images +=1
        if lista_imagens[7].get() == 1:
            composition_filtro = self.filtro(composition)
            composition_filtro = cv.putText(composition_filtro,"composition "+self.filtro_code,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(composition_filtro)
            n_images +=1
        if lista_imagens[8].get() == 1:
            img_color = cv.applyColorMap(img_edited,self.color_index)
            img_color = cv.putText(img_color,self.color,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(img_color)
            n_images +=1
        if lista_imagens[9].get() == 1:
            fixo_color = cv.applyColorMap(fixo,self.color_index)
            fixo_color = cv.putText(fixo_color,"fixo "+self.color,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(fixo_color)
            n_images +=1
        if lista_imagens[10].get() == 1:
            variado_color = cv.applyColorMap(variado,self.color_index)
            variado_color = cv.putText(variado_color,"variado "+self.color,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(variado_color)
            n_images +=1
        if lista_imagens[11].get() == 1:
            composition_color = cv.applyColorMap(composition,self.color_index)
            composition_color = cv.putText(composition_color,"composition "+self.color,(0,30),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),thickness = 1)
            imagens.append(composition_color)
            n_images +=1
        
        saida = np.zeros((self.height,self.width,3), dtype="uint8")
        
        if n_images == 1:
            n_i = 1
            n_j = 1
        elif n_images < 3:
            n_i = 1
            n_j = 2
        elif n_images < 5:
            n_i = 2
            n_j = 2
        elif n_images < 9:
            n_i = 4
            n_j = 2
        else:
            n_i = 3
            n_j = 4
        
        aux = 0
        for i in range(n_i):
            for j in range(n_j):
                try:
                    saida[imagens[aux].shape[0]*i:imagens[aux].shape[0]*(i+1),imagens[aux].shape[1]*j:imagens[aux].shape[1]*(j+1)] = imagens[aux]
                except:
                    aux = aux
                aux += 1
        
        return saida;
        

# def cropped_image(Image, ly, lx,Cx,Cy):
#     #cropped_image(img, crop[0], crop[1], crop_position[0], crop_position[1])
#     #borders
#     if Cx <= 0 and Cy <= 0:
#         return Image
#     px1, px2 = Cx - int(lx / 2), Cx + int(lx / 2)
#     qy1, qy2 = Cy - int(ly / 2), Cy + int(ly / 2)
#     return Image[qy1:qy2,px1:px2]

# def find_reference(img,Cx,Cy,lx=200,ly=200):
    
#     #borders
#     px1, px2 = Cx - int(lx / 2), Cx + int(lx / 2)
#     qy1, qy2 = Cy - int(ly / 2), Cy + int(ly / 2)
    
#     img[qy1:qy2, px1] = [0,0,255]
#     img[qy1:qy2, px2] = [0,0,255]
#     img[qy1, px1:px2] = [0,0,255]
#     img[qy2, px1:px2] = [0,0,255]
    
#     cv.imshow("img",img)
    
#     if cv.waitKey(0) == ord('q'):
#         cv.destroyAllWindows()
#     return