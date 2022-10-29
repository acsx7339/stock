nemo = ['nemo']

def findNemo(item):
    print(len(item))
    for i in range(len(item)):
        if item[i] == 'nemo':
            print('find nemo')

findNemo(nemo)