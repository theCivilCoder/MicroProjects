f = open(r'D:\Coding\100. Projects\D2LCalendar\calendar.txt', 'r')

rep1 = "ENSF 612 L01 - (Fall 2021) - Engineering Large Scale Data Analytics Systems"
rep1a = "ENSF 612 - "

rep2 = "ENSF 611 L01 - (Fall 2021) - Machine Learning for Software Engineers"
rep2a = "ENSF 611 - "

rep3 = "Repeats on Monday every week at 12:00 PM until Dec 8, 2021"
rep4 = "ENSF 611 - ENSF 611 L01 - (Fall 2021) - LectureRepeats on Monday and Wednesday every week at 3:30 PM until Dec 8, 2021Dec 6, 2021 3:30 PM - 4:45 PM"

for line in f:
	line = line.replace('\n','').replace(rep1, rep1a).replace(rep2, rep2a).replace(rep3, "")
	if "until Dec 8" in line:
		continue
	# if (rep1a in line or rep2a in line):
	if (rep1a in line):	
		print(line)