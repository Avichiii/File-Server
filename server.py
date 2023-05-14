from socket import * #type: ignore
import threading

MAX_SIZE = 1024 * 1024
PATH = r'C:\Socket Programming'

class Method:
    get = 'GET'
    post = 'POST'

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
        print(f'[+] IP: {addr[0]} Port: {addr[1]}  connected')

        if getMethod == Method.get:
            threading.Thread(target=getFile, args=(getClinetRequest, clientSocket)).start()

        elif getMethod == Method.post:
            threading.Thread(target=saveFile, args=(getClinetRequest, clientSocket)).start()

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

if __name__=='__main__':
    ser = Server()
    ser.start()