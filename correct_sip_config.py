import netmiko,csv,sys,os,datetime,re,arrow

sys.path.insert(0, 'modules')
from connect_to_device import send_commands_to_OLT
from inputfromuser import canweproceed

hostsfile = input('Please Provide the Hosts file name: ')
hosts_checked = 'Cleaned_'+hostsfile
configfile = os.path.join('modules','commandsfile.txt')

failedOLTs=[]

def clean_sip_config(hosts,V):
	with open (hosts,'r') as olts_input, open(hosts_checked,'w') as outfile:
		used=set()
		unique = [x for x in olts_input if x not in used and (used.add(x) or True)]
		outfile.writelines(''.join(unique))
		print('\nThe following OLTs will be processed')
		for i in unique:
			if (i.split(',')[0]).startswith('#') or i =='\n':
				continue
			print(i.rstrip('\n').split(',')[0])
		print('\n')
		canweproceed()
###Processing the OLTs mentioned in the hosts file, and create a logs.txt file which provides the time the OLT was processed, and if it failed or passed.	
	with open (hosts_checked,'r',newline='') as inputfile, open('logs.txt','a') as logsfile:
		csv_r = csv.reader(inputfile)
		number_of_OLTs=0
		for line in csv_r:
			if line ==[]:
				continue
			elif str(line[0]).startswith('#'):
				continue
			else:
				failed_host = send_commands_to_OLT(line[0],(line[1]),(line[2]),configfile,V)
				if failed_host!=None:
					logsfile.writelines(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+' Processing OLT: '+line[0]+'---Failed'+'\n')
				else:
					logsfile.writelines(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+' Processing OLT: '+line[0]+'---Success'+'\n')
				number_of_OLTs+=1
				failedOLTs.append(failed_host)
		print('Script Completed...\n'+('~'*79)+'\nYou will find the scripts files under the directory < outputfiles > for each OLT IP')
		return number_of_OLTs
		


def main():
	olts_processed = clean_sip_config(hostsfile,'Yes')
	#after script completion the below lines will be displayed to the user. If failures to connect to OLTs occure, the failed OLTs list will be given to the user. 
	print('Total Number of OLTs processed =', olts_processed)
	print('Total Number of OLTs scuessfully connected =', (olts_processed-len([x for x in failedOLTs if x!=None])))
	print('Total Number of OLTs failed to connect =', len([x for x in failedOLTs if x!=None]))
	if len([x for x in failedOLTs if x!=None])>0:
		print('\n'+'~'*79)
		print('\nThe following OLTs failed to connect please check them again:')
		for i in failedOLTs:
			if i !=None:
				print(i)
	

if __name__=='__main__':
	main()
