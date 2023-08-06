"""

The DotENV Package

"""

import os as __os
import time as __time
import colorama as __colorama
from colorama import Fore as __Fore

__colorama.init()

def __Error(message):
    print(__Fore.WHITE + __time.strftime("%m/%d/%Y | %H:%M:%S") + f"{__Fore.RED}  [DOTENV | ERROR]  {message}")

__envFileLines: list[str] = None

def config():
    """
        Configure the DotENV.
    """
        
    curPath = __os.getcwd()
    files = __os.listdir(curPath)
    envFile: str = None
    envPath: str = None

    for i, v in enumerate(files):
        if(v == ".env"):
            envFile = v
            envPath = f"{curPath}\{envFile}"
            break

    try:
        with open(envPath, "r") as file:
            global __envFileLines
            __envFileLines = file.readlines()

            try:
                __envFileLines[0]
            except:
                __envFileLines = None
                return __Error("The .env is empty!")

            for i, v in enumerate(__envFileLines):
                __envFileLines[i] = v.replace("\n", "")

                try:
                    __envFileLines[i].split("=")[1]
                except:
                    return __Error("A Key has no value!")

    except:
        __Error("Could not find the .env, Please Create a .env file!")

def get_value(key: str):
    """
        Get The Value from a specified key.
        \n
        Will throw a error if the DotENV is not configured (config()).
    """


    if(__envFileLines == None):
        __Error("Hm, are you sure that the library is configured?")
        return None
    
    value: str = None

    for i, v in enumerate(__envFileLines):
        if(v.split("=")[0] == key):
            value = v.split("=")[1]
            break

    return value

def exists(key: str):
    """
       Try to find if a key exists in the DotENV.
       \n
       Will throw an error if the DotENV is not configured (config()).
    """

    if(__envFileLines == None):
        __Error("Hm, are you sure that the library is configured?")
        return None
    
    value: str = None

    for i, v in enumerate(__envFileLines):
        if(v.split("=")[0] == key):
            value = v.split("=")[1]
            break

    return value != None