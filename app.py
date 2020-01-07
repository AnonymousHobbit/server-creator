import os, glob
import sys
import urllib.request

desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")

files = ['buildtools.jar', 'BuildTools.log.txt']
folders = ["BuildData", "Bukkit", "CraftBukkit", "Spigot", "work"]
versionfolders = ['apache-maven', 'PortableGit']
spigot_file = " "

def serverBuild(ram):

    curfiles = [f for f in os.listdir('.') if os.path.isfile(f)]

    for f in curfiles:
        spigot_file = f

    #Creating run.bat file
    print('[+] Creating run.bat file')
    with open("run.bat", "w+") as bat_file:
        bat_file.write(r'java -jar -Xmx{}G -Xms1G {} nogui'.format(ram, spigot_file))

    print('[*] Starting to build the server')
    #Starting to build the server
    os.system('run.bat')

    print('[+] Changing eula settings to true')
    with open("eula.txt", "w+") as eula:
        eula.write('eula=true')

    os.system('run.bat')




def remove():
    print('[*] Removing everything except spigot.jar')
    for i in folders:
        os.system("rmdir /s /q " + i)
        print("Removing folder: " + i)
    for i in versionfolders:
        for filename in glob.glob(i + "*"):
            os.system("rmdir /s /q " + filename)
            print("Removing folder: " + filename)

    for i in files:
        try:
            os.remove(i)
            print('Removing file: ' + i)
        except:
            print('File does not exist: ' + i)

    print('[*] Removing done ')


def main(name, ram):
        if not os.path.exists(desktop + "//" + name):
            os.mkdir(desktop + "//" + name)
            print('[+] Folder Created')
        else:
            print('[!] Folder already exists')

        path = desktop + "\\" + name
        os.chdir(path)
        print('[*] Retrieving the latest spigot file')
        urllib.request.urlretrieve('https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar', path + '\\buildtools.jar')

        print('[*] Starting buildtools.jar')
        os.system('java -jar ' + path + '\\buildtools.jar --rev latest')

        remove()
        serverBuild(ram)





if __name__ == '__main__':
    name = input("Folder name: ")
    ram = input("Ram amount: ")

    main(name, ram)
