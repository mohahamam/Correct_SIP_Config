# Correct_SIP_Config
script that will connect to a list of OLTs you specify in hosts file as attached.

hosts.txt file has the following format
OLTIP,username,password
10.33.72.14,isadmin,ANS#150


To run the script:

./correct_sip_config_04 
Please Provide the Hosts file name: hosts.txt

The following OLTs will be processed
10.33.72.14
10.33.72.15
10.33.72.18
10.33.72.19
11.11.11.11


Are the above inputs correct? (Yes,No):y
Proceeding to Next Steps....



After the execution, you will get a directory called outputfiles  with each OLT IP in a dedicated directory.

The script will not change anything on the OLTs, it will only retrieve all the SIP configurations and generate commands to correct them, and a file to reboot the ONTs. 
These commands should be executed manually per OLT.
For each OLT you will get commands files as below example :
*Original SIP config.  OriginalSipConfig_10.33.72.14_2018-12-26-12-36-24.txt
*Commands needed to modify and correct the voip-sip-config CorrectSipConfig_10.33.72.14_2018-12-26-12-36-24.txt
*Commands needed to reboot the ONTs. RebootONTs_10.33.72.14_2018-12-26-12-36-24.txt


