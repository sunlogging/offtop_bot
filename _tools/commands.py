import os


def parser_command(mode: str) -> bool:
    print(mode)
    if mode == 'web':
        web()
        return False
    if mode == 'gui':
        gui()
        return False
    elif mode == 'start':
        return True
def gui():
    os.system('start .\\gui\\cpp\\gui.exe')

def web():
    os.system('start http://127.0.0.1:8088')
    try:
        os.system('node .\\gui\\node\\server.js')
    except KeyboardInterrupt:
        print('\n\n\nserver stoped')

