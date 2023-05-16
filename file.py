PATH = r'C:\Users\abhijit Dey\OneDrive\Desktop\file_server\serverFiles'
for i in range(10):
    with open(f'{PATH}\\file{i}.txt', 'a') as file:
        for j in range(100000):
                file.write('this is test file content.\n')
