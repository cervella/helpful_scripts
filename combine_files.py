import os

# define OutputFileName here
OutputFilename = 'CombinedCompleteWorksiteExport.txt'

# define the paths where the files live here
InputPath = '/home/cervella/Downloads'
OutputPath = '/home/cervella/Downloads'

#use os to remove slashes
InputPath = os.path.normpath(InputPath)
OutputPath = os.path.normpath(OutputPath)

# open output file
filename = os.path.join(OutputPath, OutputFilename)
file_out = open(filename, 'w')
print "Output file opened"

# combine files here
for file in os.listdir(InputPath):
	filename = os.path.join(InputPath, file)
	if os.path.isfile(filename):
		print "	Adding :" + file
		file_in = open(filename, 'r')
		content = file_in.read()
		file_out.write(content)
		file_in.close()

# close and save the combined file
file_out.close()
print "Output file closed"