from socket import * #type: ignore
import threading
import os

MAX_SIZE = 1024 * 1024
PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server\serverFiles'

class Method:
    flist = 'LIST_DIR'
    fileOperations = 'OPERATION'

class FileManipulation:
    createFile = 'CREATE_FILE'
    deleteFile = 'DELETE_FILE'
    createDir = 'CREATE_DIR'
    deleteDir = 'DELETE_DIR'
    changeDir = 'CHANGE_DIR'
    downloadFile = 'DOWNLOAD'
    uploadFile = 'UPLOAD'

class Server:
    def __init__(self):
        self.serverPort = 8000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # let imediately use the socket after it's closed
        self.serverSocket.bind((gethostbyname(gethostname()), self.serverPort))
        self.serverSocket.listen(100)

    def start(self):
        print('[+] Server is running...\n')

        while True:
            clientSocket, addr = self.serverSocket.accept()
            self.startFileServer(clientSocket, addr)

    def startFileServer(self, clientSocket:socket, addr):
        getClinetRequest = clientSocket.recv(MAX_SIZE).decode()
        getMethod = getClinetRequest.split(' ')[0]
        print(getClinetRequest)
        print(f'[+] IP: {addr[0]} Port: {addr[1]}  connected')
            
        if getMethod == Method.flist:
            threading.Thread(target=listFileDir, args=(clientSocket,)).start()
        
        elif getMethod == Method.fileOperations:
            threading.Thread(target=self.fileOps, args=( clientSocket,)).start()
            
        else:
            clientSocket.send('Please Enter Valid Method'.encode())


def listFileDir(clientSocket:socket):
    try:
        files = os.listdir(PATH)
        clientSocket.send((str(len(files))).encode())
        for file in files:
            clientSocket.send(file.encode() + '\n'.encode())
        
        clientSocket.close()

    except:
        clientSocket.send('There are no files to list'.encode())


class FileOperation(Server):

    def __init__(self):
        super().__init__()

    def fileOps(self, clientSocket:socket):
        fileMethod = clientSocket.recv(MAX_SIZE).decode()
        print(fileMethod)

        if fileMethod == FileManipulation.createFile:
            self.createF(clientSocket)
        
        if fileMethod == FileManipulation.deleteFile:
            self.deleteF(clientSocket)

        if fileMethod == FileManipulation.createDir:
            self.createD(clientSocket)

        if fileMethod == FileManipulation.deleteDir:
            self.deleteD(clientSocket)
        
        if fileMethod == FileManipulation.changeDir:
            self.changeD(clientSocket)

        if fileMethod == FileManipulation.downloadFile:
            self.getFile(clientSocket)

        if fileMethod == FileManipulation.uploadFile:
            self.saveFile(clientSocket)

    def createF(self, clientSocket:socket):
        try:
            filename = clientSocket.recv(MAX_SIZE).decode()
            with open(f'{PATH}\\{filename}.txt', 'a') as file:
                fileContent = clientSocket.recv(MAX_SIZE).decode()
                file.write(fileContent)

            message = f'{filename} created Successfully.'
            clientSocket.send(message.encode())
            return self.fileOps(clientSocket)
            
        except:
            clientSocket.send('File Operation Failed'.encode())
    
    def deleteF(self, clientSocket:socket):
        try:
            filename = clientSocket.recv(MAX_SIZE).decode()
            os.remove(f'{PATH}\\{filename}.txt')
            message = f'{filename} deleted Successfully.'
            clientSocket.send(message.encode())
            return self.fileOps(clientSocket)
           
        except:
            clientSocket.send('File Operation Failed'.encode())

    def createD(self, clientSocket:socket):
        try:
                dirname = clientSocket.recv(MAX_SIZE).decode()
                os.makedirs(f'{PATH}\\{dirname}')
                message = f'{dirname} created Successfully.'
                clientSocket.send(message.encode())
                return self.fileOps(clientSocket)

        except:
            clientSocket.send('File Operation Failed'.encode())

    def deleteD(self, clientSocket:socket):
        try:
                dirname = clientSocket.recv(MAX_SIZE).decode()
                os.rmdir(f'{PATH}\\{dirname}')
                message = f'{dirname} created Successfully.'
                clientSocket.send(message.encode())
                return self.fileOps(clientSocket)
        
        except:
            clientSocket.send('File Operation Failed'.encode())
    
    def changeD(self, clientSocket:socket):
        global PATH
        try:
            dirname = clientSocket.recv(MAX_SIZE).decode()
            print(dirname)
            if dirname == 'pwd':
                message = f'current path > {PATH}'
                clientSocket.send(message.encode())
                return self.fileOps(clientSocket)
            
            elif dirname == '..':
                if PATH == r'D:\file_server\serverFiles':
                    clientSocket.send('can\'t revert anymore.'.encode())
                    return self.fileOps(clientSocket)
                else:
                    os.chdir('..')
                    PATH = os.getcwd()
                    message = f'{PATH} changed Successfully.'
                    clientSocket.send(message.encode())
                    return self.fileOps(clientSocket)
                
            else:
                os.chdir(f'{PATH}\\{dirname}')
                PATH = os.getcwd()
                message = f'{PATH} changed Successfully.'
                clientSocket.send(message.encode())
                return self.fileOps(clientSocket)
            
        except:
            clientSocket.send('File Operation Failed'.encode())
            clientSocket.close()
    
    def getFile(self, clientSocket:socket):
        try:
            filename = clientSocket.recv(MAX_SIZE).decode()
            file =  open(f'{PATH}\\{filename}.txt', 'r')
            readfile = file.read()

            clientSocket.sendall(readfile.encode())
            file.close()
            return self.fileOps(clientSocket)

        except:
            badResponceHeader = 'File Not Found'
            clientSocket.send(badResponceHeader.encode())
            clientSocket.close()
    
    def saveFile(self, clientSocket:socket):
        try:
            filename = clientSocket.recv(MAX_SIZE).decode()
            fileContent = clientSocket.recv(MAX_SIZE).decode()
            saveFile = open(f'{PATH}\\{filename}.txt', 'w')
            saveFile.write(fileContent)
            saveFile.close()
            return self.fileOps(clientSocket)

        except:
            clientSocket.send('File Couldn\\be saved'.encode())

    
if __name__=='__main__':
    ser = FileOperation()
    ser.start()