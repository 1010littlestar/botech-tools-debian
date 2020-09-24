#!/usr/bin/python2.7

import os
import sys
import subprocess
import time
import csv

I2CADDR_200 = "0x92"
I2CADDR_3559 = "0x90"

TEMP_CMD = "i2c_read 0x2 %s 0x00 0x00 1 2 2> /dev/null | sed -n '5p'  | awk '{print $2}'"

def init_i2c():
	subprocess.Popen("himm 0x1f000090 0x1403 &> /dev/null", shell=True)
	subprocess.Popen("himm 0x1f000094 0x1403 &> /dev/null", shell=True)
	

def get_temp(i2caddr):
	cmd = TEMP_CMD % (i2caddr)
	ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	line = ret.stdout.readline()
	value = line.strip('\r\n')
	return (int(value, 16) / 16 * 0.0625)

def main():
	color200 = '\033[1;32m'
	color500  = '\033[1;32m'

	init_i2c()

	try:
		csvfile = open("/tmp/test.csv", "w")
		writer = csv.writer(csvfile)
		while True:
			temp200 = get_temp(I2CADDR_200)
			temp3559 = get_temp(I2CADDR_3559)

			writer.writerow([int(time.time()), temp200, temp3559])

			if temp200 > 50 :
				color200 = '\033[1;31m'
			if temp3559> 50 :
				color500 = '\033[1;31m'
			format = "\ratlas200 temperature:[%s%0.01f\033[0m C]     hi3559 temperature:[%s%0.01f\033[0m C]" % \
				 (color200, temp200, color500, temp3559)
			sys.stdout.write(format)
			sys.stdout.flush()
			time.sleep(1)
	except KeyboardInterrupt:
		csvfile.close()
		pass

if __name__ == '__main__':
	main()

