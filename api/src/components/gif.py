import imageio.v2 as imageio
import os

def exportGif(name, nprueba, path):
    names = os.listdir(f"{path}/{nprueba}/fotos/{name}")
    names.sort()
    images = []
    for n in names:
        images.append(imageio.imread(f"{path}/{nprueba}/fotos/{name}/{n}"))
    imageio.mimsave(f'{path}/{nprueba}/fotos/{name}.gif', images)

def exportGif2(name, nprueba):
    names = os.listdir(f"data/{nprueba}/screenshots/{name}_test")
    names.sort()
    images = []
    names = list([int(name.split('_')[0].strip('x'))/100, int(name.split('_')[1].strip('y'))/100] for name in names)
    for n in names:
        images.append(imageio.imread(f"data/{nprueba}/screenshots/{name}_test/{n}"))
    imageio.mimsave(f'data/{nprueba}/screenshots/{name}.gif', images)

def changeNames():
    names = os.listdir(f"data/1/screenshots/above_test")
    names.sort()
    namesEdited = []
    X = ''
    Y = ''
    for name in names:
        aux = name.split('_')
        os.rename(f"data/1/screenshots/above_test/{name}", f"data/1/screenshots/above_test/{'_'.join([aux[1], aux[2]])}")

    print (namesEdited)


#exportGif('above', 1)