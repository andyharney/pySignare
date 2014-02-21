#   Copyright 2014 Andy Harney (2014)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Here we go
# Check to see if Java is installed and added to system path

def checkJava():
    import sys
    import subprocess

    sJava = subprocess.call(['java', '-version'])
    if sJava == None:
        print('Java not installed or added to system path, please install')
        pause = input('Press Any Key To Exit')
        del pause
        # Exit gracefully
        sys.exit()
    else:
        print('Java Seems OK' + '\n')
    CheckOutputFolder()

def MainMenu():

    LineBreak = ('-'*28)
    print('Main Menu')
    print(LineBreak)
    print('1 : Sign With Debug Key')
    print('2 : Sign With Private Key')
    print('3 : ZipAlign Signed APKs')
    print(LineBreak)
    print('4 : Generate Private Key')
    print(LineBreak)
    print('5 : Exit ')
    print(LineBreak)
    print('\n')
    MenuChoice()

def MenuChoice():
    import sys

    # User enters option number, its validated as an integer and passes to the Options List
    while True:
        try:
            option = int(input('Please Choose an Option : '))
            if 1 <= option <= 5:
                break
            elif option == 21:
                print('Hidden Menu')
                raise Exception('Hidden Menu')
            else:
                raise Exception('Not in Range')

        except ValueError:
            print('Please enter a valid option, whole numbers please.')
            continue
        except Exception:
            print('Please enter a valid option, ' + str(option) + " isn't an option.")

    if 1 <= option <= 5:
        # Options List
        if option == 1:
            DebugKeySign()
        elif option == 2:
            PivateKeySign()
        elif option == 3:
            option3()
        elif option == 4:
            GenPrivKey()
        elif option == 5:
            # Exit gracefully
            print('Quitting')
            sys.exit()
    print('Please Choose a Valid Option')

# Main Function
def CheckOutputFolder():
    import os
    import os.path
    if os.path.isdir('./SignedApks/'):
        print('Output Folder Exists....')
        print('\n')
    else:
        print('Making Output Folder')
        print('\n')
        os.mkdir('SignedApks')
    MainMenu()

def DebugKeySign():
    import os
    import os.path
    import sys
    import subprocess

    print('\n' + 'Debug Key Signing' + '\n')
    # Create List of APKs
    APKDir = './UnsignedApks/'
    APKList = os.listdir(APKDir)
    DebugKeyDir = './DebugKey/'
    DebugKeys = os.listdir(DebugKeyDir)
    # Returns the number of APKs Found
    print('Scanning Unsigned Apks Folder')
    # If none are found exit with message
    if len(APKList) == 0:
        print('No APKs Found' + '\n')
        pause = input('Press Any Key To Exit')
        del pause
        # Exit gracefully
        sys.exit()
    else:
        print('Found ' + str(len(APKList)) + ' APK' + '\n')
        for APK in APKList:
            try:
                print(APK)
                subprocess.call(['java',
                                 '-jar',
                                 './Files/signapk.jar',
                                 './DebugKey/' + DebugKeys[1],
                                 './DebugKey/' + DebugKeys[0],
                                 './UnsignedApks/' + APK,
                                 './SignedApks/' + APK
                ])
            except:
                print('Not Working')
    MainMenu()

def PivateKeySign():
    import os
    import os.path
    import sys
    import subprocess

    print('\n' + 'Private Key Signing' + '\n')
    # Create List of APKs
    APKDir = './UnsignedApks/'
    APKList = os.listdir(APKDir)
    # Returns the number of APKs Found
    print('Scanning Unsigned Apks Folder')
    # If none are found exit with message
    UsrAlias = input('Alias You Wish To Sign With : ')
    if len(APKList) == 0:
        print('No APKs Found' + '\n')
        pause = input('Press Any Key To Exit')
        del pause
        # Exit gracefully
        sys.exit()
    else:
        print('Found ' + str(len(APKList)) + ' APK' + '\n')
        KeyStorePass = input('Please Enter your KEYSTORE Password : ')
        KeyPass = input('Please Enter your KEY Password : ')
        for APK in APKList:
            try:
                subprocess.call(['./Files/jarsigner.exe',
                             '-keystore',
                             '"' + './PrivateKey/private-key.keystore' + '"',
                             KeyStorePass,
                             '-keypass',
                             KeyPass,
                             '"' + './UnsignedApks/' + APK + '"',
                             '"' + str(UsrAlias) + '"'
              ])
                print('Signing ' + APK)
                MainMenu()
            except:
                print('Not Working')
                MainMenu()

    # %FILES%\jarsigner.exe -keystore .\PrivateKey\%alias%-private-key.keystore %%A %alias%
def GenPrivKey():
    import subprocess
    print('Insert Warning')
    UsrAlias = input('Choose Desired Alias : ')
    KeyPass = input('Choose Desired KEY (not keystore) Password : ')
    while len(KeyPass) < 6:
        print('Your Key Password MUST be greater than 6 characters, try again')
        KeyPass = input('Choose Desired KEY Password : ')
    subprocess.call(['./Files/keytool.exe',
                     '-genkey',
                     '-v',
                     '-keystore',
                     './PrivateKey/' + str(UsrAlias) + '-private-key.keystore',
                     '-alias',
                     UsrAlias,
                     '-keypass',
                     KeyPass,
                     '-keyalg',
                     'RSA',
                     '-keysize',
                     '2048',
                     '-validity',
                     '10000'
    ])
    a = input('Pause')
    MainMenu()



checkJava()