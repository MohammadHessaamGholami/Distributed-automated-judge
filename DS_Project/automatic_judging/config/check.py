import time
import os, sys
import subprocess as sub


def check(code, sample_input, sample_output):

	sample_output_list = []
	sample_input_list = []	
	input_file = open(sample_input, "r")
	output_file = open(sample_output, "r")	
	for line in input_file:
		
		sample_input_list.append(line.rstrip())

	for line in output_file:
		sample_output_list.append(line.rstrip())

	#print(sample_input_list)
	#print(sample_output_list)

	grade = int(100/ len(sample_input_list)) 
	score = 0 
	running_time = 0

	#answer_file = open(code, "w")
	for i in range(len(sample_input_list)):
			tic = time.perf_counter()
			result = (os.popen("python3 "+code + ' '+ sample_input_list[i]).readline())
			toc = time.perf_counter()
			running_time += (toc-tic)
			if str(result) == sample_output_list[i]:
				score += grade				
				#print("***")
	#print(f"running time is {running_time:0.4f} seconds")
	#print("score is",end=' ')
	#print(score)
	input_file.close()
	output_file.close()
	print (running_time, score, end='')
try:
	check(sys.argv[1],sys.argv[2],sys.argv[3])
except:
	print(0,0)

		
		
