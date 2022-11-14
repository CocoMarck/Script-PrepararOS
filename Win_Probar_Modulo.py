import os, pathlib
import Modulo_Util as Util


def ScriptWin_Menu():
    loop = True
    while loop == True:
        Util.System('CleanScreen')
        
        txt = (Util.Title('Generar Script para Windows', see=False) + 
               Util.Title('(Opciones)', spc = 8, see=False) +
               '1. Continuar\n'
               '0. Salir\n'
               'Opción: ')
        
        opc = input(txt)

        ctn = Util.Continue()
        if ctn == 's': pass
        elif ctn == 'n': opc = 'continue'
        
        if opc == '1':
            input('Continuando...')
        
        elif opc == '0':
            loop = False
            input('Saliendo...')
            
        elif opc == 'continue':
            pass
            
        else: Util.Continue(msg=True)
        
if __name__ == '__main__':
    ScriptWin_Menu()