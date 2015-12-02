import xml.etree.ElementTree as ET
import Levenshtein
import os

list = []
for filename in os.listdir('elas-u'):
        a = filename.split('-')
        list.append(a[0])

def log():
	with open("log.txt", "a") as myfile:
		myfile.write('dosya:{0}, title-en:{1}, title-tr:{2}, doi:{3}, abstract-en:{4}, abstract-tr:{5}, keywords-en:{6}, keywords-tr:{7}, authors:{8}\n\n'.format(dosya1, baslikskor, baslikskor2, doiskor, ozetskor, ozetskor2, anahtarskor, anahtarskor2, yazarskor))

for i in list:
	dosya1 = 'elas-u/{}-u.xml'.format(i)
	dosya2 = 'xmller/{}-dp.xml'.format(i)

	tree1 = ET.parse(dosya1)
	root1 = tree1.getroot()

	tree2 = ET.parse(dosya2)
	root2 = tree2.getroot()

	skor = ET.Element('skor')
        id = ET.SubElement(skor, 'id')
        title_en = ET.SubElement(skor, 'title-en')
        title_tr = ET.SubElement(skor, 'title-tr')
        doi = ET.SubElement(skor, 'doi')
        abstract_en = ET.SubElement(skor, 'abstract-en')
        abstract_tr = ET.SubElement(skor, 'abstract-tr')
        keywords_en = ET.SubElement(skor, 'keywords-en')
        keywords_tr = ET.SubElement(skor, 'keywords-tr')
        auth = ET.SubElement(skor, 'authors')

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

	liste1 = []
	liste3 = []
	for keywords in root1.findall('keywords'):
		if keywords.attrib == {"lang": "en"}:
			for keyword in keywords.findall('keyword'):
				ET.SubElement(keywords_en, 'keyword')
				anahtar = unicode(keyword.text) 
				liste1.append(anahtar)
			liste1 = sorted(liste1)
		elif keywords.attrib == {"lang": "tr"}:
			for keyword in keywords.findall('keyword'):
				ET.SubElement(keywords_tr, 'keyword')
				anahtar = unicode(keyword.text)
				liste3.append(anahtar)
			liste3 = sorted(liste3)

	liste2 = []
	liste4 = []
	for keywords in root2.findall('keywords'):
		if keywords.attrib == {"lang": "en"}:
			for keyword in keywords.findall('keyword'):
				anahtar = unicode(keyword.text)
				liste2.append(anahtar)
			liste2 = sorted(liste2)
		elif keywords.attrib == {"lang": "tr"}:
			for keyword in keywords.findall('keyword'):
				anahtar = unicode(keyword.text)
				liste4.append(anahtar)
			liste4 = sorted(liste4)

	liste5 = []
	for authors in root1.findall('authors'):
		for author in authors.findall('author'):
			ET.SubElement(auth, 'author')
			yazar = unicode(author.text)
			liste5.append(yazar)
		liste5 = sorted(liste5)

	liste6 = []
	for authors in root2.findall('authors'):
		for author in authors.findall('author'):
			yazar = unicode(author.text)
			liste6.append(yazar)
		liste6 = sorted(liste6)

	baslikskor = str(Levenshtein.ratio(baslik1, baslik2))
	baslikskor2 = str(Levenshtein.ratio(baslik3, baslik4))
	doiskor = str(Levenshtein.ratio(doi1, doi2))
	ozetskor = str(Levenshtein.ratio(ozet1, ozet2))
	ozetskor2 = str(Levenshtein.ratio(ozet3, ozet4))
	anahtarskor = str(Levenshtein.ratio(str(liste1), str(liste2)))
	anahtarskor2 = str(Levenshtein.ratio(str(liste3), str(liste4)))
	yazarskor = str(Levenshtein.ratio(str(liste5), str(liste6)))

	log()

	id.text = i
	title_en.text = baslikskor
	title_tr.text = baslikskor2
	doi.text = doiskor
	abstract_en.text = ozetskor
	abstract_tr.text = ozetskor2
	keywords_en.text = anahtarskor
	keywords_tr.text = anahtarskor2
	auth.text = yazarskor

	agac = ET.ElementTree(skor)
	agac.write('xmloutput/{}-skor.xml'.format(i))
