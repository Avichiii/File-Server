from socket import * #type: ignore
import threading
import os
import datetime

# THREAD_COUNT = 0
MAX_SIZE = 1024 * 1024
PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server\serverFiles'

class Method:
    get = 'GET'
    post = 'POST'
    flist = 'LIST'
    fileOperations = 'OPERATION'


class FileManipulation:
    createFile = 'CREATE_FILE'
    deleteFile = 'DELETE_FILE'
    createDir = 'CREATE_DIR'
    deleteDir = 'DELETE_DIR'
    changeDir = 'CHANGE_DIR'

class Server:
    def __init__(self):
        self.serverPort = 8000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # let imediately use the socket after it's closed
        self.serverSocket.bind((gethostbyname(gethostname()), self.serverPort))
        self.serverSocket.listen(100)
        self.threadCount = 0

    def start(self):
        print('[+] Server is running...\n')

        while True:
            clientSocket, addr = self.serverSocket.accept()
            self.startFileServer(clientSocket, addr)
            print(f'thread count: {self.threadCount}')

    def startFileServer(self, clientSocket:socket, addr):
        getClinetRequest = clientSocket.recv(MAX_SIZE).decode()
        getMethod = getClinetRequest.split(' ')[0]
        print(getClinetRequest)
        print(f'[+] IP: {addr[0]} Port: {addr[1]}  connected')

        if getMethod == Method.get:
            threading.Thread(target=getFile, args=(getClinetRequest, clientSocket)).start()
            self.threadCount += 1
            

        elif getMethod == Method.post:
            threading.Thread(target=saveFile, args=(getClinetRequest, clientSocket)).start()
            self.threadCount += 1
            

        elif getMethod == Method.flist:
            threading.Thread(target=listFileDir, args=(clientSocket,)).start()
            self.threadCount += 1
        
        elif getMethod == Method.fileOperations:
            threading.Thread(target=fileOperation, args=(getClinetRequest, clientSocket,)).start()
            self.threadCount += 1
            
        else:
            clientSocket.send('Please Enter Valid Method'.encode())

def getFile(getClinetRequest, clientSocket:socket):
    try:
        filename = getClinetRequest.split(' ')[1]
        file =  open(f'{PATH}\\{filename}.txt', 'r')
        readfile = file.read()
        clientSocket.sendall(readfile.encode())
        file.close()
        clientSocket.close()

    except:
        badResponceHeader = 'File Not Found'
        clientSocket.send(badResponceHeader.encode())
        clientSocket.close()
    
def saveFile(getClinetRequest, clientSocket:socket):
    try:
        filename = getClinetRequest.split(' ')[1]
        fileContent = clientSocket.recv(MAX_SIZE).decode()
        saveFile = open(f'{PATH}\\{filename}.txt', 'w')
        saveFile.write(fileContent)
        saveFile.close()
        clientSocket.close()


    except:
        clientSocket.send('File Couldn\\be saved'.encode())

def listFileDir(clientSocket:socket):
    try:
        files = os.listdir(PATH)
        clientSocket.send((str(len(files))).encode())
        for file in files:
            clientSocket.send(file.encode() + '\n'.encode())
        
        clientSocket.close()


    except:
        clientSocket.send('There are no files to list'.encode())

    
def fileOperation(getClientRequest, clientSocket:socket):
    if getClientRequest.split(' ')[1] == FileManipulation.createFile:
        try:
            flag = True
            while flag:
                filename = clientSocket.recv(MAX_SIZE).decode()
                with open(f'{PATH}\\{filename}.txt', 'a'):
                    pass
                message = f'{filename} created Successfully.'
                clientSocket.send(message.encode())

        except:
            clientSocket.send('File Operation Failed'.encode())
    
    elif getClientRequest.split(' ')[1] == FileManipulation.deleteFile:
        try:
            flag = True
            while flag:
                filename = clientSocket.recv(MAX_SIZE).decode()
                os.remove(f'{PATH}\\{filename}.txt')
                message = f'{filename} deleted Successfully.'
                clientSocket.send(message.encode())

        except:
            clientSocket.send('File Operation Failed'.encode())

    elif getClientRequest.split(' ')[1] == FileManipulation.createDir:
        try:
            flag = True
            while flag:
                dirname = clientSocket.recv(MAX_SIZE).decode()
                os.makedirs(f'{PATH}\\{dirname}')
                message = f'{dirname} created Successfully.'
                clientSocket.send(message.encode())

        except:
            clientSocket.send('File Operation Failed'.encode())

    elif getClientRequest.split(' ')[1] == FileManipulation.deleteDir:
        try:
            flag = True
            while flag:
                dirname = clientSocket.recv(MAX_SIZE).decode()
                os.rmdir(f'{PATH}\\{dirname}')
                message = f'{filename} created Successfully.'
                clientSocket.send(message.encode())

        except:
            clientSocket.send('File Operation Failed'.encode())
    
    elif getClientRequest.split(' ')[1] == FileManipulation.changeDir:
        try:
            flag = True
            while flag:
                dirname = clientSocket.recv(MAX_SIZE).decode()
                os.chdir(f'{PATH}\\{dirname}')
                message = f'{filename} created Successfully.'
                clientSocket.send(message.encode())

        except:
            clientSocket.send('File Operation Failed'.encode())
            


if __name__=='__main__':
    ser = Server()
    ser.start()



    # os.open
    # os.makedirs
    # os.chdir
    # os.rmdir
    # os.remove
    # os.rename