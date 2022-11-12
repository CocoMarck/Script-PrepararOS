'''Modulo de prueba para usar en mis programas jejej'''

import os, platform

def System(opc = 'System'):
    '''Comandos de sistema utiles'''
    cmd = ''
    if opc == 'System':
        '''Devuelve el sistema operativo'''
        cmd = platform.system()
        if cmd == 'Windows': cmd = 'win'
        elif cmd == 'Linux': cmd = 'linux'
        else: cmd = 'linux' #(Mac)

    elif opc == 'CleanScreen':
        '''Limpia el texto/comandos que se muestren en la terminal'''
        sys = System('System')
        if sys == 'linux':
            os.system('clear')
        elif sys == 'win':
            os.system('cls')
        else: pass

    elif opc == 'ShowArchive':
        '''Muestra los archivos existentes en una ruta'''
        sys = System('System')
        if sys == 'linux':
            os.system('ls')
        elif sys == 'win':
            os.system('dir')
        else: pass

    else: pass


    return cmd

def CleanScreen():
    System('CleanScreen')


sys = System()


def Show(opc = 'Title', txt = '', smb = '#', see = True, spc = 4):
    '''Mostrar un texto predefinido'''
    if opc == 'Title':
        '''Mostrar un titulo'''
        spc = ' '*spc
        txt = f'{smb}{spc}{txt}{spc}{smb}'
        if see == True:
            print(txt)
        elif see == False:
            txt += '\n'
        else:
            pass

    elif opc == 'Separator':
        '''Para separar texto'''
        txt = smb*spc
        if see == True:
            print(txt)
        elif see == False:
            txt += '\n'
        else:
            pass

    else: txt = ''


    return txt

def Title(txt='', smb = '#', see = True, spc = 4):
    txt = Show(opc='Title', txt=txt, smb=smb, see=see, spc=spc)
    return txt

def Separator(smb = '#', see = True, spc = 128):
    txt = Show(opc='Separator', smb=smb, see=see, spc=spc)
    return txt

def Continue(txt='¿Continuar?', lang = 'español', msg = False, sys=sys):
    idm = ['']*2
    if lang == 'español': idm[0], idm[1] = 's', 'n'
    elif lang == 'english': idm[0], idm[1] = 'y', 'n'
    else: idm[0], idm[1] = '', ''

    if msg == False:
        opc = input(f'{txt} {idm[0]}/{idm[1]}: ')
        if opc == 's': System('CleanScreen')
        elif opc == 'n': System('CleanScreen')
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
    if nme == '':
        nme ='No_name'
    else: pass
    CleanScreen()
    return nme

def Path(txt = 'Ruta', sys=sys):
#    pth = ''
    CleanScreen()
    pth_fin = ''
    opc = input(Title(txt=txt, see=False) +
        "¿Elegir ruta? s/n: ")
    if sys == 'linux':
        pth_fin = '/'

        if opc == "s":
            pth = input("Escribe la ruta: ")
        else: pth = "$HOME/"

    elif sys == 'win':
        pth_fin = '\\'

        if opc == "s":
            pth = input("Escribe la ruta: ")
        else:
            pth = (os.path.join(os.path.join(os.environ['USERPROFILE']),
                   'Desktop'))

    else: pth = ''

    if pth == '':
        if sys == 'win':
            pth = (os.path.join(os.path.join(os.environ['USERPROFILE']),
                   'Desktop'))
        elif sys == 'linux': pth = '$HOME/'
        else: pass

    try: pth_laststr = pth[-1]
    except: pth_laststr = pth_fin
    if pth_laststr == pth_fin: pass
    else:        
        pth = pth + pth_fin

    CleanScreen()
    return pth