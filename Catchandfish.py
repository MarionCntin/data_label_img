# Bibliothèque

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
import cv2
import PIL.Image, PIL.ImageTk
import os
import shutil


##### WINDOW ######
# Fenetre principale
fenetre = Tk()
fenetre.geometry("620x600")
fenetre.title("Logiciel")
P = PanedWindow(fenetre, orient=VERTICAL)
P.pack(side=TOP, expand=Y, fill=BOTH)

# Variable
global fish_name

video = StringVar()
video.set(None)

stockage_file = StringVar()
stockage_file.set(os.getcwd())
os.chdir(stockage_file.get())


######### FUNCTION ######

def nom(string):
    i, a, b = 1, 0, 0
    while i < len(string):
        if string[-i] == '.':
            a = i
            while string[-i] != '/':
                i += 1
            b = i - 1
            break
        else:
            i += 1
    return string[-b:-a]


def clicRechercher():
    filepath = askopenfilename(title="Ouvrir une vidéo")
    video.set(filepath)
    label1.configure(text='Video = %s' % video.get())
    
def clicStockage():
    filepath = askdirectory(title="Choisir une destination des fichiers")
    stockage_file.set(filepath)
    labelStockage.configure(text="Destination = %s" % stockage_file.get())
    os.chdir(stockage_file.get())


def lecture_labellisation():
    global fish_name
    global choix
    global stockage_file
    # Lecture of the capture
    if video.get() == 'None' or len(video.get()) == 0:
        showinfo("Alerte", "Choissisez une vidéo")
        return False,

    cap = cv2.VideoCapture(video.get())

    # Waiting for opening
    while not cap.isOpened():
        cap = cv2.VideoCapture(video.get())
        cv2.waitKey(1000)
        print("Wait for the header")

    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    cpt_frame = 0
    while True:
        flag, frame = cap.read()
        if cpt_frame % int(custom.get()) == 0:
            if flag:

                # The frame is ready and already captured
                pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                print(str(pos_frame) + " frames")


                cv2.imshow('video', frame)

                def stay_f():
                    global choix
                    choix = 's'
                    choix_frame.quit()
                    choix_frame.withdraw()

                def next_f():
                    global choix
                    choix = 'n'
                    choix_frame.quit()
                    choix_frame.withdraw()

                def close_selection():
                    global choix
                    choix = 'c'
                    choix_frame.quit()
                    choix_frame.withdraw()


                #choix = 's'

                choix_frame = Toplevel(fenetre, height=100, width=400)
                action_suivante = Label(choix_frame, text="Que voulez-vous faire?")
                stay_frame = Button(choix_frame, text="Faire une sélection sur cette frame", command=stay_f)
                next_frame = Button(choix_frame, text="Frame suivante", command=next_f)
                stop_selection = Button(choix_frame, text="Arrêter la sélection", command=close_selection)
                action_suivante.pack(side=TOP)
                stay_frame.pack(side=LEFT)
                next_frame.pack(side=RIGHT)
                stop_selection.pack(side=BOTTOM)

                choix_frame.mainloop()




                while choix == "s":

                    fenetre.withdraw()

                    r = cv2.selectROI('video', frame, fromCenter=False, showCrosshair=False)
                    imgCrop = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                    coord_L, coord_R = r[0] + r[2], r[1] - r[3]

                    win = Toplevel(fenetre)
                    value = StringVar()
                    value.set("Nom du poisson")
                    entree = Entry(win, textvariable=value, width=30)
                    entree.pack()

                    def recupere():
                        global fish_name
                        fish_name = entree.get()
                        showinfo("Alerte", '%s a bien été ajouté !' % entree.get())
                        win.quit()

                    ajouter = Button(win, text="Ajouter", command=recupere)
                    ajouter.pack()
                    win.mainloop()

                    video_ref = nom(video.get())

                    cv2.imwrite('{NomPoisson}_{position}_{VideoRef}_{coord_1}_{coord_2}.jpg'.format(VideoRef=video_ref,
                                                                                                    NomPoisson=fish_name,
                                                                                                    position=pos_frame,
                                                                                                    coord_1=coord_L,
                                                                                                    coord_2=coord_R),
                                imgCrop)
                    if not os.path.exists(fish_name):
                        os.makedirs(fish_name)
                    dest = os.path.abspath('%s' %fish_name)
                    file = os.path.abspath('{NomPoisson}_{position}_{VideoRef}_{coord_1}_{coord_2}.jpg'.format(VideoRef=video_ref,
                                                                                                    NomPoisson=fish_name,
                                                                                                    position=pos_frame,
                                                                                                    coord_1=coord_L,
                                                                                                    coord_2=coord_R))
                    shutil.move(file, dest)
                    win.withdraw()

                    choix_frame = Toplevel(fenetre, height=100, width=400)
                    action_suivante = Label(choix_frame, text="Que voulez-vous faire?")
                    stay_frame = Button(choix_frame, text="Faire une sélection sur cette frame", command=stay_f)
                    next_frame = Button(choix_frame, text="Frame suivante", command=next_f)
                    stop_selection = Button(choix_frame, text="Arrêter la sélection", command=close_selection)
                    action_suivante.pack(side=TOP)
                    stay_frame.pack(side=LEFT)
                    next_frame.pack(side=RIGHT)
                    stop_selection.pack(side=BOTTOM)

                    choix_frame.mainloop()




                if choix == 'c':
                    cv2.destroyAllWindows()
                    fenetre.deiconify()
                    break













            else:
                # The next frame is not ready, so we try to read it again
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame - 1)
                print("frame is not ready")
                # It is better to wait for a while for the next frame to be ready
                cv2.waitKey(1000)

            if cv2.waitKey(10) == 27:
                break
            if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - int(cap.get(cv2.CAP_PROP_POS_FRAMES)) <= 2*int(custom.get()):
                # If the number of captured frames is equal to the total number of frames,
                # we stop
                break
        cpt_frame += 1
    cv2.destroyAllWindows()
    fenetre.deiconify()



