# MicronPro worker
this doccument outlines the installation of the MicronPro worker software. This program is used in additon with the cloud hosted application which renders the frontend web app. 

# About the program 
This program should be set up on the computer on which the images of the filters will be taken. This computer acts a 'worker' computer in the MicronPro platform. From the web app users will be able to configure and run jobs on worker computers. This is done to avoid the transfer of the images back and forth from a cloud and instead stores all the relavant data in the cloud (AWS heroku server).

## Requirements
    -Python 3.6> [Download from here](https://www.python.org/downloads/)
### Build Dependencies
    if you are installing this on a windows machine you will need to install the latest version of the "Build Tools for visual studio". This is required because the python packages included use low-level c compilers. This can cause issues on some platforms but not on others.
    
    Download build tools: https://visualstudio.microsoft.com/downloads/#

## Installation
    1. run provided file titled "install.bat" from the file explorer
        -this file runs creates a python virual enviroment and begins to install dependencies
        -if the command prompt appears frozen for a long period of time (60s) and doesnt appear to be doing anything click in the window and hit any key.
        -many lines will scroll accross the screen often ending with some yellow text about a pip upgrade and this can be ignored. if there is a large red error please see the troubleshooting section

## Running The Program
 To run the Program open the file run.bat and a terminal window will popup with some messages about the startup of the application.

## Configuation
in the folder titled .config (if this folder is not there right away it will be created after the first time it attempts to start) there are important values that need to be properly set to allow the computer to connect to the heroku server. for questions and complete config files email jkdev222@gmail.com



## TroubleShooting
    -"error building wheels"
        This could be an issue with how the system tried to build the dependencies. 
    - app flashes terminal up then closes
      - this may be an issue with requirements not being installed, please run the install again and note any errors
      - could also be caused by the folder of the project being named 'micronPro-worker-master' if this is the case change the folder to 'micronPro-worker'
    - 

## Updating 





