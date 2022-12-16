import os
from os import path
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from moviepy import *
from pytube import YouTube
from pytube import Playlist
from tkinter import messagebox
import shutil
import threading

#funções

#função para selecionar caminho para salvar arquivo
def selecionar_path():
    #permite usuario selecionar a pasta para salvar
    path = filedialog.askdirectory()
    path_label.config(text=path)

#função para baixar video
def download_file():
    #pegar o local para salvar
    user_path = path_label.cget("text")

    if user_path == "Selecione o caminho para salvar o arquivo" or user_path == "":
        messagebox.showinfo(title="Atenção!", message="Selecione o caminho para\nsalvar o arquivo")
    else:
        
        get_link = link_campo.get()

        eh_ytLink = get_link[0:23]
        if eh_ytLink == "https://www.youtube.com":

            eh_videoLink = get_link[0:29]

            if eh_videoLink == "https://www.youtube.com/watch":

                #pegar caminho selecionado
                path_label.cget("text")
                #download video
                yt = YouTube(get_link)
                video  = yt.streams.filter(only_audio=True).first()
                screen.title("Baixando video...")
                #baixando
                download_video = video.download()

                #convertento para mp3
                base, ext = os.path.splitext(download_video)
                new_video = base + ".mp3"
                os.rename(download_video, new_video)

                #mover para a pasta download
                shutil.move(new_video, user_path)
                messagebox.showinfo(title="Concluído", message="Download Completo!")
                screen.title("Download Completo")
                
            eh_playlist = get_link[0:32]
            if eh_playlist == "https://www.youtube.com/playlist":
                
                yt_platlist = Playlist(get_link)
                for video in yt_platlist.videos:
                    #baixando
                    download_playlist_video = video.streams.filter(only_audio=True).first().download()
                    screen.title("Baixando video...")

                    #converter para mp3
                    base, ext = os.path.splitext(download_playlist_video)
                    new_playlist_video = base + ".mp3"
                    os.rename(download_playlist_video, new_playlist_video)

                    #mvoer para pasta download
                    #arrumar shutil.move
                    shutil.move(new_playlist_video, user_path)

                screen.title("Download Completo")
                messagebox.showinfo(title="Concluído", message="Download Completo!")

#função para pesquisar video ou playlist
def pesquisa():

    if playlist_video.get() == "Você selecionou Playlist!":
        get_link = link_campo.get()


        eh_ytLink = get_link[0:23]
        if eh_ytLink == "https://www.youtube.com":

            eh_playlist = get_link[0:32]
            
            if eh_playlist == "https://www.youtube.com/playlist":
            
                playlist_yt = Playlist(get_link)
                video_label.config(text=playlist_yt.title, font=("Trebuchet MS",15))
            else:
                messagebox.showinfo(title="Link", message="Esse link não é de uma playlist\nPor favor selecione video!")
        else:
            messagebox.showinfo(title="Link",message="Esse não é um link do youtube!\nPor favor insira um link válido...")
            

    else:
        get_link = link_campo.get()
        
        eh_ytLink = get_link[0:23]
        if eh_ytLink == "https://www.youtube.com":

            eh_videoLink = get_link[0:29]

            if eh_videoLink == "https://www.youtube.com/watch":

                yt = YouTube(get_link)
                video_label.config(text=yt.title, font=("Trebuchet MS",15))

            else:
                messagebox.showinfo(title="Link", message="Esse link não é de um video\nPor favor selecione playlist!")
        else:
            messagebox.showinfo(title="Link",message="Esse não é um link do youtube!\nPor favor insira um link válido...")

#messabox para mostrar o que foi selecionado playlist ou video
def playlist_ou_video():
    messagebox.showinfo(title='Escolha',message=playlist_video.get())

#criação da janela e seus objetos
screen = Tk()
title = screen.title("Youtube Downloader")
canvas = Canvas(screen, width=500, height=500)
canvas.pack()

playlist_video = StringVar()

#logo do app
logo_img = PhotoImage(file="Zoe.png")
#logo_img = PhotoImage(file="melhor img do planeta.png")
#resize
logo_img = logo_img.subsample(1,1)

canvas.create_image(60, 60, image=logo_img)

#campo do link
link_campo = Entry(screen,width=50)
link_label = Label(screen, text="Coloque o link para download: ", font=("Trebuchet MS",15))
#adicionando na para tela
canvas.create_window(270,60,window=link_label)
canvas.create_window(280,90,window=link_campo)

#pesquisa para ver nome do video
link_pesquisa = Button(screen, text="Pesquisar", command=pesquisa,font=("Trebuchet MS",9))
canvas.create_window(470,90,window=link_pesquisa)
#mostrando video
video_label = Label(screen,text="", font=("Trebuchet MS", 10))
canvas.create_window(250,140,window=video_label)

#checkbox para baixar playlist ou video
playlist_checkbox = Checkbutton(screen,text="Playlist", command=playlist_ou_video, variable=playlist_video, onvalue="Você selecionou Playlist!", offvalue="Você desselecionou Playlist!", font=("Trebuchet MS",10))
canvas.create_window(155,20,window=playlist_checkbox)
video_checkbox = Checkbutton(screen,text="Video", command=playlist_ou_video, variable=playlist_video, onvalue="Você selecionou video", offvalue="Você desselecionou video",font=("Trebuchet MS",10))
canvas.create_window(235,20,window=video_checkbox)

#Selecionar caminho para salvar arquivo
path_label = Label(screen, text="Selecione o caminho para salvar o arquivo", font=("Trebuchet MS",15))
selecionar_btn = Button(screen, text="Selecione", command=selecionar_path,font=("Trebuchet MS",10))

#Adicionar na tela
canvas.create_window(250,280,window=path_label)
canvas.create_window(250,330,window=selecionar_btn)

#Mostrando thumbnail do video
#imageUrl = ""
#u = urlopen(imageUrl)
#raw_data = u.read()
#u.close()

#photo = ImageTk.PhotoImage(data=raw_data)
#image_label = Label(screen, image=photo)
#image_label.pack()  

#aviso
label_aviso = Label(screen, text="AVISO: Caso a playlist seja sua não pode ser particular\nTem que estar (Não listada) ou (Pública)",font=("Trebuchet MS",9))
canvas.create_window(250,480,window=label_aviso)

#Download botoes
download_btn = Button(screen, text="Baixar Mp3", width=20, height=3, command=lambda: threading.Thread(target=download_file).start() ,font=("Trebuchet MS",10))
#Adicionar na tela
canvas.create_window(250,400,window=download_btn)

screen.mainloop()