def image_viewer():
    global frame
    global my_label
    global button_forward
    global button_back
    global periode

    if video.get() == 'None' or len(video.get()) == 0:
        showinfo("Alerte", "Choissisez une vidéo")
        return False,


    video_frame = Toplevel(fenetre)
    cap = cv2.VideoCapture(video.get())

    # Création de la liste de frame
    frame_list = []
    cpt_frame = 0
    while True:
        _, frame = cap.read()
        cpt_frame += 1

        if frame is None:
            break

        if cpt_frame % int(custom.get()) == 1:
            scale_percent = 50000/frame.shape[0]
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            frame_resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_resized))
            frame_list.append(photo)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    my_label = Label(video_frame, image=frame_list[0])

    my_label.pack(side=TOP)

    def forward(frame_number):
        global my_label
        global cmd

        cmd.destroy()
        barre_cmd()

        my_label.pack_forget()
        my_label = Label(video_frame, image=frame_list[frame_number - 1])
        button_forward = Button(cmd, text=">>", command=lambda: forward(frame_number + 1))
        button_back = Button(cmd, text="<<", command=lambda: back(frame_number - 1))

        if frame_number == len(frame_list):
            button_forward = Button(video_frame, text=">>", state=DISABLED)

        my_label.pack(side=TOP)

        button_forward.pack(side=RIGHT)
        button_back.pack(side=LEFT)

    def back(frame_number):
        global my_label
        global cmd

        cmd.destroy()
        barre_cmd()

        my_label.pack_forget()
        my_label = Label(video_frame, image=frame_list[frame_number - 1])
        button_forward = Button(cmd, text=">>", command=lambda: forward(frame_number + 1))
        button_back = Button(cmd, text="<<", command=lambda: back(frame_number - 1))

        if frame_number == 1:
            button_back = Button(video_frame, text="<<", state=DISABLED)

        my_label.pack(side=TOP)
        button_back.pack(side=LEFT)
        button_forward.pack(side=RIGHT)

    def barre_cmd():
        global cmd
        cmd = LabelFrame(video_frame)
        button_exit = Button(cmd, text="Exit", command=video_frame.destroy)

        button_exit.pack(side=BOTTOM)

        cmd.pack(side=BOTTOM)

    barre_cmd()

    button_back = Button(cmd, text="<<", command=back)
    button_forward = Button(cmd, text=">>", command=lambda: forward(2))
    button_forward.pack(side=RIGHT)
    button_back.pack(side=LEFT)


##### WINDOW ######

# Fenetre de chargement
Chargement = LabelFrame(P, text="Chargement d'un fichier")

boutonFile = Button(Chargement, text="Rechercher vidéo", command=clicRechercher)
boutonFile.pack(pady=5)

label1 = Label(Chargement, text="Video = %s" % video.get())
label1.pack()

boutonLaunch = Button(Chargement, text="Lancer l'analyse", command=lecture_labellisation)
boutonLaunch.pack(pady=5)

P.add(Chargement)

# Fenetre de destination
PanelB = LabelFrame(P, text="Dossier de destination", width=500, height=120)

boutonFileStockage = Button(PanelB, text="Choisir le répertoire", command=clicStockage)
boutonFileStockage.pack(pady=5)

labelStockage = Label(PanelB, text="Destination = %s" % stockage_file.get())
labelStockage.pack()


PanelB.pack()
P.add(PanelB)

# Fenêtre de sélection de frames
PanelC = LabelFrame(P, text="Périodicité")

label2 = Label(PanelC, text="Afficher une frame sur")
label2.pack()

periode = StringVar()
periode.set("15")
custom = Entry(PanelC, textvariable=periode, width=15)
custom.pack()

apercu = Button(PanelC, text="Aperçu", command=image_viewer)
apercu.pack()

PanelC.pack()
P.add(PanelC)

# Fenetre d'instructions
PanelD = LabelFrame(P, text="Instructions")

etape1 = Label(PanelD, text='1. Rechercher un vidéo')
etape2 = Label(PanelD, text='2. Choisir le répertoire pour enregistrer les vidéos')
etape3 = Label(PanelD, text='3. Sélectionner une périodicité de frame, un aperçu permet de modifier au besoin')
etape4 = Label(PanelD, text="4. Lancer l'analyse")
remarque1 = Label(PanelD,
                  text='\n'+ "Remarque : Sélectionner une zone intéressante avec votre souris puis" + '\n'+ "appuyer sur la touche entrée ou espace pour labelliser l'imagette")
#remarque2 = Label(PanelD, text="Appuyer sur la touche n pour passer à la slide suivante")

etape1.pack()
etape2.pack()
etape3.pack()
etape4.pack()
remarque1.pack()
#remarque2.pack()

PanelD.pack()
P.add(PanelD)

fenetre.mainloop()
