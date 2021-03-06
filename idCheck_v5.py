import xml.etree.ElementTree as ET
import Levenshtein
import os

minratio = 0.07

def skoryaz(skor1, skor2, root, tag = str):
	for j in root.findall(tag):
		if j.attrib == {"lang": "en"}:
			j.set('skor', skor1)
		elif j.attrib == {"lang": "tr"}:
			j.set('skor', skor2)

def karsilastir(a, b):
	if Levenshtein.ratio(a,b) < minratio:
		if len(a) > len(b): return '21'
		elif len(b) > len(a): return '22'
		else: return '23'
	elif Levenshtein.ratio(a,b) == 1:
		if a == u'None': return '24'
		else: return '1.0'
	else: return str(Levenshtein.ratio(a,b))
	
list = []
for filename in os.listdir('elas-u'):
        a = filename.split('-')
        list.append(a[0])

for i in list:
	dosyalar = ['elas-u/{}-u.xml'.format(i),'xmller/{}-dp.xml'.format(i)]
	kok = []

	for dosya in dosyalar:
        	tree = ET.parse(dosya)
       		root = tree.getroot()
        	kok.append(root)

	baslik1 = baslik2 = baslik3 = baslik4 = doi1 = doi2 = ozet1 = ozet2 = ozet3 = ozet4 = u''

	for child in kok[0]:
		if child.tag == 'title' and child.attrib == {"lang": "en"}:
			baslik1 = unicode(child.text)
		elif child.tag == 'title' and child.attrib == {"lang": "tr"}:
			baslik3 = unicode(child.text)
		elif child.tag == 'doi':
			doi1 = unicode(child.text)
		elif child.tag == 'abstract' and child.attrib == {"lang": "en"}:
			ozet1 = unicode(child.text)
		elif child.tag == 'abstract' and child.attrib == {"lang": "tr"}:
			ozet3 = unicode(child.text)

	for child in kok[1]:
        	if child.tag == 'title' and child.attrib == {"lang": "en"}:
                	baslik2 =  unicode(child.text)
		elif child.tag == 'title' and child.attrib == {"lang": "tr"}:
			baslik4 = unicode(child.text)
		elif child.tag == 'doi':
			doi2 = unicode(child.text)
		elif child.tag == 'abstract' and child.attrib == {"lang": "en"}:
			ozet2 = unicode(child.text)
		elif child.tag == 'abstract' and child.attrib == {"lang": "tr"}:
			ozet4 = unicode(child.text)

	for keywords in kok[0].findall('keywords'):
		if keywords.attrib == {"lang": "en"}:
			p = False
			for keyword in keywords.findall('keyword'):
				p = True
				anahtar = unicode(keyword.text)
				liste1 = ['21']
				for keys in kok[1].findall('keywords'):
					if keys.attrib == {"lang": "en"}:
						if liste1 == ['21']: liste1 = []
						for key in keys.findall('keyword'):
							anahtar2 = unicode(key.text)
							liste1.append(str(Levenshtein.ratio(anahtar, anahtar2)))
				if not liste1 == []:
					keyword.set('skor', max(liste1))
				else:
					keyword.set('skor', '21')
			if p == False: keywords.set('skor', '22')
		elif keywords.attrib == {"lang": "tr"}:
			q = False
			for keyword in keywords.findall('keyword'):
				q = True
				anahtar = unicode(keyword.text)
				liste2 = ['21']
				for keys in kok[1].findall('keywords'):
					if keys.attrib == {"lang": "tr"}:
						if liste2 == ['21']: liste2 = []
						for key in keys.findall('keyword'):
							anahtar2 = unicode(key.text)
							liste2.append(str(Levenshtein.ratio(anahtar, anahtar2)))
				if not liste2 == []:
					keyword.set('skor', max(liste2))
				else:
					keyword.set('skor', '21')
			if q == False: keywords.set('skor', '22')

	for authors in kok[0].findall('authors'):
		o = False
		for author in authors.findall('author'):
			o = True
			yazar = unicode(author.text)
			liste3 = ['20']
			for aauthors in kok[1].findall('authors'):
				for aauthor in aauthors.findall('author'):
					if liste3 == ['20']: liste3 = []
					yazar2 = unicode(aauthor.text)
					liste3.append(str(Levenshtein.ratio(yazar, yazar2)))
			author.set('skor', max(liste3))
		if o == False:
			authors.set('skor', '22') 

	baslikskor = karsilastir(baslik1, baslik2)
	baslikskor2 = karsilastir(baslik3, baslik4)
	doiskor = karsilastir(doi1, doi2)
	ozetskor = karsilastir(ozet1, ozet2)
	ozetskor2 = karsilastir(ozet3, ozet4)

	for j in kok[0].findall('doi'):
		j.set('skor', doiskor)

	skoryaz(baslikskor, baslikskor2, kok[0], 'title')
	skoryaz(ozetskor, ozetskor2, kok[0], 'abstract')

	agac = ET.ElementTree(kok[0])
	agac.write('xmloutput/{}-skor.xml'.format(i))
