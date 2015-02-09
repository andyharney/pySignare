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

# Define some global vars for later use
version = '1.1'
# APK Folders
usapks = './UnsignedApks/'
sapks = './SignedApks/'
zaapks = './ZipAlignedApks/'
# Key Folders
dgkeydir = './DebugKey/'
privkeydir = './PrivateKey/'
# Temp Folder
tmp = './tmp/'


def operatingsystem():
    import sys

    global keytool, zipalign, jarsigner, osplat, clsh, warning

    if sys.platform.startswith('linux'):
        clsh = 'clear'
        osplat = 'Linux'
        keytool = 'keytool-lin'
        zipalign = 'zipalign-lin'
        jarsigner = 'jarsigner-lin'
    elif sys.platform.startswith('darwin'):
        clsh = 'clear'
        osplat = 'Mac'
        keytool = 'keytool-mac'
        zipalign = 'zipalign-mac'
        jarsigner = 'jarsigner-mac'
    elif sys.platform.startswith('win32'):
        clsh = 'cls'
        osplat = 'Windows'
        keytool = 'keytool-win.exe'
        zipalign = 'zipalign-win.exe'
        jarsigner = 'jarsigner-win.exe'
        warning = ''
    # print(keytool, zipalign, jarsigner)
    # print()
    if not sys.platform.startswith('win32'):
        warning = '''****** Warning ******
Linux & OSX Support is Experimental
Proceed At Your Own Risk'''
    splash()


# Loads the splash, with a standard Apache Licence 2.0 disclaimer, and an acceptance option


def splash():
    import sys

    global warning

    print()
    print('pySignare v' + version + ' ' + osplat)
    print('https://github.com/andyharney/pySignare')
    print('')
    print('Written Exclusively For All Members of XDA-Developers.com')
    print()
    print('by Andy')
    print('http://forum.xda-developers.com/member.php?u=797171')
    print()
    print('''
Copyright 2014 Andy Harney (2014)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.''')
    print()
    try:
        if len(warning) != 0:
            print(warning)
            print()
        lic = input('Do you accept the terms of the above licence? Y/N - ')
        print()
        assert isinstance(lic, object)
        if lic.lower() == 'y':
            del lic
            checkjava()
        else:
            print('Without accepting the terms, you cannot continue')
            input('Press Enter To Exit')
            del lic
            sys.exit()
    except NameError as e:
        print('An Error Occurred\n')
        print(e)
        print('\nAssuming You Wish to Continue. This May Not Work.')
        checkjava()


def checkjava():
    import sys
    import subprocess
    # Java is called, checking if its in the system path, if not. It should exit with a user prompt
    # Not fully tested, java is installed on all my machines.
    sjava = subprocess.call(['java', '-version'])
    if sjava is None:
        print('Java not installed or added to system path, please install')
        input('Press Enter To Exit')
        del sjava
        # Exit gracefully
        sys.exit()
    else:
        print()
        del sjava
        # Moves on to the output folder checking function
        checkoutputfolder()


def checkoutputfolder():
    import os
    import os.path

    global sapks, zaapks, privkeydir

    # Create required output folders
    if not os.path.isdir(sapks):
        os.mkdir('SignedApks')
    if not os.path.isdir(zaapks):
        os.mkdir('ZipAlignedApks')
    if not os.path.isdir(privkeydir):
        os.mkdir('PrivateKey')
    # All clear, now the main menu function is loaded.
    mainmenu()


def mainmenu():
    import os

    global version, osplat, clsh

    os.system(clsh)
    print('pySignare v' + version + ' ' + osplat)
    print()
    print()
    # Here the main menu is printed
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
    del linebreak
    # Runs the menu choice function
    menuchoice()


