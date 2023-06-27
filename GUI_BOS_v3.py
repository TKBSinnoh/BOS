# -*- coding: utf-8 -*-
"""
Created on Fri May 19 08:44:37 2023

@author: Master
"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import cv2 as cv
import BOS_support_v4 as BS3


def open_file():
    
    filepath = askopenfilename(initialdir = "C:/Users/",
                               title = "Select Video",
        filetypes = [("Arquivos MP4","*.mp4"),("Arquivos AVI","*.avi"),("All Files", "*.*")]
        )
    if not filepath:
        return

    entry_load.delete(0,tk.END)                                       # Delete any strings in text box for file name
    entry_load.insert(0,filepath)                                 # Add file name to the text box
    
    cap = cv.VideoCapture(filepath)
    comprimento_imagem.set(int(cap.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5))
    altura_imagem.set(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count/fps)
    time_final.set(time_int_to_str(duration))

    return;

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("Arquivos MP4", "*.mp4"),("Arquivos AVI","*.avi"),("All Files", "*.*")]
    )
    if not filepath:
        return
    
    entry_save.delete(0,tk.END)                                       # Delete any strings in text box for file name
    entry_save.insert(0,filepath)                                 # Add file name to the text box
    
    return;
    
def time_str_to_int(time):
    m,s = time.split(':')
    total_time = 60*int(m) + int(s)
    return total_time

def time_int_to_str(time):
    m = time//60
    s = time%60
    if m < 10:
        string1 = "0" + repr(m)
    else:
        string1 = repr(m)
    
    if s < 10:
        string2 = "0" + repr(s)
    else:
        string2 = repr(s)
    return(string1+":"+string2)

window = tk.Tk()

n = ttk.Notebook(window)
n.pack(pady=10, expand=True)

f1 = ttk.Frame(n)
f2 = ttk.Frame(n)

#--------------LOAD AND SAVE BUTTONS-------------------------------------------

load = ttk.Frame(f1)
loadlbl = ttk.Label(load,text= "Video File:")
loadlbl.grid(row = 0,column = 0,sticky = "w")
save = ttk.Frame(f1)
savelbl = ttk.Label(save,text = "Save Location:")
savelbl.grid(row = 2,column = 0, sticky = "w")

buttonLoadImage = ttk.Button(load,text = "...",command = open_file)
buttonLoadImage.grid(column = 3,row = 1)

buttonSaveImage = ttk.Button(save,text = "...", command = save_file)
buttonSaveImage.grid(column = 3, row = 3)

load_path = tk.StringVar()
entry_load = tk.Entry(load,textvariable = load_path)
entry_load.configure(bg = "White", fg = "Black", width = 50)
entry_load.grid(column = 0, row = 1, columnspan = 3)
load.grid(column = 0, row = 0, columnspan = 3)

save_path = tk.StringVar()
entry_save = tk.Entry(save,textvariable = save_path)
entry_save.configure(bg = "white", fg = "black", width = 50)
entry_save.grid(column = 0, row = 3, columnspan = 3)
save.grid(column = 0, row = 1,columnspan = 3)

#------------------------------------------------------------------------------


#------------IMAGE SELECTOR----------------------------------------------------

lf3 = ttk.LabelFrame(f1,text = "Imagens:")
lf3.grid(column=0, row=4,sticky = "w",padx = 15)

RealImage = tk.IntVar()
check_image = ttk.Checkbutton(lf3, text='Video original', 
	    variable=RealImage)
check_image.grid(row = 0,column =0,sticky = "w")

BOSfixo = tk.IntVar()
check_BOS_fixo = ttk.Checkbutton(lf3, text='Background Fixo', 
	    variable=BOSfixo)
check_BOS_fixo.grid(row = 1,column =0,sticky = "w")

BOSvariado = tk.IntVar()
check_BOS_variado = ttk.Checkbutton(lf3, text='Background Variado', 
	    variable=BOSvariado)
check_BOS_variado.grid(row = 3,column =0,sticky = "w")

BOScomposition = tk.IntVar()
check_BOS_composition = ttk.Checkbutton(lf3, text='Composição dos métodos', 
	    variable=BOScomposition)
check_BOS_composition.grid(row = 4,column =0,sticky = "w")


#------------------------------------------------------------------------------

#----------FILTER SELECTOR-----------------------------------------------------

lf4 = ttk.LabelFrame(f1,text = "Filtros:")
lf4.grid(column=1, row=4,sticky = "w",padx = 15)

filter_type = tk.StringVar()
combo = ttk.Combobox(lf4,textvariable = filter_type,state = 'readonly')
combo['values'] = ["","Blur",'Gaussian',"Median","Bilateral"]
combo.grid(row = 0,column = 0,sticky = "w")

FilterImage = tk.IntVar()
check_image = ttk.Checkbutton(lf4, text='Video original', 
	    variable=FilterImage,onvalue=1, offvalue=0)
check_image.grid(row = 1,column =0,sticky = "w")

FilterBOSfixo = tk.IntVar()
check_BOS_fixo = ttk.Checkbutton(lf4, text='Background Fixo', 
	    variable=FilterBOSfixo,onvalue=1, offvalue=0)
check_BOS_fixo.grid(row = 2,column =0,sticky = "w")

FilterBOSvariado = tk.IntVar()
check_BOS_variado = ttk.Checkbutton(lf4, text='Background Variado', 
	    variable=FilterBOSvariado,onvalue=1, offvalue=0)
check_BOS_variado.grid(row = 3,column =0,sticky = "w")

FilterBOScomposition = tk.IntVar()
check_BOS_composition = ttk.Checkbutton(lf4, text='Composição dos métodos', 
	    variable=FilterBOScomposition,onvalue=1, offvalue=0)
check_BOS_composition.grid(row = 4,column =0,sticky = "w")

#------------------------------------------------------------------------------

#---------------COLOR SCHEME SELECTION ----------------------------------------

lf5 = ttk.LabelFrame(f1,text = "Esquema de cores:")
lf5.grid(column=2, row=4,sticky = "w",padx = 15)

Color_type = tk.StringVar()
combo = ttk.Combobox(lf5,textvariable = Color_type,state = 'readonly')
combo['values'] = ["","AUTUMN","BONE","JET","WINTER","RAINBOW","OCEAN",
                   "SUMMER","SPRING","COOL","HSV","PINK","HOT","PARULA",
                   "MAGMA","INFERNO","PLASMA","VIRIDIS","CIVIDIS","TWILIGHT",
                   "TWILIGHT_SHIFTED","TURBO","DEEPGREEN"]
combo.grid(row = 0,column = 0,sticky = "w")

ColorImage = tk.IntVar()
check_image = ttk.Checkbutton(lf5, text='Video original', 
	    variable=ColorImage,onvalue=1, offvalue=0)
check_image.grid(row = 1,column =0,sticky = "w")

ColorBOSfixo = tk.IntVar()
check_BOS_fixo = ttk.Checkbutton(lf5, text='Background Fixo', 
	    variable=ColorBOSfixo,onvalue=1, offvalue=0)
check_BOS_fixo.grid(row = 2,column =0,sticky = "w")

ColorBOSvariado = tk.IntVar()
check_BOS_variado = ttk.Checkbutton(lf5, text='Background Variado', 
	    variable=ColorBOSvariado,onvalue=1, offvalue=0)
check_BOS_variado.grid(row = 3,column =0,sticky = "w")

ColorBOScomposition = tk.IntVar()
check_BOS_composition = ttk.Checkbutton(lf5, text='Composição dos métodos', 
	    variable=ColorBOScomposition,onvalue=True, offvalue=False)
check_BOS_composition.grid(row = 4,column =0,sticky = "w")

lista_imagens = [RealImage,BOSfixo,BOSvariado,BOScomposition,
                 FilterImage,FilterBOSfixo,FilterBOSvariado,FilterBOScomposition,
                 ColorImage,ColorBOSfixo,ColorBOSvariado,ColorBOScomposition]

#------------------------------------------------------------------------------

#-----------------LAYOUT-------------------------------------------------------

# lf6 = ttk.LabelFrame(f1,text = "Layout:")
# lf6.grid(column=0, row=5,sticky = "w",padx = 15,columnspan = 2)

# entry_T1_output = tk.Entry(lf6,width = 6)
# T1_output_label = ttk.Label(lf6, text = "Nº imagens vertical:")
# entry_T1_output.grid(column = 1,row = 1,sticky = "w")
#T1_output_label.grid(column = 0,row = 1,sticky = "w")

# entry_T2_output = tk.Entry(lf6,width = 6)
# T2_output_label = ttk.Label(lf6, text = "Nº imagens Horizontal:")
# entry_T2_output.grid(column = 3,row = 1,sticky = "w")
#T2_output_label.grid(column = 2,row = 1,sticky = "w")

# sup = 2
# for i in range(2):
#     for j in range(2):
#         frame = ttk.Frame(lf6)
#         label = ttk.Label(frame,text = lista_nomes[i])
#         label['background'] = 'black'
#         label['foreground'] = 'white'
#         frame.grid(row = i+2, column = j)
#         label.grid(row = i+2, column = j,padx = 5,pady = 5,sticky = "nsew")
    

#------------------------------------------------------------------------------

#------------------CONFIGURAÇÕES-----------------------------------------------

#------------------ CROP ------------------------------------------------------

lf7 = ttk.LabelFrame(f2,text = "Recortar:")
lf7.grid(column=0,row =0,columnspan = 3, sticky = "w")


##POSIÇÃO

frame_position = ttk.Frame(lf7)
frame_label = ttk.Label(frame_position,text = "Posição:")
frame_label.grid(row = 0,column = 0,pady = 5)

crop_x = tk.IntVar(0)
entry_width = tk.Entry(frame_position,textvariable = crop_x,width = 6)
entry_widthlbl = ttk.Label(frame_position, text = "Coordenada X:")
entry_widthlbl.grid(column = 0,row = 1,sticky = "w")
entry_width.grid(column = 1,row = 1,sticky = "w")

crop_y = tk.IntVar(0)
entry_height = tk.Entry(frame_position,textvariable = crop_y,width = 6)
entry_heightlbl = ttk.Label(frame_position, text = "Coordenada Y:")
entry_heightlbl.grid(column = 2,row = 1,sticky = "w")
entry_height.grid(column = 3,row = 1,sticky = "w")

frame_position.grid(row = 0, column = 0,padx = 5)

##TAMANHO

frame_tamanho = ttk.Frame(lf7)
frame_label = ttk.Label(frame_tamanho,text = "Tamanho:")
frame_label.grid(row = 0,column = 0,pady = 5)

crop_height = tk.IntVar(0)
entry_height = tk.Entry(frame_tamanho,textvariable = crop_height,width = 6)
entry_heightlbl = ttk.Label(frame_tamanho, text = "Height:")
entry_heightlbl.grid(column = 0,row = 1,sticky = "w")
entry_height.grid(column = 1,row = 1,sticky = "w")

crop_width = tk.IntVar(0)
entry_width = tk.Entry(frame_tamanho,textvariable = crop_width,width = 6)
entry_widthlbl = ttk.Label(frame_tamanho, text = "Width:")
entry_widthlbl.grid(column = 2,row = 1,sticky = "w")
entry_width.grid(column = 3,row = 1,sticky = "w")

frame_tamanho.grid(row = 0, column = 1,padx = 3)

#------------------------------------------------------------------------------

#----------------REDIMENSIONAR-------------------------------------------------

lf8 = ttk.LabelFrame(f2,text = "Redimensionar:")
lf8.grid(column=0,row =2,columnspan = 3,sticky = 'w')

frame_duracao = ttk.Frame(lf8)
frame_label = ttk.Label(frame_duracao,text = "Duração(MM:SS):")
frame_label.grid(row = 0,column = 0,columnspan = 2,pady = 5)

time_inicio = tk.StringVar(lf8,"00:00")
entry_inicio = tk.Entry(frame_duracao,width = 6,textvariable = time_inicio)
entry_iniciolbl = ttk.Label(frame_duracao, text = "Tempo inicial:")
entry_iniciolbl.grid(column = 0,row = 1,sticky = "w")
entry_inicio.grid(column = 1,row = 1,sticky = "w")

time_final = tk.StringVar(lf8,'00:00')
entry_fim = tk.Entry(frame_duracao,width = 6,textvariable = time_final)
entry_fimlbl = ttk.Label(frame_duracao, text = "Tempo final:")
entry_fimlbl.grid(column = 2,row = 1,sticky = "w")
entry_fim.grid(column = 3,row = 1,sticky = "w")

frame_duracao.grid(row = 0, column = 0,padx = 3)

frame_tamanho = ttk.Frame(lf8)
frame_label = ttk.Label(frame_tamanho,text = "Tamanho Individual de cada imagem:")
frame_label.grid(row = 0,column = 0,columnspan = 4,pady = 5)

altura_imagem = tk.IntVar(lf8,0)
entry_height_imagem = tk.Entry(frame_tamanho,textvariable = altura_imagem,width = 6)
entry_height_imagemlbl = ttk.Label(frame_tamanho, text = "Height:")
entry_height_imagemlbl.grid(column = 0,row = 1,sticky = "w")
entry_height_imagem.grid(column = 1,row = 1,sticky = "w")

comprimento_imagem = tk.IntVar(lf8,0)
entry_width_imagem = tk.Entry(frame_tamanho,width = 6,textvariable = comprimento_imagem)
entry_width_imagemlbl = ttk.Label(frame_tamanho, text = "Width:")
entry_width_imagemlbl.grid(column = 2,row = 1,sticky = "w")
entry_width_imagem.grid(column = 3,row = 1,sticky = "w")

frame_tamanho.grid(row = 0, column = 1,padx = 3)


#-----------------CONTRASTE, BRILHO E COMPOSIÇÃO-------------------------------

lf9 = ttk.LabelFrame(f2,text = "Contraste:")
lf9.grid(column=0,row =3,sticky = 'w')

contrast = tk.IntVar()
scale = tk.Scale(lf9, orient='horizontal', length=200, from_=-10, to=10, variable=contrast,resolution = 1,tickinterval = 10)
scale.grid(column=0, row=2, sticky='we')
scale.set(0)

lf10 = ttk.LabelFrame(f2,text = "Brilho:")
lf10.grid(column=1,row =3,sticky = 'we')

bright = tk.IntVar()
scale = tk.Scale(lf10, orient='horizontal', length=200, from_=-50, to=50, variable=bright,resolution = 1,tickinterval = 50)
scale.grid(column=0, row=2, sticky='we')
scale.set(0)

lf11 = ttk.LabelFrame(f2,text = "Composição:")
lf11.grid(column=2,row =3,sticky = 'we')

alpha = tk.IntVar()

label_percent = ttk.Label(lf11)
label_percent["text"] = repr(round(0.5 * 100,2)) + "%"
label_percent.grid(row = 0,column = 1)
label_fixo = ttk.Label(lf11,text = 'fixo')
label_fixo.grid(column = 0, row = 0,sticky = "w")
label_variado = ttk.Label(lf11,text = 'variado')
label_variado.grid(column = 2, row = 0,sticky = "e")

def var_percent(num):
    val = float(num)
    if val>0:
        label_percent["text"] = repr(round((0.5 + val)*100,2)) +"% -->"
    if val<0:
        label_percent["text"] = "<--" +repr(round((0.5 + abs(val))*100,2)) + "%"
    if val == 0:
        label_percent["text"] = repr(round(0.5 * 100,2)) + "%"
    return

scale = tk.Scale(lf11, orient='horizontal', length=200, from_=-0.5, to=0.5, variable=alpha,resolution = 0.05,showvalue = 0,command = var_percent)
scale.grid(column=0, row=2,columnspan = 3, sticky='we')
scale.set(0)


#------------------------------------------------------------------------------

#------------------EXECUTAR + PROGRESS BAR ------------------------------------

lf12 = ttk.LabelFrame(f1)
lf12.grid(column = 0,row = 6,columnspan = 3,sticky = "w")

execution_progress = ttk.Progressbar(lf12, orient=tk.HORIZONTAL, length=200, mode='determinate')
execution_progress.grid(column = 1, row = 0,columnspan = 3)

def execute():
    try:
        video_teste = BS3.video(load_path.get())
    except:
        tk.messagebox.showinfo(message="Caminho de arquivo invalido")
        return
    execution_progress['value'] = 0
    execution_progress['maximum'] = video_teste.frame_count
    
    n_images = 0
    for image in lista_imagens:
        if image.get() == 1:
            n_images += 1
     
    video_teste.crop_coeff(crop_height.get(), crop_width.get(), crop_x.get(), crop_y.get())
    video_teste.resize_coeff(altura_imagem.get(), comprimento_imagem.get(),n_images)
    video_teste.brilho(contrast.get(), bright.get())
    video_teste.composition_transparency(alpha.get())
    if not (filter_type.get() == ""):
        video_teste.apply_filter(filter_type.get())
    if not (Color_type.get() == ""):   
        video_teste.apply_color(Color_type.get())
    
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(save_path.get(), fourcc, 30.0, (video_teste.width,video_teste.height))

    video_teste.ret, video_teste.img = video_teste.cap.read()   
    video_teste.background_fixo = video_teste.img
    
    time_aux = 0
    while video_teste.cap.isOpened():
        execution_progress['value'] += 1
        lf12.update_idletasks()
        video_teste.background_variado = video_teste.img            
            
        video_teste.ret, video_teste.img = video_teste.cap.read()
        
        
        if not video_teste.ret:
            break
        
        if(time_str_to_int(time_inicio.get())*video_teste.fps < time_aux) and ((time_str_to_int(time_final.get())+1)*video_teste.fps > time_aux):
            saida = video_teste.output(lista_imagens)
            
            out.write(saida)
            
            if cv.waitKey(1) == ord('q'):
                break
        time_aux += 1
        
    tk.messagebox.showwarning("teste","Processo finalizado")    
    video_teste.cap.release()
    out.release()
    cv.destroyAllWindows()
    return


exec_button = ttk.Button(lf12,text = "Executar",command = execute)
exec_button.grid(column = 0, row = 0,padx = 20)

#------------------------------------------------------------------------------


n.add(f1, text = "Imagens")
n.add(f2, text = "Configurações")
 
window.mainloop()
