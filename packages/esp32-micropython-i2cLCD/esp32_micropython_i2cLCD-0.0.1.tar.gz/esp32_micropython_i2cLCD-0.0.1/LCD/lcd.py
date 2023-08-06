from utime import sleep_ms
from i2c_lcd import I2cLcd
from time import sleep

class LCD1602():
    def __init__(self, scl, sda, num_lines=None, num_columns=None, freq=None):
        self.hal_backlightvalue = True
        self.posi = None
        self.txt = None
        self.escolha = []
        self.lcd = I2cLcd(scl, sda, num_lines, num_columns, freq)

    def clear(self):
        self.posi = None
        self.txt = None
        self.escolha = []
        self.lcd.clear()

    def puts(self, txt, x=0, y=0, desactive_auto=True, moveto=None):
        return self.lcd.puts(txt,x,y, desactive_auto, moveto)

    def list_to_txt(self):
        lista = []
        for i in self.txt:
            for it in i:
                if len(it) > 16:
                    x=1
                    st = ''
                    for i in it:
                        if len(st) == 16:
                            lista.append(st)
                            st = ''
                        st += i
                        x+=1
                    if len(st) > 0:
                        lista.append(st)
                else:
                    lista.append(it)
        self.txt = lista

    def notlist_to_txt(self):
        lista = []
        st = ''
        for i in self.txt:
            if i == '\n':
                lista.append('')
            else:
                if len(st) < 16:
                    st += i
                else:
                   lista.append(st)
                   st = i
        if len(lista) == 1:
            lista.append('')
        self.txt = lista


    def println(self, txt=None, linha=1):
        if txt:
            self.txt = txt
        if type(txt) == str:
            self.notlist_to_txt()
        elif txt(txt) == list:
            self.list_to_txt()
        numlinhas = len(self.txt)-2
        if linha > numlinhas:
            linha = numlinhas
        elif linha < -1:
            linha = 0
        self.putsln([self.txt[linha]+" "*(16-len(self.txt[linha])), self.txt[linha-1]+" "*(16-len(self.txt[linha-1]))])
        sleep_ms(3)

    def putsln(self, txt):
        if txt:
            self.clear()
            self.puts(txt[0])
            self.puts(txt[1],0,1)

    def posicao(self, value=None):
        if value:
            self.posi = value
        else:
            return self.posi

    def escolhas(self, txtprincipal, posicao, escolhas=None, select=None):
        self.puts(txtprincipal+" "*(16-len(txtprincipal)))
        if escolhas:
            self.escolha = escolhas
        if posicao > len(self.escolha)-1:
            posicao = 0
        elif posicao < 0:
            posicao = len(self.escolha)-1
        self.puts(str(self.escolhas[posicao])+" " * (16 - len(str(self.escolhas[posicao]))), y=1)
        if select:
            self.clear()
            return self.escolhas[posicao]

    def char(self,location, charmap):
        self.lcd.custom_char(location, charmap)

    def hal_backlight(self):
        self.hal_backlightvalue = not self.hal_backlightvalue
        if self.hal_backlightvalue:
            self.lcd.hal_backlight_on()
        else:
            self.lcd.hal_backlight_off()
        return self.hal_backlightvalue