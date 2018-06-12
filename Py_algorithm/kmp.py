#! -*- coding:utf-8 -*-

def getNext(data):
	dataLen = len(data)
	k=0
	i = 1	
	arrayNext=[0]*dataLen		
	while i<dataLen:
		if data[i] == data[k]:
			k = k + 1
			arrayNext[i] = k
			i = i + 1
		elif k == 0:
			arrayNext[i] = k
			i = i+1
		else:
			k = arrayNext[k-1]
	return arrayNext
def KMP(data1,data2):
	iRet = -1
	arrayNext=getNext(data2)
	len1=len(data1)
	len2=len(data2)
	i = 0
	j = 0
	while i<len1 and j < len2:
		if data1[i] == data2[j]:
			i=i+1
			j=j+1
		elif j == 0:
			i = i + 1
		else:
			j=arrayNext[j-1]

	if j == len2:
		iRet = i-len2	
	elif i == len1:
		pass
	return iRet
if __name__=="__main__":
	iRet = KMP("abcabc","abc")
	if iRet == -1:
		print "Sorry,not find" 
	else:
		print "pos is:",iRet