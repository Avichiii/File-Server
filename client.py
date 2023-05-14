from socket import * #type: ignore
import time

PATH = r'C:\Socket Programming\file_server'
MAX_SIZE = 1024 * 1024

class Method:
    get = 'GET'
    post = 'POST'

class CreatingSocket:
    def __init__(self):
        self.serverIP = gethostbyname(gethostname())
        self.serverPort = 8000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverIP, self.serverPort))

    def request(self):
        try:
            reqMethod = input('Method <: ').upper()
            fileName = input('File <: ').lower()
            
            if reqMethod == Method.get:
                rqGet = f'{reqMethod} {fileName}'.encode()
                self.clientSocket.send(rqGet)

                recvFile = self.clientSocket.recv(MAX_SIZE).decode()
                with open(f'{PATH}\\{fileName}.txt', 'a') as file:
                    file.write(recvFile)
                
                self.clientSocket.close()
                    
            elif reqMethod == Method.post:
                rqPost = f'{reqMethod} {fileName}'.encode()
                self.clientSocket.send(rqPost)
                with open(f'{PATH}\\{fileName}.txt', 'r') as file:
                    sendFile = file.read()

                self.clientSocket.sendall(sendFile.encode())
                
                self.clientSocket.close()
        
        except:
            print('File Operation Failed')
            self.clientSocket.close()

if __name__=='__main__':
    cl = CreatingSocket()
    cl.request()