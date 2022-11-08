'''Modulo de prueba para usar en mis programas jejej'''

import os, platform

def System():
    sys = platform.system()
    if sys == 'Windows': sys = 'win'
    elif sys == 'Linux': sys = 'linux'
    else: sys = 'linux'
    return sys

sys = System()

def Title(txt = '', smb = '#', see = True, spc = 4):
    '''Mostrar un titulo'''
    spc = ' '*spc
    txt = f'{smb}{spc}{txt}{spc}{smb}'
    if see == True:
        print(txt)
    elif see == False:
        txt += '\n'
    else:
        pass
    return txt

def CleanScreen(sys=sys):
    '''Limpiar pantalla'''
    if sys == 'linux':
        os.system('clear')
    elif sys == 'win':
        os.system('cls')
    else: pass

def Separator(spc = 128, smb = '#', see = True, sys=sys):
    '''Separar texto'''
    txt = smb*spc
    if see == True:
        print(txt)
    elif see == False:
        txt += '\n'
    else:
        pass
    return txt

def Continue(txt='¿Continuar?', lang = 'español', msg = False, sys=sys):
    idm = ['']*2
    if lang == 'español': idm[0], idm[1] = 's', 'n'
    elif lang == 'english': idm[0], idm[1] = 'y', 'n'
    else: idm[0], idm[1] = '', ''

    if msg == False:
        opc = input(f'{txt} {idm[0]}/{idm[1]}: ')
        if opc == 's': CleanScreen(sys)
        elif opc == 'n': CleanScreen(sys)
        elif opc == '':
            print('No escribiste nada')
            opc = Continue(txt=txt, lang=lang)
        else: 
            print(f'"{opc}" No existe')
            opc = Continue(txt=txt, lang=lang)
    else:
        opc = ''
        input(f'La opcion "{txt}" no existe\n'
              'Precione enter para continuar...')
        
    return opc

def Name(txt = 'Archivo', sys=sys):
    nme = input(Title(txt=f'Nombre de {txt}', see=False) +
              'Nombre: ')
    CleanScreen(sys)
    return nme

def Path(txt = 'Ruta', sys=sys):
#    pth = ''
    CleanScreen(sys)
    pth_fin = ''
    opc = input(Title(txt=txt, see=False) +
        "¿Elegir ruta? s/n: ")
    if sys == 'linux':
        pth_fin = '/'

        if opc == "s":
            pth = input("Escribe la ruta: ")
        else:
            pth = "$HOME/"
    elif sys == 'win':
        pth_fin = '\\'

        if opc == "s":
            pth = input("Escribe la ruta: ")
        else: pth = ''

    else: pth = ''

    try: pth_laststr = pth[-1]
    except: pth_laststr = pth_fin
    if pth_laststr == pth_fin: pass
    else:        
        pth = pth + pth_fin

    CleanScreen(sys)
    return pth