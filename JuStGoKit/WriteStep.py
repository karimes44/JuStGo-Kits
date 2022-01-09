"""
Read a "panoptic" file and writes out the step files.

Syntax:
First line of the file must contain ![<n>]! where <n> is the number of step
files to be written.

Below blocks of code are identified by prepended and appended lines that
contain block command like:
 ![<streamlist>]!
<block code>
 ![<next_streamlist>]
where <streamlist> is a ascending list of stream indices, e.g. 1,3,5-7,12+. This would mean that this block is part of the stream, 1,3,5,6,7,12 and any stream with an index higher than 12.

A stream list is active until the next stream list is defined. Nesting is not supported.
"""

# Read pano file:
#fLoc = './Warehouse/'
#fName = 'Warehouse'
#fLoc = './15squares/'
#fName = '15sqr'
#fLoc = './Pong/'
#fName = 'Pong'
fLoc = './Mastermind/'
fName = 'Mastermind'
with open(fLoc + 'pano/' + fName + '_pano.html') as fin:
	lines = fin.readlines()
fin.close()

line0 = lines[0]
stt   = line0.find('![')
end   = line0.find(']!')
nTSK  = int(line0[stt+2:end])
print('Number of Tasks is {:d}'.format(nTSK))

# set-up default mask and output streams
htmls = []
diffs = []
maskF = []
maskT = []
for i in range(nTSK):
	maskF.append(False)
	maskT.append(True)
	htmls.append('')
	diffs.append('')
mask = maskF[:]

il = 1
for line in lines[1:]:
	print('Reading line '+str(il)+': ' + line)
	il += 1
	
	# Does the line contain a BLK command?
	stt = line.find('![')
	
	if stt != -1:
		# Y:Process stream list cmd
		mask = maskF[:]

		end = line.find(']!')
		strmstr = line[stt+2:end]

		strms = strmstr.split(',')
		for strm in strms:
			print('Found stream: ' + str(strm))
			if strm.find('-') != -1:
				sttend = strm.split('-')
				stt = int(sttend[0])
				end = int(sttend[1])+1
				print('stt: {:d} -- end: {:d}'.format(stt,end))
				for i in range(stt,end):
					mask[i] = True
			elif strm[-1] == '+':
				n = int(strm[0:-1])
				for i in range(n,nTSK):
					mask[i] = True
			else:
				n = int(strm)
				mask[n] = True
		print('Mask     is: ' + str(mask))
	else:
		for i in range(nTSK):
			if mask[i]:
				if i == nTSK-1:
					out=line.replace("$STREAM$",'')
				else:
					out=line.replace("$STREAM$",'/'+str(i))
				htmls[i] += out
				if i == 0:
						diffs[i] += out
				elif i > 0 and not mask[i-1]:
						# print('Diff: ' + out)
						diffs[i] += out

# Writing out the streams:
print('===========================')
for i in range(nTSK):
	print('Stream {:d}'.format(i))
	# print(htmls[i])
	if i == nTSK-1:
		fou = open(fLoc + fName +'.html','w')
		fdi = open(fLoc + 'pano/' + fName+'_diff.txt','w')
	else:
		fou = open(fLoc + fName + '_step{:d}.html'.format(i),'w')
		fdi = open(fLoc + 'pano/' + fName + '_step{:d}_diff.txt'.format(i),'w')

	fou.write(htmls[i])
	fou.close()
	fdi.write(diffs[i])
	fdi.close()

