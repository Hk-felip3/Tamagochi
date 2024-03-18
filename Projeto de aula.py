from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import requests
from tkinter import ttk
from tkinter import messagebox


class Tamagotchi:
    vida_min = 0
    vida_max = 100

    fome_min = 0
    fome_max = 10

    energia_min = 0
    energia_max = 10

    felicidade_min = 0
    felicidade_max = 10

    xp_min = 0
    xp_Up_Nivel = 60

    def __init__(self, nome):
        self.nome = nome
        self.vida = 100
        self.fome = 10
        self.energia = 10
        self.felicidade = 10
        self.xp = 0
        self.level = 1

    def verificarAtributos(self):
        if self.vida > self.vida_max:
            self.vida = self.vida_max
        elif self.vida < self.vida_min:
            self.vida = self.vida_min

        if self.fome > self.fome_max:
            self.fome = self.fome_max
        elif self.fome < self.fome_min:
            self.fome = self.fome_min

        if self.energia > self.energia_max:
            self.energia = self.energia_max
        elif self.energia < self.energia_min:
            self.energia = self.energia_min

        if self.felicidade > self.felicidade_max:
            self.felicidade = self.felicidade_max
        elif self.felicidade < self.felicidade_min:
            self.felicidade = self.felicidade_min

        if self.xp >= self.xp_Up_Nivel:
            self.xp = self.xp_min
            self.level += 1
            if self.level == 7:
                messagebox.showinfo("Evolução", "Você evoluiu para Charmeleon!")
            elif self.level == 15:
                messagebox.showinfo("Evolução", "Você evoluiu para Charizard!")

    def alimentar(self):
        self.fome += 2
        self.energia -= 1
        self.verificarAtributos()
        if self.fome == self.fome_max:
            messagebox.showinfo("Aviso", "Estou cheio! Pronto para lutar novamente.")

    def brincar(self):
        self.felicidade += 5
        self.energia -= 2
        self.fome -= 2
        self.verificarAtributos()

    def dormir(self):
        self.vida += 20
        self.energia = 10
        self.fome -= 2
        self.felicidade -= 2
        self.verificarAtributos()

    def realizar_luta(self):
        self.xp += 20
        self.vida -= 20
        self.energia -= 3
        self.fome -= 3
        self.felicidade = 10
        self.verificarAtributos()


def atualizar_barras():
    fome_progressbar['value'] = tamagotchi.fome
    energia_progressbar['value'] = tamagotchi.energia
    felicidade_progressbar['value'] = tamagotchi.felicidade


def atualizar_status():
    fome_label.config(text="Fome: {}".format(tamagotchi.fome))
    energia_label.config(text="Energia: {}".format(tamagotchi.energia))
    felicidade_label.config(text="Felicidade: {}".format(tamagotchi.felicidade))
    level_label.config(text="Level: {}".format(tamagotchi.level))
    atualizar_barras()
    atualizar_imagem()


def atualizar_imagem():
    if tamagotchi.level < 7:
        url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png"
        evolucao_inicial = "Charmander"
        evolucao_nivel_7 = "Charmeleon"
        evolucao_maxima = "Charizard"
    elif tamagotchi.level < 15:
        url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/005.png"
        evolucao_inicial = "Charmeleon"
        evolucao_nivel_7 = "Charmeleon"
        evolucao_maxima = "Charizard"
    else:
        url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png"
        evolucao_inicial = "Charizard"
        evolucao_nivel_7 = "Charizard"
        evolucao_maxima = "Charizard"

    response = requests.get(url)
    imagem_bytes = response.content
    imagem = Image.open(BytesIO(imagem_bytes))
    imagem = imagem.resize((200, 200))
    imagem_tk = ImageTk.PhotoImage(imagem)
    imagem_label.configure(image=imagem_tk,
                           text=f"{evolucao_inicial}\nLevel 7: {evolucao_nivel_7}\nLevel 15: {evolucao_maxima}")
    imagem_label.image = imagem_tk


def alimentar_tamagotchi():
    tamagotchi.alimentar()
    atualizar_status()


def brincar_tamagotchi():
    tamagotchi.brincar()
    atualizar_status()


def dormir_tamagotchi():
    tamagotchi.dormir()
    atualizar_status()


def lutar_tamagotchi():
    tamagotchi.realizar_luta()
    atualizar_status()


janela = tk.Tk()
janela.title("Tamagotchi")
janela.geometry("400x700")

imagem_label = tk.Label(janela, text="Charmander")
imagem_label.pack(pady=100)

status_label = tk.Label(janela, text="Status:")
status_label.pack()

status_frame = tk.Frame(janela)
status_frame.pack()

tamagotchi = Tamagotchi("Meu Tamagotchi")

fome_label = tk.Label(status_frame, text="Fome: {}".format(tamagotchi.fome))
fome_label.pack(side=tk.LEFT, padx=7)

energia_label = tk.Label(status_frame, text="Energia: {}".format(tamagotchi.energia))
energia_label.pack(side=tk.LEFT, padx=10)

felicidade_label = tk.Label(status_frame, text="Felicidade: {}".format(tamagotchi.felicidade))
felicidade_label.pack(side=tk.LEFT, padx=10)

level_label = tk.Label(status_frame, text="Level: {}".format(tamagotchi.level))
level_label.pack(side=tk.LEFT, padx=10)

fome_progressbar = ttk.Progressbar(janela, length=200, maximum=10, value=tamagotchi.fome)
fome_progressbar.pack(pady=10)

energia_progressbar = ttk.Progressbar(janela, length=200, maximum=10, value=tamagotchi.energia)
energia_progressbar.pack(pady=10)

felicidade_progressbar = ttk.Progressbar(janela, length=200, maximum=10, value=tamagotchi.felicidade)
felicidade_progressbar.pack(pady=10)

button_frame = tk.Frame(janela)
button_frame.pack(side=tk.BOTTOM, pady=10)

alimentar_button = tk.Button(button_frame, text="Alimentar", command=alimentar_tamagotchi)
alimentar_button.pack(side=tk.LEFT, padx=10)

brincar_button = tk.Button(button_frame, text="Brincar", command=brincar_tamagotchi)
brincar_button.pack(side=tk.LEFT, padx=10)

dormir_button = tk.Button(button_frame, text="Dormir", command=dormir_tamagotchi)
dormir_button.pack(side=tk.LEFT, padx=10)

lutar_button = tk.Button(button_frame, text="Lutar", command=lutar_tamagotchi)
lutar_button.pack(side=tk.LEFT, padx=10)

atualizar_status()

janela.mainloop()

