from socket import * #type: ignore
import time
import string

PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server\clientFiles'
MAX_SIZE = 1024 * 1024

class Method:
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
            authResponse = self.checkAuth()

            if authResponse == True:
                print('[+] command: List | Operation')
                reqMethod = input('Method <: ').upper()

                if reqMethod == Method.flist:
                    self.listFiledDir()
                
                elif reqMethod == Method.fileOperations:
                    self.callMainLoop(reqMethod)
            else:
                print('Auth Failure')

        except:
            print('File Operation Failed')
            self.clientSocket.close()


    def listFiledDir(self):
        self.clientSocket.send('LIST_DIR'.encode())
        fileCount = self.clientSocket.recv(MAX_SIZE).decode()
        print(fileCount)
        for _ in range(int(fileCount)):
            file = self.clientSocket.recv(MAX_SIZE).decode()
            print(file)
        
        self.clientSocket.close()

class FileOperations(CreatingSocket):
    def __init__(self):
        super().__init__()
    
    
    def callMainLoop(self, reqMethod:str):
        time.sleep(0.1)
       
        self.clientSocket.send(reqMethod.encode())
        self.mainLoop()

    def checkAuth(self):
        psw = input('Enter Password <: ')
        passwd = self.rot(psw)
        self.clientSocket.send(str(passwd).encode())
        responseCode = self.clientSocket.recv(MAX_SIZE).decode()
        if responseCode == 'True':
            return True

        elif responseCode == 'False':
            return False
        
        else:
            print('Exception occured! ')
    
    def rot(self, psw: str):
        lenpass = len(psw)

        newEncryptedPass = ''

        for i in range(lenpass):
            if psw[i] in string.ascii_lowercase:
                index = string.ascii_lowercase.index(psw[i])
                newEncryptedPass += string.ascii_lowercase[(index+13)%26]
            elif psw[i] in string.ascii_uppercase:
                index = string.ascii_uppercase.index(psw[i])
                newEncryptedPass += string.ascii_uppercase[(index+13)%26]
            else:
                newEncryptedPass += i

        return newEncryptedPass

    def mainLoop(self):
        while True:
            print(
                '\n',
                '\t1. Create File\n',
                '\t2. Delete File\n',
                '\t3. Create Dir\n',
                '\t4. Delete Dir\n',
                '\t5. Change Dir\n'
                '\t6. Download File\n'   
                '\t7. Upload File\n'     
                '\t8. Quit\n'   
            )
            command = int(input('Command! [1 - 8] <: '))

            if command == 1:
                try:
                    self.clientSocket.send(f'CREATE_FILE'.encode())
                    filename = input('FileName <: ')

                    self.clientSocket.send(filename.encode())
                    time.sleep(0.25)
                    fileContent = input('Enter File Content <: ')
                    self.clientSocket.send(fileContent.encode())
                    fileCreationResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(fileCreationResult)

                except:
                    print('Exception Occured')

            elif command == 2:
                try:
                    self.clientSocket.send(f'DELETE_FILE'.encode())
                    filename = input('FileName <: ')
                    self.clientSocket.send(filename.encode())
                    fileDeletionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(fileDeletionResult)

                except:
                    print('Exception Occured')


            elif command == 3:
                try:
                    self.clientSocket.send(f'CREATE_DIR'.encode())
                    dirname = input('DirName <: ')
                    self.clientSocket.send(dirname.encode())
                    dirCreationtionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(dirCreationtionResult)

                except:
                    print('Exception Occured')

            elif command == 4:
                try:
                    self.clientSocket.send(f'DELETE_DIR'.encode())
                    dirname = input('DirName <: ')
                    self.clientSocket.send(dirname.encode())
                    dirDeletiontionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(dirDeletiontionResult)

                except:
                    print('Exception Occured')

            elif command == 5:
                try:
                    self.clientSocket.send(f'CHANGE_DIR'.encode())
                    dirname = input('DirName <: ')
                    self.clientSocket.send(dirname.encode())
                    dirDeletiontionResult = self.clientSocket.recv(MAX_SIZE).decode()
                    print(dirDeletiontionResult)

                except:
                    print('Exception Occured')
            
            elif command == 6:
                # Download File
                try:
                    self.clientSocket.send('DOWNLOAD'.encode())
                    rqGet = input('File <: ')
                    # rqGet = f'{fileName}'.encode()
                    self.clientSocket.send(rqGet.encode())

                    recvFile = self.clientSocket.recv(MAX_SIZE).decode()
                    with open(f'{PATH}\\{rqGet}.txt', 'a') as file:
                        file.write(recvFile)
                except:
                    print('Exception occured')


            elif command == 7:
                # Upload File
                try:
                    rqPost = input('File <: ')
                    self.clientSocket.send('UPLOAD'.encode())
                    self.clientSocket.send(rqPost.encode())
                    with open(f'{PATH}\\{rqPost}.txt', 'r') as file:
                        sendFile = file.read()
                        self.clientSocket.sendall(sendFile.encode())
                except:
                    print('Exception occured')  

            elif command == 8:
                self.clientSocket.close()
                exit(0)
                
            else:
                print('Invalid Command! ')
            
if __name__=='__main__':
    cl = FileOperations()
    cl.request()