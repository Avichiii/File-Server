from socket import * #type: ignore
import time
import os

PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server\clientFiles'
MAX_SIZE = 1024 * 1024

class Method:
    get = 'GET'
    post = 'POST'
    flist = 'LIST'
    fileOperations = 'OPERATION'

class CreatingSocket:
    def __init__(self):
        self.serverIP = gethostbyname(gethostname())
        self.serverPort = 8000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverIP, self.serverPort))

    def request(self):
        try:
            reqMethod = input('Method <: ').upper()
            if (reqMethod != Method.flist) and (reqMethod != Method.fileOperations):
                fileName = input('File <: ').lower()
            
            if reqMethod == Method.get:
                self.downloadFile(reqMethod, fileName)
        
            elif reqMethod == Method.post:
                self.uploadFile(reqMethod, fileName)

            elif reqMethod == Method.flist:
                self.listFiledDir()
            
            elif reqMethod == Method.fileOperations:
                self.mainLoop(reqMethod)

        except:
            print('File Operation Failed')
            self.clientSocket.close()

    def downloadFile(self, reqMethod, fileName):
        rqGet = f'{reqMethod} {fileName}'.encode()
        self.clientSocket.send(rqGet)

        recvFile = self.clientSocket.recv(MAX_SIZE).decode()
        with open(f'{PATH}\\{fileName}.txt', 'a') as file:
            file.write(recvFile)
        
        self.clientSocket.close()

    def uploadFile(self, reqMethod, fileName):
        rqPost = f'{reqMethod} {fileName}'.encode()
        self.clientSocket.send(rqPost)
        with open(f'{PATH}\\{fileName}.txt', 'r') as file:
            sendFile = file.read()

        self.clientSocket.sendall(sendFile.encode())

        self.clientSocket.close()

    def listFiledDir(self):
        self.clientSocket.send('LIST DIR'.encode())
        fileCount = self.clientSocket.recv(MAX_SIZE).decode()
        print(fileCount)
        for _ in range(int(fileCount)):
            file = self.clientSocket.recv(MAX_SIZE).decode()
            print(file)
        
        self.clientSocket.close()

class FileOperations(CreatingSocket):
    def __init__(self):
        super().__init__()
    
    
    def mainLoop(self, reqMethod):
        flag = True
        while flag:
            print(
                '\n',
                '\t1. Create File\n',
                '\t2. Delete File\n',
                '\t3. Create Dir\n',
                '\t4. Delete Dir\n',
                '\t5. Change Dir\n'
                '\t6. Quit\n'   
            )

            command = int(input('Command! [1 - 6] <: '))
            if command == 1:
                try:
                    self.clientSocket.send(f'{reqMethod} CREATE_FILE'.encode())
                    filename = input('FileName <: ')
                    self.clientSocket.send(filename.encode())
                    fileCreationResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(fileCreationResult)

                except:
                    print('Exception Occured')

            elif command == 2:
                # self.deleteFile()
                try:
                    self.clientSocket.send(f'{reqMethod} DELETE_FILE'.encode())
                    filename = input('FileName <: ')
                    self.clientSocket.send(filename.encode())
                    fileDeletionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(fileDeletionResult)

                except:
                    print('Exception Occured')

            elif command == 3:
                # self.createDir()
                try:
                    self.clientSocket.send(f'{reqMethod} CREATE_DIR'.encode())
                    dirname = input('DirName <: ')
                    self.clientSocket.send(dirname.encode())
                    dirCreationtionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(dirCreationtionResult)

                except:
                    print('Exception Occured')

            elif command == 4:
                # self.deleteDir()
                try:
                    self.clientSocket.send(f'{reqMethod} DELETE_DIR'.encode())
                    dirname = input('DirName <: ')
                    self.clientSocket.send(dirname.encode())
                    dirDeletiontionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(dirDeletiontionResult)

                except:
                    print('Exception Occured')

            elif command == 5:
                self.changeDir()
            
            elif command == 6:
                flag = False
                exit(0)
            
            else:
                print('Invalid Command! ')
            


    def createFile(self, reqMethod):
        pass

    def deleteFile(self):
        pass
    def createDir(self):
        pass
    def deleteDir(self):
        pass
    def changeDir(self):
        pass




if __name__=='__main__':
    cl = FileOperations()
    cl.request()
