import os

def export_svg():
    for file in os.listdir("svg"):
        if os.name == 'nt':
            command = "c:\Program Files\Inkscape\Inkscape.exe"
        else:
            command = "inkscape"
        for i in [2**a for a in range(3,8)]:
            os.system(command+"-zf "+file+" -C --export-width="+i+" --export-height="+i)
    

if __name__ == '__main__':
    export_svg()