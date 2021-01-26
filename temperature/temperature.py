#!/usr/bin/python2.7

import os
import sys
import subprocess
import time
import csv

I2CADDR_200 = "0x92"
I2CADDR_3559 = "0x90"

MISC_CTRL28 = "0x12030070"
MISC_CTRL29 = "0x12030074"
MISC_CTRL30 = "0x12030078"

MISC_CTRL28_VALUE = "0xfffc1cc3"
MISC_CTRL29_VALUE = "0x1c"

TEMP_CMD = "i2c_read 0x2 %s 0x00 0x00 1 2 2> /dev/null | sed -n '5p'  | awk '{print $2}'"
CORETEMP_CMD = "himd %s | sed -n '4p' | awk '{print $3$2}'" %  MISC_CTRL30


def init_i2c():
	subprocess.Popen("himm 0x1f000090 0x1403 &> /dev/null", shell=True)
	subprocess.Popen("himm 0x1f000094 0x1403 &> /dev/null", shell=True)

def init_coresensor():
        cmdtmp = "himm %s %s &> /dev/null" % (MISC_CTRL28, MISC_CTRL28_VALUE)
        cmdtmp = "himm %s %s &> /dev/null" % (MISC_CTRL29, MISC_CTRL29_VALUE)
	subprocess.Popen(cmdtmp, shell=True)

def get_temp(i2caddr):
	cmd = TEMP_CMD % (i2caddr)
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	line = ret.stdout.readline()
	value = line.strip('\r\n')
	return (int(value, 16) / 16 * 0.0625)

def get_coretemp():
	cmd = CORETEMP_CMD
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	line = ret.stdout.readline()
	value = line.strip('\r\n')
	return (((float(int(value, 16) - 116) / 806) * 165) - 40)

def main():
	color200 = '\033[1;32m'
	color500  = '\033[1;32m'
	corecolor = '\033[1;32m'

	init_i2c()
        init_coresensor()

	try:
		csvfile = open("/tmp/test.csv", "w")
		writer = csv.writer(csvfile)
		while True:
			temp200 = get_temp(I2CADDR_200)
			temp3559 = get_temp(I2CADDR_3559)
                        coretemp  = get_coretemp();

			writer.writerow([int(time.time()), temp200, temp3559, coretemp])

			if temp200 > 50 :
				color200 = '\033[1;31m'
			if temp3559 > 50 :
				color500 = '\033[1;31m'
                        if coretemp > 95 :
				corecolor= '\033[1;31m'

			format = "\x1b[1A \ratlas200 temperature:[%s%0.01f\033[0m C]     hi3559 temperature:[%s%0.01f\033[0m C] \n\rcore temperature: [%s%0.01f\033[0m  C]" % (color200, temp200, color500, temp3559, corecolor, coretemp)
			sys.stdout.write(format)
			sys.stdout.flush()
			time.sleep(1)
	except KeyboardInterrupt:
		csvfile.close()
		pass


if __name__ == '__main__':
	main()

