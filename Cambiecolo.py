import sys
import threading
import random
import concurrent.futures
from multiprocessing import Process, Manager, Array, Queue, Lock
import time
import queue
import msvcrt
import pygame





def jeuJoueur (i, jeu, offres, jeuDeCarte , l, q):
    global offreEnCours
    offreEnCours=True
    global mainJoueur
    l.acquire()
    mainJoueur = []
    for k in range(len(jeuDeCarte)):
        if jeuDeCarte[k][1]==i[0]:
            mainJoueur.append((jeuDeCarte[k][0],k))
    l.release()
    print(mainJoueur)
    for i in range(10):
        if offreEnCours == False:
            if q[i[0]].qsize() != 0:
                q[i[0]].get()
                l.acquire()
                mainJoueur = []
                for k in range(len(jeuDeCarte)):
                    if jeuDeCarte[k][1]==i[0]:
                        mainJoueur.append((jeuDeCarte[k][0],k))
                l.release()
                offreEnCours = False
'''
        else :
            l.acquire()
                q[numJoueur].put(1)
            l.release()

        if gagne():
            jeu[0] = False'''




def affichage(i, jeu, offres, jeuDeCarte , l, q):
    print(i[0])
    time.sleep(1)
    (width, height) = (1300,750)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    background_colour = (0,128,0)
    pygame.display.set_caption('Joueur '+str(i[0]))
    screen.fill(background_colour)

    color_light = (170,170,170)
    color_dark = (100,100,100)
    smallfont = pygame.font.SysFont('Corbel',35)
    text = smallfont.render('Mettre Offre' , True , (255,255,255))
    text2 = smallfont.render('Annuler Offre' , True , (255,255,255))
    text3 = smallfont.render('Joueur 0 : ' , True , (255,255,255))
    text4 = smallfont.render('Joueur 1 : ' , True , (255,255,255))
    text5 = smallfont.render('Joueur 2 : ' , True , (255,255,255))
    text6 = smallfont.render('Offres disponibles' , True , (255,255,255))

    pygame.display.flip()

    cpt=0
    l.acquire()
    for k in range(5):
        carte = pygame.image.load(str(mainJoueur[k][1])+".png").convert_alpha()
        pygame.display.get_surface().blit(carte, [50 + k*245,455,195,295])
        rectangle = pygame.Rect(50 + k*245,455,195,295)
        pygame.display.update(rectangle)
    l.release()



    selection=[]
    tailleJ=[0,0,0]
    running = True
    while running:
        l.acquire()
        for h in range(3):
            v=-1
            for w in range(len(offres)):
                if offres[w][2]==h:
                    v=w
                    break
            if v==-1:
                tailleJ[h]=0
            else:
                tailleJ[h]=len(offres[v][1])
        l.release()
        text7 = smallfont.render(str(tailleJ[0])+' cartes' , True , (255,255,255))
        text8 = smallfont.render(str(tailleJ[1])+' cartes' , True , (255,255,255))
        text9 = smallfont.render(str(tailleJ[2])+' cartes' , True , (255,255,255))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(5):
                    if (50 + k*245) <= mouse[0] <= (50 + k*245)+195 and 455 <= mouse[1] <= 455+295:
                        a=False
                        l.acquire()
                        for j in range(len(selection)):
                            if selection[j]==mainJoueur[k][1]:
                                selection.pop(j)
                                a=True
                                print(selection)
                                break
                        if a==False:
                            selection.append(mainJoueur[k][1])
                            print(selection)
                        l.release()
                        a=True

                if 1000 <= mouse[0] <= 1000+225 and 100 <= mouse[1] <= 100+45:
                    if len(selection) == 0:
                        pass
                    else:
                        l.acquire()
                        offres.append((0, selection, i[0]))
                        print(offres)
                        l.release()
                        slection=[]

                if 1000 <= mouse[0] <= 1000+225 and 200 <= mouse[1] <= 200+45:
                    l.acquire()
                    if offreEnCours == False:
                        pass
                    else:
                        for v in range(len(offres)):
                            if offres[v][2]==i[0]:
                                offres.pop(v)
                    print(offres)
                    l.release()


        if 1000 <= mouse[0] <= 1000+225 and 100 <= mouse[1] <= 100+45:
            pygame.draw.rect(screen,color_light,[1000,100,225,45])
        elif 1000 <= mouse[0] <= 1000+225 and 200 <= mouse[1] <= 200+45:
            pygame.draw.rect(screen, color_light, [1000, 200, 225, 45])
        elif 200 <= mouse[0] <= 200+225 and 120 <= mouse[1] <= 120+45:
            pygame.draw.rect(screen, color_light, [200, 120, 200, 45])
        elif 200 <= mouse[0] <= 200+225 and 190 <= mouse[1] <= 190+45:
            pygame.draw.rect(screen, color_light, [200, 190, 200, 45])
        elif 200 <= mouse[0] <= 200+225 and 260 <= mouse[1] <= 260+45:
            pygame.draw.rect(screen, color_light, [200, 260, 200, 45])
        else:
            pygame.draw.rect(screen,color_dark,[1000,100,225,45])
            pygame.draw.rect(screen,color_dark,[1000,200,225,45])
            pygame.draw.rect(screen, color_dark, [200, 260, 200, 45])
            pygame.draw.rect(screen, color_dark, [200, 190, 200, 45])
            pygame.draw.rect(screen, color_dark, [200, 120, 200, 45])

        screen.blit(text ,(1000+25,105))
        screen.blit(text2 ,(1000+25,205))
        screen.blit(text6 ,(75,55))
        screen.blit(text3 ,(40,125))
        screen.blit(text4,(40,195))
        screen.blit(text5 ,(40,265))
        screen.blit(text7 ,(225,125))
        screen.blit(text8 ,(225,195))
        screen.blit(text9 ,(225,265))

        pygame.display.update()





def joueur (i, jeu, offres, jeuDeCartes, l, q):
    t1 = threading.Thread(target=affichage, args=([i], jeu, offres, jeuDeCartes, l, q))
    t2 = threading.Thread(target=jeuJoueur, args=([i], jeu, offres, jeuDeCartes , l, q))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(offres)






if __name__ == '__main__':

    with Manager() as manager:
        jeuDeCartes = manager.list([[0, 0], [0, 1], [0, 2], [0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1,2], [1,0], [2,0], [2,1], [2,2], [2,1],[2,2]])
        offres = manager.list([])
        l = Lock()
        jeu = manager.list([True])
        queues = [Queue() for i in range(3)]
        p = [Process(target=joueur, args=(i, jeu, offres, jeuDeCartes, l, queues,)) for i in range(3)]
        for i in range(3):
            p[i].start()
        for i in range(3):
            p[i].join()