def menuchoice():
    import sys

    # A Couple custom exceptions are created to catch any invalid/secret menu choices
    class MenuError(Exception):
        pass

    class HiddenMenu(Exception):
        pass

    option = ''
    # User enters option number, its validated as an integer and passes to the Options List
    while True:
        # This while loop catches the option choice and will only break if the choice is valid
        try:
            option = int(input('Please Choose an Option : '))
            if 1 <= option <= 5:
                break
            elif option == 1729:
                raise HiddenMenu()
            else:
                raise MenuError()
        # If the option choice is not a valid integer or a character this exception is raised
        except ValueError:
            print('Please enter a valid option, whole numbers please.')
            continue
        # If a valid integer is entered, but not a valid menu option, this exception is raised
        except MenuError:
            print('Please enter a valid option, ' + str(option) + " isn't an option.")
        # If 1729 is entered, this exception is raised.
        # Ref: Srinivasa Ramanujan - http://en.wikipedia.org/wiki/Srinivasa_Ramanujan
        except HiddenMenu:
            print('Very Clever, but nothing is hidden. Yet')

    # Menu choice logic
    # Lack of case statements shows.
    if 1 <= option <= 5:
        # Options List
        if option == 1:
            del option
            debugkeysign()
        elif option == 2:
            del option
            privkeyprep()
            del option
        elif option == 3:
            del option
            zipalignfunc()
        elif option == 4:
            del option
            genprivkey()
        elif option == 5:
            del option
            # Exit gracefully
            print('Quitting')
            sys.exit()
    print('Please Choose a Valid Option : ')


def debugkeysign():
    import os
    import os.path
    import subprocess

    global usapks, dgkeydir, sapks

    os.system('cls')
    print('\n' + 'Debug Key Signing' + '\n')
    # Create List of APKs
    apklist = os.listdir(usapks)
    debugkeys = os.listdir(dgkeydir)
    # If none are found exit with message
    if len(apklist) == 0:
        print('No APKs Found' + '\n')
        input('Press Enter to Return to Menu')
        print()
        mainmenu()
    else:
        print('Found ' + str(len(apklist)) + ' APK' + '\n')
        for APK in apklist:
            print('Signing ' + APK)
            subprocess.call(['java',
                             '-jar',
                             './Files/signapk.jar',
                             dgkeydir + debugkeys[1],
                             dgkeydir + debugkeys[0],
                             usapks + APK,
                             sapks + APK
            ])
    print()
    print('Signing has finished, please check the messages above for any errors.')
    input('Press Enter to continue')
    print()
    del apklist, debugkeys
    mainmenu()


def privkeyprep():
    class MenuError(Exception):
        pass

    import os
    import shutil

    global usapks, tmp, privkeydir

    os.system('cls')
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    print('\n' + 'Private Key Signing' + '\n')
    # Create List of APKs
    apklist = os.listdir(usapks)
    apkcount = len(apklist)
    privkeylist = os.listdir(privkeydir)
    privkeycount = len(privkeylist)
    keychoice = 0
    if privkeycount == 0:
        print('No Private Keys Found' + '\n')
        input('Press Enter to Return to Menu')
        print()
        mainmenu()
    sorted(privkeylist)
    if len(apklist) == 0:
        print('No APKs Found' + '\n')
        input('Press Enter to Return to Menu')
        print()
        mainmenu()
    if privkeycount == 1:
        chosenprivatekey = privkeylist
        privatekeysigning(apklist, apkcount, chosenprivatekey[0])
    else:
        print(str(privkeycount) + ' Private Keys Found')
        print()
        # Thanks Martijn Pieters
        # http://stackoverflow.com/a/21962946/3303492
        for keynum, privkey in enumerate(privkeylist, 1):
            print('{} : {}'.format(keynum, privkey))
        while True:
            # This while loop catches the option choice and will only break if the choice is valid
            try:
                keychoice = int(input('Please Choose a Key : '))
                print()
                if 1 <= keychoice <= privkeycount:
                    break
                else:
                    raise MenuError()
            # If the option choice is not a valid integer or a character this exception is raised
            except ValueError:
                print('Please enter a valid option')
                continue
            # If a valid integer is entered, but not a valid menu option, this exception is raised
            except MenuError:
                print('Please enter a valid option, ' + str(keychoice) + " isn't an option.")
                continue
        chosenprivatekey = privkeylist[(keychoice - 1)]
        print(chosenprivatekey + ' has been chosen')
        print()
        privatekeysigning(apklist, apkcount, chosenprivatekey)


