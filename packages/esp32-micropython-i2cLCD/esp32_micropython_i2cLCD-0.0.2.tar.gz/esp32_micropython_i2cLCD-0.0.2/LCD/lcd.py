from utime import sleep_ms
from LCD.i2c_lcd import I2cLcd
from time import sleep


class LCD1602():
    def __init__(self, scl, sda, num_lines=2, num_columns=16, freq=None):
        self.hal_backlightvalue = True
        self.posi = None
        self.escolha = []
        self.lcd = I2cLcd(scl, sda, num_lines, num_columns, freq)
        self.txt = None
        self.txtprincipal = None
        self.posicao = None

    def clear(self):
        self.txt = None
        self.txtprincipal = None
        self.posi = None
        self.posicao = None
        self.escolha = []
        self.lcd.clear()

    def puts(self, txt, x=0, y=0, desactive_auto=True, moveto=None):
        return self.lcd.puts(txt, x, y, desactive_auto, moveto)

    def list_to_txt(self):
        lista = []
        for i in self.txt:
            for it in i:
                if len(it) > 16:
                    x = 1
                    st = ''
                    for char in it:
                        if len(st) == 16:
                            lista.append(st)
                            st = ''
                        st += char
                        x += 1
                    if len(st) > 0:
                        lista.append(st)
                else:
                    lista.append(it)
        self.txt = lista

    def notlist_to_txt(self):
        lista = []
        st = ''
        x = 1
        for char in self.txt:
            print(char)
            if char == '\n':
                if st != '':
                    lista.append(st)
                    st = ''
                lista.append('')
            else:
                if len(st) < 16:
                    st += char
                else:
                    lista.append(st)
                    st = char
            if len(self.txt) == x and len(st) < 16:
                lista.append(st)
            x += 1
        if len(lista) == 1:
            lista.append('')
        print(lista)
        self.txt = lista

    def println(self, txt=None, linha=1):
        if txt is not None:
            self.txt = txt
            if isinstance(txt, str):
                self.notlist_to_txt()
            elif isinstance(txt, list):
                self.list_to_txt()
        elif self.txt is None:
            self.txt = [''] * 2

        numlinhas = len(self.txt) - 1

        if linha > numlinhas:
            linha = numlinhas
        elif linha < 0:
            linha = 0

        self.putsln([self.txt[linha - 1] + " " * (16 - len(self.txt[linha - 1])),
                     self.txt[linha] + " " * (16 - len(self.txt[linha - 1]))])
        sleep_ms(3)

    def putsln(self, txt):
        if txt:
            self.puts(txt[0] + " " * (16 - len(txt[0])))
            self.puts(txt[1] + " " * (16 - len(txt[1])), 0, 1)

    def posicao(self, value=None):
        if value:
            self.posi = value
        else:
            return self.posi

    def apagarlinha(self, y):
        self.lcd.apagar_linha(y)

    def brilhe(self, n=True, local=None):
        self.lcd.brilhe(n, local)

    def escolhas(self, txtprincipal=None, posicao=None, escolhas=None, select=None):
        if posicao:
            self.posicao = posicao
        else:
            if not self.posicao:
                self.posicao = 0

        if txtprincipal is not None:
            self.txtprincipal = txtprincipal
        self.puts(self.txtprincipal + " " * (16 - len(self.txtprincipal)))
        if escolhas:
            self.escolha = escolhas
        if self.posicao > len(self.escolha) - 1:
            self.posicao = 0
        elif self.posicao < 0:
            self.posicao = len(self.escolha) - 1
        self.puts(str(self.escolha[self.posicao]) + " " * (16 - len(str(self.escolha[self.posicao]))), y=1)
        if select:
            re = self.escolha[self.posicao]
            self.clear()
            return re

    def char(self, location, charmap):
        self.lcd.custom_char(location, charmap)

    def hal_backlight(self):
        self.hal_backlightvalue = not self.hal_backlightvalue
        if self.hal_backlightvalue:
            self.lcd.hal_backlight_on()
        else:
            self.lcd.hal_backlight_off()
        return self.hal_backlightvalue