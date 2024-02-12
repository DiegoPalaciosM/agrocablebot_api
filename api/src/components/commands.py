
def dateFormat(dates):
    return list(date.strftime('%Y-%m-%d %H:%M:%S') for date in dates)
    #return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def getIndex1(pos):
    matriz = []
    for index in range (4,-5, -1):
        matriz.append(list([n*100, index*100] for n in list(range(-4,5))))
    for y in matriz:
        for x in y:
            if ([pos['x'], pos['y']]) == x:
                i = y.index(x) + 9*matriz.index(y)
                return i
        
def getIndex(pos):
    aux = {}
    for key,value in pos.items():
        aux[key] = value/100
    # -4, 4 = 0
    # -4, -4 = 72
    # 4, 4 = 8
    # 4, -4 = 80
    data = None
    data = ((aux['x'] + 4) + ((-aux['y'] + 4) * 9))
    return data
