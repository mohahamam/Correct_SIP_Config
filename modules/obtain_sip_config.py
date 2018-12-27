import csv,re

def geting_voip_sip_config(inputfile,outputfile):
	with open (inputfile,'r') as raw_config ,open (outputfile,'w') as ouput_content:
		configuraiton = raw_config.readlines()
		
		for line in configuraiton:
			if 'sip-config ont:' in line:
				ouput_content.write(('configure voice ont '+line.lstrip(r' *').rstrip('\n')+' '))
			elif 'proxyserv-prof-name' in line:
				ouput_content.write((line.lstrip(r' *').replace('-name ', ' name:').replace('name:""', 'none').rstrip('\n')+' '))
			elif 'outproxyserv-prof-name' in line:
				ouput_content.write((line.lstrip(r' *').replace('-name ', ' name:').replace('name:""', 'none').rstrip('\n')+' '))
			elif 'aor-host-prt-prof-name' in line:
				ouput_content.write((line.lstrip(r' *').replace('-name ', ' name:').replace('name:""', 'none').rstrip('\n')+' '))
			elif 'registrar-prof-name' in line:
				ouput_content.write(line.lstrip(r' *').replace('-name ', ' name:').replace('name:""', 'none '))
			else:
				continue
				
def convert_config(inputfile,outputfile):
	inspectedLine01 = ' proxyserv-prof name:ims.etisalat.ae outproxyserv-prof name:asbg.ims.etisalat.ae aor-host-prt-prof name:ims.etisalat.ae registrar-prof name:asbg.ims.etisalat.ae'
	inspectedLine02 =  'registrar-prof name:asbg.ims.etisalat.ae'
	inspectedLine03 =  'proxyserv-prof name:ims.etisalat.ae'
	
	with open (inputfile,'r') as sip_config, open (outputfile,'w') as new_sip_config:
		old_sip_config =sip_config.readlines()
		for line in old_sip_config:
			if inspectedLine01 in line:
				new_sip_config.write(line.replace('proxyserv-prof name:ims.etisalat.ae','proxyserv-prof none').replace('registrar-prof name:asbg.ims.etisalat.ae','registrar-prof none'))
			elif inspectedLine02 in line:
				new_sip_config.write(line.replace('registrar-prof name:asbg.ims.etisalat.ae','registrar-prof none'))
			elif inspectedLine03 in line:
				new_sip_config.write(line.replace('proxyserv-prof name:ims.etisalat.ae','proxyserv-prof none'))
			else:
				continue
def reboot_ONTs(input01,output01):
	ont_regex = re.compile(r'(\b1/1(/(1[0-6]|[1-9])){2}/(109|119|1[0-2][0-8]|[1-9][0-9]|[1-9])\b)')
	with open (input01) as file1, open(output01,'w') as outfile:
		onts = file1.read()
		ont = ont_regex.findall(onts)
		ontlist = [ont[i][0]for i,x in enumerate(ont)]
		used=set()
		unique = [x for x in ontlist if x not in used and (used.add(x) or True)]
		#print('\n'.join(unique))
		for i in unique:
			outfile.writelines('admin equipment ont interface '+i+' reboot with-active-image\n')	
def main():
	geting_voip_sip_config('sample.txt','sample1.txt')
	convert_config('sample1.txt','finalconfig.txt')
	reboot_ONTs('listoflines.txt', 'rebootONTs.txt')

if __name__=='__main__':
	main()
