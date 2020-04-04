import sys, os, cv2
from PIL import Image


w, h = 30, 30
ram = 8192

def progress(value, max_value):
  final = 50
  k = int((value + 1) / max_value * 100) // (100 // final)
  sys.stdout.write('|{}{}| {}%\r'.format('#' * k, ' ' * (final - k), (k * 2)))
  if k == final:
    print('\n')
  

def BuildDat(pre_path, path, w, h, g=False):
  f = open('{}/{}.dat'.format(pre_path, path), 'w')
  i = 0
  imgs = os.listdir('{}/{}'.format(pre_path, path))
  l = len(imgs)
  print('BuildDat for {}:'.format(path))
  for i in range(l):
    if g:
      f.write('{}/{} 1 0 0 {} {}\n'.format(path, imgs[i], w, h))
    else:
      f.write('{}/{}/{}\n'.format(pre_path, path, imgs[i]))
    progress(i, l)
  f.close()
  return l


def ToGray(pre_path, path, w, h):
  i = 0
  gr_path = '{}/{}_Gr'.format(pre_path, path)
  path = '{}/{}'.format(pre_path, path)

  if os.path.exists(gr_path):
    imgs = os.listdir(gr_path)
    l = len(imgs)
    if l > 0:
      print('Removing old {}:'.format(gr_path))
    for i in range(l):
      os.remove(gr_path + '/' + imgs[i])
      progress(i, l)
  else:
    os.mkdir(gr_path)

  imgs = os.listdir(path)
  l = len(imgs)
  print('Converting {} to gray:'.format(path))
  for i in range(l):   
    gr = cv2.cvtColor(cv2.imread(path + "/" + imgs[i]), cv2.COLOR_BGR2GRAY)
    gr = cv2.resize(gr, (w, h), cv2.INTER_LINEAR)
    cv2.imwrite(gr_path+"/"+str(i)+".bmp", gr)
    progress(i, l)
  
if len(sys.argv) > 1:
  folders = sys.argv
  for i in range(1, len(folders)):
    if os.path.exists('{}/Good'.format(folders[i])) and os.path.exists('{}/Bad'.format(folders[i])):
      pre_path = folders[i].replace('\\', '/')
      print('Working with: {}'.format(pre_path))
      
      print('Set size of samples (press ENTER to set 30x30):')
      while True:
        s = input()
        if len(s) > 0:
          try:
            s = s.split()
            w, h = int(s[0]), int(s[1])
            break
          except:
            print('Type two numbers')
        else:
          w, h = 30, 30
          break
      print('Size of samples {}x{}\n'.format(w, h))
      ToGray(pre_path, "Good", w, h)
      ToGray(pre_path, "Bad", w, h)
      gn = BuildDat(pre_path, "Good_Gr", w, h, True)
      bn = BuildDat(pre_path, "Bad_Gr", w, h)

      ln1 = 'cd /d {}/Haar \n'.format(pre_path[:pre_path.rindex('/')])
      ln2 = 'opencv_createsamples.exe -info {}/Good_Gr.dat -vec samples.vec -w {} -h {} -num {} \n'.format(pre_path, w, h, gn)
      ln3 = 'opencv_traincascade.exe -data haarcascade -vec samples.vec -bg {}/Bad_Gr.dat -numStages 16 '.format(pre_path)
      ln3 += '-minhitrate 0.99 -maxFalseAlarmRate 0.1 -numPos {} -numNeg {} '.format(int(gn * 0.8), bn)
      ln3 += '-w {} -h {} -mode ALL -precalcValBufSize {} -precalcIdxBufSize {} \n'.format(w, h, ram, ram)

      f = open('{}/START.bat'.format(pre_path), 'w')
      f.write(ln1)
      f.write(ln2)
      f.write(ln3)
      f.close()

      print('Comands: \n')
      print(ln1)
      print(ln2)
      print(ln3)
      print('Or you can run START.bat file in folder whith images. \n')
    else:
      print('"Data" folder must contain folders: "Good", "Bad"')
  
else:
  print('Put "Data" folder to this script.')
  print('"Data" folder must contain folders: "Good", "Bad"')

input()






