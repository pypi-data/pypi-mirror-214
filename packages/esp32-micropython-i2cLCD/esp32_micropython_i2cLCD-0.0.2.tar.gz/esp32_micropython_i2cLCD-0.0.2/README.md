# I2C LCD micropython esp32

import

    from LCD.lcd import LCD1602
    
    LCD = LCD1602(scl=12, sda=14)
    #LCD1602(scl, sda, num_lines=None, num_columns=None, freq=None):

print
    
    LCD.puts('teste',x=0,y=1)
    #y 0~1
    #x 0~15

print txt

    from time import sleep
    
    LCD.println(['1','2','3','4','5'])
    
    x = 2
    while True:
        sleep(1)
        LCD.println(linha=x)
        x+=1

    #linha == line for txt(list)

for txt

    from time import sleep
    
    LCD.println('1 \n 2 \n 3 \n 4 \n 5')

    x = 2
    while True:
        sleep(1)
        LCD.println(linha=x)
        x+=1

print choices

    from time import sleep
    
    LCD.escolhas('txtprincipal', 0, ['1','2','3','4','5'])
    
    x = 1
    while True:
        sleep(1)
        LCD.escolhas(posicao=x)
        if x == 3:
            print(LCD.escolhas(select=True))
            break
        x+=1

lcd clear

    LCD.clear()
    
lcd print in line

    LCD.putsln(['line 0', 'line 1'])

especial char

    from time import sleep
    
    b = bytearray([0x04,0x0A,0x04,0x0A,0x04,0x0A,0x04,0x0A])
    
    LCD.char(0,b)
    
    v = ' 1 \n 2 \n 3 \n 4 \n 5 \n '+chr(0)
    # or v = ['1','2','3','4','5',chr(0)]
    
    LCD.println(v)
    
    x = 2
    while True:
        sleep(1)
        LCD.println(linha=x)
        x+=1

    #linha == line for txt(list)

lcd hal backlight

    LCD.hal_backlight()

lcd blink

    LCD.brilhe(local=[1,1])
    # or lcd not blink LCD.brilhe(False) 

lcd animation for clear line
    
    LCD.apagarlinha(1)