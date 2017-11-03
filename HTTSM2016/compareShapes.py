#!/usr/bin/env python
from ROOT import *
import os

gROOT.SetBatch(True)

folder1 = "WAW"
folder2 = "USCMS"
os.system("rm -rf "+folder1+"_"+folder2)
os.mkdir(folder1+"_"+folder2)

fileNameMT = "htt_mt.inputs-sm-13TeV-2D.root"
fileNameTT = "htt_tt.inputs-sm-13TeV-2D.root"

mainCategories = ["0jet", "boosted", "vbf"]
mtCR = ["antiiso", "wjets"]
ttCR = ["qcd",]

def getHisto(inFile, directory, name):
	histo = inFile.Get(directory+"/"+name)
	if histo == None:
		print "Histo "+directory+"/"+name+" not found in file "+inFile.GetName()
	return histo

def saveHisto(histo, directory):
	c = TCanvas()
	histo.Draw()
	c.Print(folder1+"_"+folder2+"/"+directory+"/"+histo.GetName()+".png")
	
def save2histos(h1, h2, directory):
	c = TCanvas()
	c.Divide(1,2)
	c.GetPad(1).SetPad(0.01,0.29,0.99,0.99)
	c.GetPad(2).SetPad(0.01,0.01,0.99,0.29)
	c.cd(1)
	maxH=h1.GetMaximum() if h1.GetMaximum()>h2.GetMaximum() else h2.GetMaximum()
	h1.ResetAttFill()
	h2.ResetAttFill()
	h1.ResetAttMarker()
	h2.ResetAttMarker()
	h1.SetMarkerStyle(20)
	h1.SetStats(kFALSE)
	h2.SetStats(kFALSE)
	h1.SetMaximum(1.1*maxH)
	h1.SetTitle(h1.GetName())
	h1.Draw()
	h2.SetLineColor(kRed)
	h2.Draw("same hist")
	legend = TLegend(0.8, 0.8, 0.99, 0.99)
	legend.AddEntry(h1, folder1)
	legend.AddEntry(h2, folder2)
	legend.Draw()
	c.cd(2)
	diff = h1.Clone()
	diff.SetTitle("")
	diff.Divide(h2)
	diff.SetMaximum(1.2)
	diff.SetMinimum(0.8)
	diff.GetYaxis().SetLabelSize(0.1)
	diff.SetStats(kFALSE)
	diff.Draw()
	aLine = TLine(diff.GetXaxis().GetXmin(),1.0,diff.GetXaxis().GetXmax(),1.0)
	aLine.SetLineColor(1)
	aLine.SetLineWidth(2)
	aLine.Draw()
	c.Print(folder1+"_"+folder2+"/"+directory+"/"+h1.GetName()+"_ratio.png")

def compareMainCategories(file1, file2):
	channel = "mt_" if file1.GetName().count("htt_mt")>0 else "tt_"
	dirKeys = file1.GetListOfKeys()
	dirKey = dirKeys.First()
	while dirKey != None:
		dirKey.Print()
		directory = dirKey.ReadObj()
		dirKey = dirKeys.After(dirKey)
		if directory.GetName().count("_cr")>0:
			continue
		histoKeys = directory.GetListOfKeys()
		histoKey = histoKeys.First()
		while histoKey != None:
			histo1 = histoKey.ReadObj()
			histoKey = histoKeys.After(histoKey)
			if (histo1.GetName().count("Up") or histo1.GetName().count("Down")) and histo1.GetName().count("CMS_scale_t")==0:
				continue
			histo2 = getHisto(file2, directory.GetName(), histo1.GetName())
			if histo2 == None:
				continue
			print histo2
			histoDiff = histo1.Clone()
			histoDiff.Add(histo2, -1)
			#saveHisto(histoDiff, directory.GetName())
			save2histos(histo1, histo2, directory.GetName())

def compareMTcr(file1, file2):
	print "mt_cr"
	
def compareTTcr(file1, file2):
	print "tt_cr"

def compare(fileName):
	file1 = TFile("shapes/"+folder1+"/"+fileName)
	file2 = TFile("shapes/"+folder2+"/"+fileName)
	compareMainCategories(file1, file2)
	compareMTcr(file1, file2) if fileName.count("mt")>0 else compareTTcr(file1, file2)
	
for cat in mainCategories:
	os.mkdir(folder1+"_"+folder2+"/mt_"+cat)
	os.mkdir(folder1+"_"+folder2+"/tt_"+cat)

compare(fileNameMT)
compare(fileNameTT)
