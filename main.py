from random import randint
import tkinter as tk
from datetime import timedelta
import time


def init_grille(m, n, n_mines):  # m = Oy, n = Ox
    _grille = [[0 for j in range(n)] for i in range(m)]

    while n_mines > 0:
        c_mine = randint(0, m - 1), randint(0, n - 1)
        if type(_grille[c_mine[0]][c_mine[1]]) == int:
            _grille[c_mine[0]][c_mine[1]] = "X"
            n_mines -= 1

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 <= c_mine[0] + x < m and 0 <= c_mine[1] + y < n and type(_grille[c_mine[0] + x][c_mine[1] + y]) == int:
                        _grille[c_mine[0] + x][c_mine[1] + y] += 1
    return _grille


def init_grille_joueur(m, n):  # m = Oy, n = Ox
    return [[0 for j in range(n)] for i in range(m)]


def fenetre_principale():
    _root = tk.Tk()
    _root.title("Démineur")
    _root.geometry(str(N * LARGEUR_CASE + right_margin * 3) + "x" + str(M * HAUTEUR_CASE + top_margin * 2) + "+500+100")
    _label_b = tk.Label(_root, foreground="red", text=(str(N_MINES) + chr(128163)), font=20)
    _label_b.grid(column=0, row=0)
    _label_t = tk.Label(_root, foreground="red", text="0.0", font=20)
    _label_t.grid(column=1, row=0)
    _heure_debut_partie = time.time()
    return _root, _label_b, _label_t, _heure_debut_partie


def init_canvas(m, n, _root):  # m = Oy, n = Ox
    canvas = tk.Canvas(_root, width=N * LARGEUR_CASE + right_margin * 2, height=M * HAUTEUR_CASE + top_margin)
    canvas.bind('<Button-1>', clic_gauche)
    canvas.bind('<Button-3>', clic_droit)
    liste_rec = []
    for i in range(m):
        for j in range(n):
            liste_rec.append(
                canvas.create_rectangle(right_margin + j * LARGEUR_CASE, top_margin + i * HAUTEUR_CASE, right_margin + (j + 1) * LARGEUR_CASE, top_margin + (i + 1) * HAUTEUR_CASE, fill="grey",
                                        outline="lightgrey", width=2))
    canvas.grid(column=1, row=1)
    return canvas, liste_rec


def get_case(x, y):  # x = Ox, y = Oy
    overlap = canevas.find_overlapping(x, y, x, y)
    if len(overlap) > 0:
        return ((min(overlap) - 1) % N), (min(overlap) - 1) // N
    return -1, -1


def creuser(i, j):  # i = Ox, j = Oy
    if grille_joueur[j][i] == 0:
        canevas.itemconfig(j * N + i + 1, fill="white")
        if grille[j][i] == "X":
            canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text=chr(128163), font=25)  # font='Wingdings'
            return stop_and_print(False)
        grille_joueur[j][i] = -1
        if grille[j][i] == 0:
            [[creuser(i + x, j + y) for y in range(-1, 2) if 0 <= i + x < N and 0 <= j + y < M and grille[j + y][i + x] != "X" and grille_joueur[j + y][i + x] == 0] for x in range(-1, 2)]
        elif grille[j][i] == 1:
            canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text="1", fill="blue")
        elif grille[j][i] == 2:
            canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text="2", fill="green")
        elif grille[j][i] > 2:
            canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text=grille[j][i], fill="red")
        return test_gagne()


def drapeau(i, j):  # i = Ox, j = Oy
    global nb_drapeau
    if grille_joueur[j][i] == 0 and nb_drapeau < N_MINES:
        grille_joueur[j][i], nb_drapeau = 1, nb_drapeau + 1
        canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text=chr(80), fill="orange", font=("Wingdings", 20), tags=str(i) + ';' + str(j))
    elif grille_joueur[j][i] == 1:
        grille_joueur[j][i], nb_drapeau = 0, nb_drapeau - 1
        canevas.delete(str(i) + ';' + str(j))
    test_gagne()


def clic_gauche(event):
    x, y = get_case(event.x, event.y)
    if x != -1 and y != -1:
        creuser(x, y)


def clic_droit(event):
    x, y = get_case(event.x, event.y)
    if x != -1 and y != -1:
        drapeau(x, y)


def maj_labels():
    global end
    if not end:
        label_bombe["text"] = (str(N_MINES - nb_drapeau) + chr(128163))
        label_temp["text"] = (str(timedelta(seconds=int(time.time() - heure_debut_partie)))[2:])
        root.after(100, maj_labels)


def test_gagne():
    for i in range(M):
        for j in range(N):
            if grille_joueur[i][j] == 0:
                return False
    return stop_and_print(True)


def stop_and_print(gagne):
    global end
    end = True
    if gagne:
        init_end_label("Vous avez gagné !")
    else:
        [[canevas.create_text(right_margin + i * LARGEUR_CASE + LARGEUR_CASE / 2, top_margin + j * HAUTEUR_CASE + HAUTEUR_CASE / 2, text=chr(128163), font=25) for i in range(N) if grille[j][i] == "X"] for j in range(M)]
        init_end_label("Vous avez perdu !")
    canevas.unbind('<Button-1>')
    canevas.unbind('<Button-3>')


def init_end_label(msg):
    global root
    _label = tk.Label(root, foreground="red", text=msg, font=20)
    _label.grid(column=1, row=2)
    btn1 = tk.Button(root, text="Rejouer", command=root.destroy)
    btn2 = tk.Button(root, text="Quitter", command=quitter)
    btn1.grid(column=1, row=3)
    btn2.grid(column=0, row=3)


def quitter():
    global restart, root
    restart = False
    root.destroy()


def choice_user():
    global M, N, N_MINES
    _root_user = tk.Tk()
    _root_user.title("Initialisation Démineur")
    tk.Label(_root_user, text="Hauteur").grid(row=0)
    tk.Label(_root_user, text="Largeur").grid(row=1)
    tk.Label(_root_user, text="Nombre de mines").grid(row=2)
    tk.Label(_root_user, text="Largeur des cases").grid(row=3)
    tk.Label(_root_user, text="Hauteur des cases").grid(row=4)

    _input = [tk.Entry(_root_user) for i in range(5)]
    [j.insert(10, "10") for j in _input]
    [_input[k].grid(row=k, column=1) for k in range(5)]

    tk.Button(_root_user, text='Jouer', command=set_values).grid(row=5, column=0)
    return _root_user, _input


def set_values():
    global M, N, N_MINES, root_user, user_input, LARGEUR_CASE, HAUTEUR_CASE
    M, N, N_MINES, LARGEUR_CASE, HAUTEUR_CASE = int(user_input[0].get()), int(user_input[1].get()), int(user_input[2].get()), int(user_input[3].get()), int(user_input[4].get())
    root_user.destroy()


### Main Program ###
restart = True
while restart:
    M, N, N_MINES, LARGEUR_CASE, HAUTEUR_CASE, top_margin, right_margin = 10, 10, 10, 25, 25, 100, 50
    nb_drapeau, end = 0, False
    root_user, user_input = choice_user()
    root_user.mainloop()

    grille = init_grille(M, N, N_MINES)
    grille_joueur = init_grille_joueur(M, N)
    root, label_bombe, label_temp, heure_debut_partie = fenetre_principale()
    canevas, grille_canevas = init_canvas(M, N, root)

    root.after(100, maj_labels)
    root.mainloop()