def privatekeysigning(apklist, apkcount, chosenprivatekey):
    import os
    import shutil
    import subprocess

    global jarsigner, sapks, usapks, tmp, privkeydir

    alias = str(str.rstrip(chosenprivatekey, '-private-key.keystore'))
    signcount = 0
    if len(apklist) == 1:
        print('Found ' + str(apkcount) + ' APK' + '\n')
    else:
        print('Found ' + str(apkcount) + ' APKs' + '\n')
    # Insert warning about entering the keystore password
    print('Important, your KEYSTORE password is required to sign multiple apks at once.')
    print("Your KEYSTORE password is not used outside of this menu option. It's cleared when signing is complete.")
    print()
    keystorepass = input('Please Enter your KEYSTORE Password : ')
    print()
    while signcount != apkcount:
        for APK in apklist:
            print('Signing ' + APK)
            # Because private key signing is done "in-place" we backup the original apk, sign, move and restore
            # Create tmp folder
            os.mkdir('tmp')
            # Copy unsigned apk out
            shutil.copyfile(usapks + APK, tmp + APK)
            subprocess.call(['./Files/' + jarsigner,
                             '-keystore',
                             privkeydir + str(chosenprivatekey),
                             '-storepass',
                             keystorepass,
                             usapks + APK,
                             alias,
                             #'-verify',
                             #'-verbose',
                             #'-certs'
            ])
            # Now we try to put the signed apk into the signed folder
            try:
                os.rename(usapks + APK, sapks + APK)
            except FileExistsError:
                # If the file already exists, we move signed file out and replace
                os.rename(sapks + APK, tmp + '_T' + APK)
                os.rename(usapks + APK, sapks + APK)
            except PermissionError:
                # If the unsigned apk is open, this error is raised
                print()
                print('Seems ' + APK + ' is open elsewhere. Unable to continue')
                input('Press Enter to Quit to Menu')
                print()
                mainmenu()
            # Restore the unsigned apk.
            os.rename(tmp + APK, usapks + APK)
            # Clean up
            shutil.rmtree(tmp)
            signcount += 1
    print()
    print('Signing has finished, please check the messages above for any errors.')
    # Keystore password is overwritten, then deleted. Alias is also deleted
    keystorepass = '_0_'
    del keystorepass, alias
    print('Your KEYSTORE password has been cleared')
    input('Press Enter to continue')
    print()
    # Clear other objects
    del apklist, apkcount, signcount, chosenprivatekey
    # Return to the menu
    mainmenu()


def genprivkey():
    import subprocess
    import os

    global privkeydir, keytool

    os.system('cls')
    # Generic warning about trusting some code from a random bloke on the intertubes
    print('''
    WARNING
    -------

    You are about to generate a private key to sign (potentially) your own apps.
    You are doing this using software that you have not authored yourself.
    Exercise extreme caution when inputting passwords and/or aliases.
    If you did not download this from XDA-Developers, be even more cautious.

    If you wish full source is available to download, inspect & compare.
    https://github.com/andyharney/pySignare
    ''')
    print()
    # Grab some info from the user to smooth out the key generation
    usralias = input('Choose Desired Alias : ')
    keypass = input('Choose a Desired KEY (not keystore) Password : ')
    # Keypass has to be at least 6 chars long, its re-entered until it is.
    while len(keypass) < 6:
        print('Your Key Password MUST be greater than 6 characters, try again')
        keypass = input('Choose Desired KEY Password : ')
    subprocess.call(['./Files/' + keytool,
                     '-genkey',
                     '-v',
                     '-keystore',
                     privkeydir + str(usralias) + '-private-key.keystore',
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
    print('Please Check the Above Log for Any Errors')
    input('Press Enter to Continue')
    # Overwrite keypass
    keypass = '_0_'
    # Delete the keypass & usralias objects
    del usralias, keypass
    mainmenu()


def zipalignfunc():
    import os
    import subprocess

    global sapks, zaapks, zipalign

    os.system('cls')
    print('\n' + 'Zip Aliging' + '\n')
    zipaligncount = 0
    apklist = os.listdir(sapks)
    apkcount = len(apklist)
    if len(apklist) == 0:
        print('No Signed APKs Found' + '\n')
        input('Press Enter to Return to Menu')
        print()
        mainmenu()
    else:
        while zipaligncount != apkcount:
            for APK in apklist:
                print(APK)
                subprocess.call(['./Files/' + zipalign,
                                 '-f',
                                 '4',
                                 sapks + APK,
                                 zaapks + APK
                ])
            zipaligncount += 1
    print()
    print('Zip Aligning has finished, please check the messages above for any errors.')
    input('Press Enter to Continue')
    print()
    # Clear out the objects
    del zipaligncount, apklist, apkcount
    mainmenu()


operatingsystem()
