# Assign04.py programmed by Sean Murren
# CMSC331 Spring 2015
# Python v3+

import os
import subprocess
import time
import datetime


def updateLog(logFile, time, testResult):
	log = open(logFile,'a')
	log.write(time + "  " + testResult + "\n")
	log.close()

	
def main():
	
	javaFile = "Assign01"
	inputFile = "beFile.huge"
	outputFile =  "output.huge"
	expectedOutputFile = "csvFile.huge"
	option = ""
	logFilename = "log.txt"
	newFailDir = ""
	newTime = ""
	
	modifyTimeVal = os.path.getmtime("./app/" + javaFile + ".java")
	
	
	for i in range(10):
		print("-------------------------")
		print("Starting Run " + str(i+1))
		
		tempTimeVal = os.path.getmtime("./app/" + javaFile + ".java")
		
		# check if different
		if modifyTimeVal != tempTimeVal:
			
			newTime = str(datetime.datetime.now())
			modifyTimeVal = tempTimeVal
			
			# remove space from time info
			for j in range(len(newTime)):
				if newTime[j] == " ":
					newTime = newTime[:j] + "_" + newTime[j+1:]
		
			# recompile
			subprocess.call("javac app/" + javaFile + ".java", 
							stdout=None, stderr=None,shell=True)
			# run
			subprocess.call("java app/" + javaFile + " " + option + " input/" + inputFile + " " + outputFile,
						    stdout=None, stderr=None,shell=True)
			
			# check for errors
			diff = subprocess.call("diff -q -N ./expected/"+expectedOutputFile+" "+outputFile,
			                        stdout=None, stderr=None,shell=True)
			
			
			#if diff, create new fail folder and move file there
			if diff == 1: 
				newFailDir = "./fail/" + newTime
				os.mkdir(newFailDir)
				os.rename(outputFile, newFailDir + "/" + outputFile)
				#update log
				updateLog(logFilename, newTime, "\tFail")
				
			#else remove new output
			else:
				os.remove(outputFile)
				#update log
				updateLog(logFilename, newTime, "\tPass")
				
			
		# sleep 5s
		print("Snooze " + str(i+1) + "\n")
		time.sleep(5)


main()