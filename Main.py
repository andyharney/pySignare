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


def checkjava():

    import sys
    import subprocess

    sjava = subprocess.call(['java', '-version'])
    if sjava is None:
        print('Java not installed or added to system path, please install')
        pause = input('Press Any Key To Exit')
        del pause
        # Exit gracefully
        sys.exit()
    else:
        print('Java Seems OK' + '\n')
    checkoutputfolder()


def mainmenu():

    linebreak = ('-' * 28)
    print('Main Menu')
    print(linebreak)
    print('1 : Sign With Debug Key')
    print('2 : Sign With Private Key')
    print('3 : ZipAlign Signed APKs')
    print(linebreak)
    print('4 : Generate Private Key')
    print(linebreak)
    print('5 : Exit ')
    print(linebreak)
    menuchoice()


def menuchoice():

    import sys

    class MenuError(Exception):
        pass

    class HiddenMenu(Exception):
        pass

    option = ''
    # User enters option number, its validated as an integer and passes to the Options List
    while True:

        try:
            option = int(input('Please Choose an Option : '))
            if 1 <= option <= 5:
                break
            elif option == 1729:
                raise HiddenMenu()
            else:
                raise MenuError()

        except ValueError:
            print('Please enter a valid option, whole numbers please.')
            continue
        except MenuError:
            print('Please enter a valid option, ' + str(option) + " isn't an option.")
        except HiddenMenu:
            print('Very Clever, but nothing is hidden. Yet')

    if 1 <= option <= 5:
        # Options List
        if option == 1:
            debugkeysign()
        elif option == 2:
            privatekeysign()
        elif option == 3:
            zipalign()
        elif option == 4:
            genprivkey()
        elif option == 5:
            # Exit gracefully
            print('Quitting')
            sys.exit()
    print('Please Choose a Valid Option')


def checkoutputfolder():

    import os
    import os.path

    if os.path.isdir('./SignedApks/'):
        #print('Output Folder Exists....')
        #print('\n')
        mainmenu()
    else:
        os.mkdir('SignedApks')
        mainmenu()


def debugkeysign():

    import os
    import os.path
    import subprocess

    print('\n' + 'Debug Key Signing' + '\n')
    # Create List of APKs
    apkdir = './UnsignedApks/'
    apklist = os.listdir(apkdir)
    debugkeydir = './DebugKey/'
    debugkeys = os.listdir(debugkeydir)
    # If none are found exit with message
    if len(apklist) == 0:
        print('No APKs Found' + '\n')
        pause = input('Press Any Key to Return to Menu')
        print()
        del pause
        mainmenu()
    else:
        print('Found ' + str(len(apklist)) + ' APK' + '\n')
        for APK in apklist:
            print('Signing ' + APK)
            subprocess.call(['java',
                             '-jar',
                             './Files/signapk.jar',
                             './DebugKey/' + debugkeys[1],
                             './DebugKey/' + debugkeys[0],
                             './UnsignedApks/' + APK,
                             './SignedApks/' + APK
            ])
    print()
    print('Signing has finished, please check the messages above for any errors.')
    input('Press any key to continue')
    print()
    mainmenu()


def privatekeysign():

    import os
    import os.path
    import subprocess
    import shutil

    if os.path.isdir('./tmp/'):
        shutil.rmtree('./tmp')
    else:
        print('No tmp folder')

    print('\n' + 'Private Key Signing' + '\n')
    # Create List of APKs
    apkdir = './UnsignedApks/'
    apklist = os.listdir(apkdir)
    # Returns the number of APKs Found
    usralias = input('Alias You Wish To Sign With : ')
    if len(apklist) == 0:
        print('No APKs Found' + '\n')
        pause = input('Press Any Key to Return to Menu')
        print()
        del pause
        mainmenu()
    else:
        apkcount = len(apklist)
        signcount = 0
        print('Found ' + str(apkcount) + ' APK' + '\n')
        keystorepass = input('Please Enter your KEYSTORE Password : ')
        #KeyPass = input('Please Enter your KEY Password : ')
        while signcount != apkcount:
            for APK in apklist:
                print('Signing ' + APK)
                os.mkdir('tmp')
                shutil.copyfile('./UnsignedApks/' + APK, './tmp/' + APK)
                subprocess.call(['./Files/jarsigner.exe',
                                 '-keystore',
                                 'PrivateKey/' + str(usralias) + '-private-key.keystore',
                                 '-storepass',
                                 keystorepass,
                                 './UnsignedApks/' + APK,
                                 str(usralias),
                                 #'-verify',
                                 #'-verbose',
                                 #'-certs'
                ])
                try:
                    os.rename('./UnsignedApks/' + APK, './SignedApks/' + APK)
                except FileExistsError:
                    os.rename('./SignedApks/' + APK, './tmp/T_' + APK)
                    os.rename('./UnsignedApks/' + APK, './SignedApks/' + APK)
                os.rename('./tmp/' + APK, './UnsignedApks/' + APK)
                shutil.rmtree('./tmp/')
                signcount += 1
        print()
        print('Signing has finished, please check the messages above for any errors.')
        input('Press any key to continue')
        print()
        mainmenu()


def genprivkey():

    import subprocess

    print('Insert Warning')
    usralias = input('Choose Desired Alias : ')
    keypass = input('Choose Desired KEY (not keystore) Password : ')
    while len(keypass) < 6:
        print('Your Key Password MUST be greater than 6 characters, try again')
        keypass = input('Choose Desired KEY Password : ')
    subprocess.call(['./Files/keytool.exe',
                     '-genkey',
                     '-v',
                     '-keystore',
                     './PrivateKey/' + str(usralias) + '-private-key.keystore',
                     '-alias',
                     usralias,
                     '-keypass',
                     keypass,
                     '-keyalg',
                     'RSA',
                     '-keysize',
                     '2048',
                     '-validity',
                     '10000'
    ])
    print()
    mainmenu()


def zipalign():

    import os
    import subprocess

    print('\n' + 'Zip Aliging' + '\n')
    zipaligncount = 0
    apkdir = './SignedApks/'
    apklist = os.listdir(apkdir)
    apkcount = len(apklist)
    if len(apklist) == 0:
        print('No Signed APKs Found' + '\n')
        pause = input('Press Any Key to Return to Menu')
        del pause
        print()
        mainmenu()
    else:
        while zipaligncount != apkcount:
            for APK in apklist:
                print(APK)
                subprocess.call(['./Files/zipalign.exe',
                                 '-f',
                                 '4',
                                 './SignedApks/' + APK,
                                 './ZipAlignedApks/' + APK
    ])
            zipaligncount += 1
    print()
    mainmenu()

checkjava()
