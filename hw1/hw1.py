import requests
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class HW1():
	def __init__(self, filename):
		self.row = []
		self.clz = dict()
		with open(filename) as file:
			for line in file:
				r = self.parseLine(line)
				self.row.append(r)
				if int(r[0]) in self.clz.keys():
					self.clz[int(r[0])] = self.clz[int(r[0])] + 1
				else:
					self.clz.update({int(r[0]):1})
		
	def parseLine(self, text):
		list = []
		for x in text.split(","):
			list.append(float(x))
		return list
		
	def getMeanVector(self, clz, cmd = None):
		count = 0
		mean = np.zeros((1,13))
		for r in self.row:
			if int(r[0]) is clz and self.row.index(r) is not 0:
				if cmd is None:
					mean = np.array(r[1:]) + mean
				elif cmd is "half" and count%2 is 0:
					mean = np.array(r[1:]) + mean
			count = count + 1
		return (mean/count)
		
	def getConvariance(self, clz, cmd = None):
		'''
		# implement of cov
		n = len(self.row[0])
		s = np.zeros((n, n))
		count = 0
		for r in self.row:
			if int(r[0]) is clz:
				count = count + 1
				s = (r - self.getMeanVector(clz,cmd))*(r - self.getMeanVector(clz,cmd)).T + s
				if cmd is not None:
					if count >= self.clz[clz]/2:
						break
		return s/count
		'''
		count = 0
		row = []
		for r in self.row:
			if int(r[0]) is clz and self.row.index(r) is not 0:
				if cmd is None:
					row.append(r[1:])
				elif cmd is "half" and count%2 is 0:
					row.append(r[1:])
			count = count + 1
		ary = np.array(row)
		return np.cov(ary.T, ddof=0)
		
	def plot2D(self, d1, d2):
		color = ["red","blue","yellow"]
		for r in self.row:
			#print(r[d1],r[d2])
			plt.scatter(r[d1], r[d2], c=color[int(r[0])-1], alpha=0.6, edgecolors="black")
		
		strD1 = "D"+str(d1)
		strD2 = "D"+str(d2)
		plt.xlabel(strD1+"-axis") 
		plt.ylabel(strD2+"-axis") 
		plt.title(strD1+" and "+strD2)
		plt.grid(True)
		patch = []
		count = 0
		for c in color:
			count = count + 1
			patch.append(mpatches.Patch(color=c, label='Class'+str(count)))
		plt.legend(handles=patch)
		plt.show()
	
def main():
	filename = "wine.data.txt"
	resultname = "result.txt"
	hw1 = HW1(filename)
	np.set_printoptions(suppress=True)
	f = open("result.txt","w+")
	for i in range(3):
		f.write("\nClass"+str(i+1)+":\n")
		f.write("Mean Vector:\n")
		f.write("\n"+str(hw1.getMeanVector(i+1))+"\n")
		for j in range(100):
			f.write("-")
		f.write("\nConvariance Matrix:\n")
		f.write("\n"+str(hw1.getConvariance(i+1))+"\n")
		
	for j in range(100):
			f.write("-")
			
	for i in range(3):
		f.write("\nClass"+str(i+1)+" (half):\n")
		f.write("Mean Vector:\n")
		f.write("\n"+str(hw1.getMeanVector(i+1,"half"))+"\n")
		for j in range(100):
			f.write("-")
		f.write("\nConvariance Matrix:\n")
		f.write("\n"+str(hw1.getConvariance(i+1,"half"))+"\n")
	
	f.close()
	
if __name__ == "__main__":
	main()