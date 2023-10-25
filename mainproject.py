import customtkinter as ctk
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
import json
import re
import os


class MainScreen:
    def __init__(self):

        # Config da janela
        ctk.set_appearance_mode('dark')
        self.root = ctk.CTk()
        self.root.title('Contatos')
        self.root.resizable(False, False)
        self.root.geometry('680x450+330+110')

        # Selection Clear
        self.root.bind_all('<Button-1>', lambda event: event.widget.focus_set())

        # Contatos
        if os.path.isfile('contatos.json'):
            self.carregar_contatos_json()
        else:
            self.contatos = []

        # ID Contatos
        if len(self.contatos) == 0:
            self.id_contatos = 1
        else:
            self.id_contatos = len(self.contatos) + 1


        # Text fonts
        self.font1 = Font(family='@Batang', size=20, weight='bold', slant='roman', underline=False)
        self.font2 = Font(family='@KaiTi', size=10, weight='bold')
        self.font3 = Font(family='@KaiTi', size=8, weight='bold', underline=True, slant='italic')

        # Criação dos widgets
        self.frame = ctk.CTkFrame(self.root, corner_radius=12, width=630, height=400)
        self.frame.place(x=340, y=225, anchor=tk.CENTER)

        self.titulo_principal = tk.Label(self.frame, text='Contatos', font=self.font1, bg='#352c2c',
                                         fg='white')
        self.titulo_principal.place(x=250, y=8)

        self.linha_sep = ctk.CTkFrame(self.frame, width=1, bg_color='grey')
        self.linha_sep.place(x=312, y=100)

        self.criar_contato_label = tk.Label(self.frame, text='Criar Contato', font=self.font2, bg='#302c2c',
                                            fg='white')
        self.criar_contato_label.place(x=115, y=80)

        self.lista_contatos_label = tk.Label(self.frame, text='Lista de Contatos', font=self.font2, bg='#302c2c',
                                             fg='white')
        self.lista_contatos_label.place(x=410, y=80)

        self.nome_entry = ctk.CTkEntry(self.frame, width=180, placeholder_text='Nome')
        self.nome_entry.place(x=70, y=110)

        self.telefone_entry = ctk.CTkEntry(self.frame, width=180, placeholder_text='Telefone')
        self.telefone_entry.place(x=70, y=160)

        self.cpf_entry = ctk.CTkEntry(self.frame, width=180, placeholder_text='CPF')
        self.cpf_entry.place(x=70, y=210)

        self.email_entry = ctk.CTkEntry(self.frame, width=180, placeholder_text='Email')
        self.email_entry.place(x=70, y=260)


        self.criar_contato = ctk.CTkButton(self.frame, text='Criar', bg_color='#352c2c', fg_color='#8fa080',
                                               hover_color='#708066', corner_radius=16, text_color='white',
                                           command=self.adicionar_contato)
        self.criar_contato.place(x=88, y=310)

        self.voltar_label = tk.Label(self.frame, text='Voltar', font=self.font3, background='#352c2c', fg='white',
                                   cursor='hand2')
        self.voltar_label.bind('<Button-1>', self.leave)

        self.voltar_label.place(x=293, y=350)

        self.listbox = tk.Listbox(self.frame, width=40, relief='solid', background='#3f2c2c', fg='white',
                                  borderwidth=2, activestyle='none', selectbackground='grey')
        self.listbox.place(x=350, y=120)

        self.listbox.bind('<Double-Button>', self.mostrar_detalhes_contato)

        self.pesquisar_contato  = ctk.CTkEntry(self.frame, width=180, placeholder_text='Pesquisar contato')
        self.pesquisar_contato.place(x=350, y=300)

        self.botao_pesquisar = ctk.CTkButton(self.frame, text='Ok', bg_color='#352c2c', fg_color='#8fa080',
                                             hover_color='#708066', corner_radius=0, text_color='white', width=50,
                                             border_width=1, border_color='black', command=self.pesquisar_contatos)
        self.botao_pesquisar.place(x=545, y=300)

        self.contatos_data = {}
        print(self.contatos)
        self. atualizar_lista_contatos()


    def pesquisar_contatos(self):
        termo = self.pesquisar_contato.get().strip().lower()
        self.listbox.delete(0, tk.END)
        for i, contato in self.contatos_data.items():
            nome = contato['Nome'].lower()
            nomes = nome.split()
            if termo in nomes[0]:
                self.listbox.insert(tk.END, contato['Nome'])



    def adicionar_contato(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        cpf = self.cpf_entry.get()
        email = self.email_entry.get()

        telefone_info = False
        cpf_info = False
        email_info = False
        if nome and cpf and email:
            if len(telefone) == 10 or len(telefone) == 11:
                telefone_info = True
            else:
                messagebox.showwarning('Número inválido', 'Número de telefone inválido')
                self.telefone_entry.delete(0, tk.END)

            if len(cpf) == 11:
                cpf_info = True
            else:
                messagebox.showwarning('CPF inválido', 'Número de CPF Inválido')
                self.cpf_entry.delete(0, tk.END)

            if re.match(r'.+@.+\..+', email):
                email_info = True
            else:
                messagebox.showwarning('Email inválido', 'Formato de email inválido')
                self.email_entry.delete(0, tk.END)

        nome = nome.title()
        telefone = '(' + telefone[:2] + ')' + telefone[2:7] + '-' + telefone[7:]
        cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

        novo_contato = {
            'ID': f'{self.id_contatos:04d}',
            'Nome': nome,
            'Telefone': telefone,
            'CPF': cpf,
            'Email': email
        }

        if telefone_info and cpf_info and email_info:
            self.contatos.append(novo_contato)
            self.salvar_contato_json()
            self.atualizar_lista_contatos()
            messagebox.showinfo('Cadastrado com sucesso!', 'Usuário cadastrado com sucesso')
            self.nome_entry.delete(0, tk.END)
            self.telefone_entry.delete(0, tk.END)
            self.cpf_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        self.atualizar_lista_contatos()


    def salvar_contato_json(self):
        with open('contatos.json', 'w') as arquivo:
            json.dump(self.contatos, arquivo, indent=4)


    def atualizar_lista_contatos(self):
        self.listbox.delete(0, tk.END)

        with open('contatos.json', 'r', encoding='utf-8') as arquivo:
            try:
                contatos = json.load(arquivo)

                self.contatos_data = {}

                for i, contato in enumerate(contatos, start=1):
                    nome = contato['Nome']
                    self.listbox.insert(tk.END, nome)
                    self.contatos_data[i] = contato
            except json.decoder.JSONDecodeError:
                pass

    def mostrar_detalhes_contato(self, event):
        indices = self.listbox.curselection()

        if indices:
            index = int(indices[0])
            contato = self.contatos_data.get(index + 1)
            if contato:
                nome = contato['Nome']
                telefone = contato['Telefone']
                cpf = contato['CPF']
                email = contato['Email']
                id = contato['ID']

                info_root = ctk.CTk()
                info_root.resizable(False, False)
                info_root.geometry('400x280+470+220')
                info_root.overrideredirect(True)

                id_contato_label = ctk.CTkLabel(info_root, text='ID Contato: ', font=('Roboto', 18))
                id_contato_label.place(x=25, y=25)

                id_contato_label2 = ctk.CTkLabel(info_root, text=id, font=('Roboto', 18))
                id_contato_label2.place(x=120, y=25)

                nome_label = ctk.CTkLabel(info_root, text='Nome: ', font=('Roboto', 18))
                nome_label.place(x=25, y=65)

                nome_label2 = ctk.CTkLabel(info_root, text=nome, font=('Roboto', 18))
                nome_label2.place(x=120, y=65)

                telefone_label = ctk.CTkLabel(info_root, text='Telefone: ', font=('Roboto', 18))
                telefone_label.place(x=25, y=105)

                telefone_label2 = ctk.CTkLabel(info_root, text=telefone, font=('Roboto', 18))
                telefone_label2.place(x=120, y=105)

                cpf_label = ctk.CTkLabel(info_root, text='CPF: ', font=('Roboto', 18))
                cpf_label.place(x=25, y=145)

                cpf_label2 = ctk.CTkLabel(info_root, text=cpf, font=('Roboto', 18))
                cpf_label2.place(x=120, y=145)

                email_label = ctk.CTkLabel(info_root, text='Email: ', font=('Roboto', 18))
                email_label.place(x=25, y=185)

                email_label2 = ctk.CTkLabel(info_root, text=email, font=('Roboto', 18))
                email_label2.place(x=120, y=185)

                voltar_label = tk.Label(info_root, text='Voltar', font=self.font3, background='#352c2c',
                                        fg='white', cursor='hand2')
                voltar_label.place(x=180, y=240)
                voltar_label.bind('<Button-1>', lambda e: info_root.destroy())

                info_root.mainloop()



    def carregar_contatos_json(self):
        with open('contatos.json', 'r') as arquivo:
            try:
                self.contatos = json.load(arquivo)
            except json.decoder.JSONDecodeError:
                self.contatos = []
                self.contatos_data = {}

    def leave(self, event):
        from login import LoginScreen
        login = LoginScreen()

        login.root.mainloop()

    def run(self):
        print(self.contatos_data)
        self.root.mainloop()


