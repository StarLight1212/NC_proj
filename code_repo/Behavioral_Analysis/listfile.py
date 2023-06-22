import os

def command_generate(group):
    basepath = "D:\\data\\pack\\Poincare\\"+group+'\\'
    path = []
    filelist = os.listdir('D:\\data\\pack\\Poincare\\'+group)
    #print(filelist)
    for i in filelist:
        path.append(basepath + i)
        #print(basepath + i)
    print(path)
    return path
    
    
    
    
    
if __name__ == '__main__':
    command_generate('Tr2')
