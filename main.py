import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font








class BloccoNote():


    #Definiamo il costruttore della nostra classe in modo che, se chiamiamo determinati metodi qui possiamo accedere ai loro dati e alle loro variabili che sono state definite all'interno
    def __init__(self):

       


        
        #variabile inizializzata per il path destinato all'apertura dei file
        self.filename = None

        #variabile utile per indicare i tipi di file quando chiediamo all'utente di salvare o aprire un file
        self.filetypes = (
            ("file di testo","*.txt"),
            )


        #Componenti della finestra
        self.root = Tk()
        self.root.title("Blocco Note")
        self.root.geometry("1080x900")
        self.widget()
        self.root.mainloop()



    #Metodo che serve per inizializzare tutte le componenti grafiche di tkinter
    def widget(self):

        #Creiamo un notebook per le nostre tab

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH,expand=True,pady=20)

        #Creiamo un frame da inserire all'interno del notebook
        self.frame = Frame(self.notebook)
        self.frame.pack()


        #Aggiungiamo la tab di default che si apre all'apertura del programma
        self.notebook.add(self.frame,text="Nuova Scheda")



        #Aggiungiamo uno scrolledtext cioè un area di testo scrollabile dentro il frame
        self.scrolledtxt = scrolledtext.ScrolledText(self.frame,width = 50,height = 10 )
        self.scrolledtxt.pack(fill=BOTH, expand=True)
        
        #Settiamo la dimensione del font dello scrolledtxt
        self.dim_font = 12
        self.font_corrente = font.Font(size = self.dim_font)
        self.scrolledtxt.configure(font=self.font_corrente)
        
        
        
        #Creiamo una MenuBar
        self.menubar = Menu(self.root)

        #configuriamo il menu nella finestra 
        self.root.config(menu=self.menubar)

        #Creiamo il menu file
        self.file_menu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File",menu=self.file_menu) 

        #Comandi del menu file
        self.file_menu.add_command(label="Nuova Scheda",command=self.nuova_scheda)
        self.file_menu.add_command(label="Apri file",command=self.apriFile)
        self.file_menu.add_command(label="Salva",command=self.salvaFile)
        self.file_menu.add_command(label="Salva con nome",command=self.salva_con_nome)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Esci", command=self.esci)





        #Creiamo il menu Modifica
        self.modifica_menu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Modifica", menu=self.modifica_menu)

        self.modifica_menu.add_command(label="Taglia", command=self.taglia)
        self.modifica_menu.add_command(label="Copia", command=self.copia)
        self.modifica_menu.add_command(label="Incolla", command=self.incolla)


        #Creiamo il menu Visualizza
        self.visualizza_menu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Visualizza", menu=self.visualizza_menu)


        self.zoom_submenu = Menu(self.visualizza_menu,tearoff=0)
        self.zoom_submenu.add_command(label="Zoom avanti", command=self.zoom_in)
        self.zoom_submenu.add_command(label="Zoom indietro",command=self.zoom_out)
        self.zoom_submenu.add_command(label="Ripristina Zoom", command = self.ResetZoom)


        self.visualizza_menu.add_cascade(label="Zoom",menu=self.zoom_submenu)




        

        #collegamento tasti shortcut per lo zoom

        self.root.bind("<Control-MouseWheel>",self.zoomRotella)
        self.root.bind("<Control-plus>",self.zoom_in)
        self.root.bind("<Control-minus>",self.zoom_out)
        self.root.bind("<Control-0>",self.ResetZoom)





        #Creiamo un menu contestuale per gestire le tab
        self.ctx_menu = Menu(self.notebook,tearoff=0)


        self.ctx_menu.add_command(label="Aggiungi tab",command=self.nuova_scheda)
        self.ctx_menu.add_command(label="Rimuovi tab",command=self.rimuovi_tab)





        #collegamento tasti shortcut per le tab
        self.notebook.bind("<Button-3>",self.ctx_menu_popup)
        self.notebook.bind("<Button-2>",self.rimuovi_tab)
        
    



    #metodo per eseguire un salvataggio che ci consente di scegliere il nome del file e crearne uno nuovo
    def salva_con_nome(self):


        try:
            #Chiediamo all'utente in quale file vuole salvare
            f = filedialog.asksaveasfile(mode="w",title="salva file",defaultextension=".txt", filetypes=self.filetypes)

            #ricaviamo il nome del file introdotto
            self.nome_file = os.path.basename(f.name)

            #Scriviamo il contenuto della scrolledtext in quel file
            f.write(self.scrolledtxt.get("1.0",END))

            #rinominiamo la tab 
            self.notebook.add(self.frame,text= self.nome_file)  
        except AttributeError:
            messagebox.showerror(title="Errore", message="Non è stato indicato nessun file")

        
        

        


    #metodo che salva in un file già importato in precedenza 
    def salvaFile(self):

        #Se esiste un filename, cioè il path di un file che è stato importato prima salva il file in quel percorso altrimenti
        if self.filename!= None:

            #apriamo il path in scrittura
            with open(self.filename,"w") as f:
                # e  poi scriviamo il contenuto della scrolledtext in quel file
                f.write(self.scrolledtxt.get("1.0",END))

        else:

            #Chiamia il metodo salva con nome che chiederà all'utente in input di salvare il file assegnandogli un nome
            self.salva_con_nome()
            

        

            




        
    
    #Metodo che ci consente di aprire il file ogni volta cliccato il tasto nella menu bar di file
    def apriFile(self):
        try:
            
            #Chiediamo in input il file da aprire
            self.filename = filedialog.askopenfilename(title="Apri un file",initialdir="/",filetypes=self.filetypes)

            #Se il file è stato selezionato e quindi abbiamo il percorso leggiamo il contenuto, prendiamo il nome del file e rinominiamo la tab, sostituiamo la tab precedente con la nuova che conterrà i dati letti dal file
            with open(self.filename,"r") as f:
                self.dati = f.read()  

                #Prendiamo il nome esatto del file
                self.nome_file = os.path.basename(f.name)
                    
                indice_tab = self.notebook.index(self.notebook.select())
                self.notebook.forget(indice_tab)

                self.notebook.add(self.frame,text= self.nome_file)

                self.scrolledtxt.delete(1.0, END) 
                self.scrolledtxt.insert(END, self.dati) 
        except AttributeError and FileNotFoundError:
            messagebox.showerror(title="Errore", message="Non è stato indicato nessun file")







        
    

    #metodo per fare in modo che quando viene premuto il tasto Esci nella menu bar di file la finestra root venga chiusa
    def esci(self):
        self.root.destroy()



    #metodo per fare in modo che quando viene premuto il tasto Nuova Scheda nella menu bar di file venga effettivamente aggiunta come tab
    def nuova_scheda(self, event = None):
        self.frame = Frame(self.notebook)
        self.frame.pack(fill=BOTH, expand=True)
        self.notebook.add(self.frame, text="Nuova Scheda")

        self.scrolledtxt = scrolledtext.ScrolledText(self.frame)
        self.scrolledtxt.pack(fill=BOTH, expand=True)

        

    #metodo per fare in modo che quando viene premuto il tasto Rimuovi Tab comparso una volta cliccato il tasto destro sulla tab la elimini effettivamente dal notebook
    def rimuovi_tab(self, event = None):


        

        
        
        #Prendiamo l'indice della tab selezionata con il tasto destro
        self.indice_tab = self.notebook.index(self.notebook.select())

        #Contiamo il numero di tab che ci sono all'interno del notebook
        self.numero_tabs = len(self.notebook.tabs())

        self.salvaPrimaDiUscire()



        #Se la tab selezionata non è la prima e se  il numero di tabs è più di una rimuove la tab altrimenti chiude la root
        if self.indice_tab > 0 or self.numero_tabs > 1:
            self.notebook.forget(self.indice_tab)
            
        else:
            self.root.destroy()

        

        
        

    #Metodo che ci consente di chiedere all'utente se vuole effettivamente chiudere la tab prima di salvare
    def salvaPrimaDiUscire(self):

        #ricaviamo il contenuto della tab
        self.contenuto = self.scrolledtxt.get("1.0",END)




        #Prendiamo il nome della tab
        self.nomeTab = self.notebook.tab(self.indice_tab, option="text")



        #Se abbiamo scritto qualcosa e non abbiamo ancora salvato, prima di chiudere viene chiesto all'utente se vuole salvare
        if self.contenuto == "\n" and self.nomeTab == "Nuova Scheda":
            self.notebook.forget(self.indice_tab)
        else:
            self.risposta = messagebox.askyesnocancel(title="Blocco Note", message="Vuoi salvare le modifiche prima di uscire?")

            if self.risposta:
                self.salva_con_nome()
            elif self.risposta is False:
                
                self.root.destroy()



    #Metodo che ci consente di incollare una volta cliccato il tasto nel menu Modifica
    def incolla(self):
        self.scrolledtxt.event_generate("<<Paste>>")


    #Metodo che ci consente di copiare una volta cliccato il tasto nel menu Modifica
    def copia(self):
        self.scrolledtxt.event_generate("<<Copy>>")


    #Metodo che ci consente di Tagliare una volta cliccato il tasto nel menu Modifica
    def taglia(self):
        self.scrolledtxt.event_generate("<<Cut>>")





    #Metodo che ci consente di zoommare con la rotella
    def zoomRotella(self,event = None):
        if event.delta > 0:
            self.zoom_in(None)
        elif event.delta < 0:
            self.zoom_out(None)



    #Metodo che ci consente di fare uno zoom avanti
    def zoom_in(self,event = None):
        self.dim_font += 2
        self.AggiornaFont()

    #Metodo che ci consente di fare uno zoom indietro
    def zoom_out(self,event = None):
        if self.dim_font > 2:
            self.dim_font-=2
        self.AggiornaFont()

    #Metodo che ci consente di tornare alle impostazione di default
    def ResetZoom(self,event = None):
        self.dim_font = 12
        self.AggiornaFont()


    #Metodo per aggiornare costantemente le dimensioni del font e permetterci di zoommare
    def AggiornaFont(self):
    
        self.font_corrente.configure(size=self.dim_font)
        self.scrolledtxt.configure(font=self.font_corrente)






    #metodo che ci consente di aprire un menu contestuale
    def ctx_menu_popup(self,event):
        try:
            self.ctx_menu.tk_popup(event.x_root,event.y_root)
        finally:
            self.ctx_menu.grab_release()

       

    







#Se l'attributo nome è main cioè se questo file non è stato importato come modulo crea un istanza della classe
if __name__ == "__main__":
    bn = BloccoNote()























