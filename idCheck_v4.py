import xml.etree.ElementTree as ET
import Levenshtein
import os

list = []
for filename in os.listdir('elas-u'):
        a = filename.split('-')
        list.append(a[0])

#def log():
#	with open("log.txt", "a") as myfile:
#		myfile.write('dosya:{0}, title-en:{1}, title-tr:{2}, doi:{3}, abstract-en:{4}, abstract-tr:{5}, keywords-en:{6}, keywords-tr:{7}, authors:{8}\n\n'.format(dosya1, baslikskor, baslikskor2, doiskor, ozetskor, ozetskor2, anahtarskor, anahtarskor2, yazarskor))

for i in list:
	dosya1 = 'elas-u/{}-u.xml'.format(i)
	dosya2 = 'xmller/{}-dp.xml'.format(i)

	tree1 = ET.parse(dosya1)
	root1 = tree1.getroot()

	tree2 = ET.parse(dosya2)
	root2 = tree2.getroot()

	baslik1 = unicode('')
	for child in root1:
		if child.tag == 'title' and child.attrib == {"lang": "en"}:
			baslik1 = unicode(child.text)

	baslik2 = unicode('')
	for child in root2:
        	if child.tag == 'title' and child.attrib == {"lang": "en"}:
                	baslik2 =  unicode(child.text)

	baslik3 = unicode('')
	for child in root1:
		if child.tag == 'title' and child.attrib == {"lang": "tr"}:
			baslik3 = unicode(child.text)

	baslik4 = unicode('')
	for child in root2:
		if child.tag == 'title' and child.attrib == {"lang": "tr"}:
			baslik4 = unicode(child.text)

	doi1 = unicode('')
	for child in root1:
		if child.tag == 'doi':
			doi1 = unicode(child.text)

	doi2 = unicode('')
	for child in root2:
		if child.tag == 'doi':
			doi2 = unicode(child.text)
		
	ozet1 = unicode('')
	for child in root1:
		if child.tag == 'abstract' and child.attrib == {"lang": "en"}:
			ozet1 = unicode(child.text)

	ozet2 = unicode('')
	for child in root2:
		if child.tag == 'abstract' and child.attrib == {"lang": "en"}:
			ozet2 = unicode(child.text)

	ozet3 = unicode('')
	for child in root1:
		if child.tag == 'abstract' and child.attrib == {"lang": "tr"}:
			ozet3 = unicode(child.text)

	ozet4 = unicode('')
	for child in root2:
		if child.tag == 'abstract' and child.attrib == {"lang": "tr"}:
			ozet4 = unicode(child.text)

	for keywords in root1.findall('keywords'):
		if keywords.attrib == {"lang": "en"}:
			for keyword in keywords.findall('keyword'):
				anahtar = unicode(keyword.text)
				liste1 = ['20']
				for keys in root2.findall('keywords'):
					if keys.attrib == {"lang": "en"}:
						if liste1 == ['20']: liste1 = []
						for key in keys.findall('keyword'):
							anahtar2 = unicode(key.text)
							liste1.append(str(Levenshtein.ratio(anahtar, anahtar2)))
				keyword.set('skor', max(liste1))
		elif keywords.attrib == {"lang": "tr"}:
			for keyword in keywords.findall('keyword'):
				anahtar = unicode(keyword.text)
				liste2 = ['20']
				for keys in root2.findall('keywords'):
					if keys.attrib == {"lang": "tr"}:
						if liste2 == ['20']: liste2 = []
						for key in keys.findall('keyword'):
							anahtar2 = unicode(key.text)
							liste2.append(str(Levenshtein.ratio(anahtar, anahtar2)))
				keyword.set('skor', max(liste2))

	for authors in root1.findall('authors'):
		for author in authors.findall('author'):
			yazar = unicode(author.text)
			liste3 = ['20']
			for aauthors in root2.findall('authors'):
				for aauthor in aauthors.findall('author'):
					if liste3 == ['20']: liste3 = []
					yazar2 = unicode(aauthor.text)
					liste3.append(str(Levenshtein.ratio(yazar, yazar2)))
			author.set('skor', max(liste3))

	baslikskor = str(Levenshtein.ratio(baslik1, baslik2))
	baslikskor2 = str(Levenshtein.ratio(baslik3, baslik4))
	doiskor = str(Levenshtein.ratio(doi1, doi2))
	ozetskor = str(Levenshtein.ratio(ozet1, ozet2))
	ozetskor2 = str(Levenshtein.ratio(ozet3, ozet4))

#	log()
	
	for j in root1.findall('title'):
		if j.attrib == {"lang": "en"}:
			j.set('skor', baslikskor)
		elif j.attrib == {"lang": "tr"}:
			j.set('skor', baslikskor2)
	for j in root1.findall('doi'):
		j.set('skor', doiskor)
	for j in root1.findall('abstract'):
		if j.attrib == {"lang": "en"}:
			j.set('skor', ozetskor)
		elif j.attrib == {"lang": "tr"}:
			j.set('skor', ozetskor2)

	agac = ET.ElementTree(root1)
	agac.write('xmloutput/{}-skor.xml'.format(i))
