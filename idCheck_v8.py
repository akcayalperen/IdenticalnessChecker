import xml.etree.ElementTree as ET
import Levenshtein
import os

minratio = 0.07
hatakodlari = ['20', '21','22', '23', '24', '25', '26']
diller = ['tr', 'en']
caprazsinir = 0.5
birlesiksinir = 0.7
sonucsinir = 0.8

def hatayacevir(root):
	for child in root:
        	for hata in hatakodlari:
                	 for isim, kod in child.attrib.iteritems():
				if isim == 'score' and kod == hata:
					child.set('info', hata)
					del child.attrib["score"]
        return

def skoryaz(skor1, skor2, root, tag = str):
	for j in root.findall(tag):
		if j.attrib == {"lang": "en"}:
			j.set('score', skor1)
		elif j.attrib == {"lang": "tr"}:
			j.set('score', skor2)

def karsilastir(a, b):
	if a == u'None' and b == u'None': return '24'
	elif a == u'None': return '22'
	elif b == u'None': return '21'
	elif Levenshtein.ratio(a,b) < minratio:
		if len(a) > len(b): return '25'
		elif len(b) > len(a): return '26'
		else: return '23'
	else: return str(Levenshtein.ratio(a,b))

def caprazskor(root, root2):
    for child in root:
        for isim, puan in child.attrib.items():
            if isim == 'score' and float(puan) < caprazsinir or isim == 'info' and puan == '21':
               	for ad, tur in child.attrib.items():
			for dil in diller:
                       		if ad == 'lang' and tur == dil:
                       			for child2 in root2:
                           			for ad2, tur2 in child2.attrib.iteritems():
                               				if ad2 == 'lang' and not tur2 == dil:
                                   				skor = Levenshtein.ratio(unicode(child.text), unicode(child2.text))
                                        			skor_str = str(skor)
								if skor > sonucsinir:
									child.set('score', skor_str)
									child.set('cross-lang', tur2)
											
def birlesikskor(root, root2, liste, liste2):
	for child in root:
		for isim, puan in child.attrib.items():
			if isim == 'score' and float(puan) < birlesiksinir or isim == 'info' and puan == '21' and 'cross-lang' not in child.attrib.items():
				for ad, tur in child.attrib.items():
					for dil in diller:
						if ad == 'lang' and tur == dil:
							for child2 in root2:
								if child.tag == 'abstract':
									for ad2, tur2 in child2.attrib.iteritems():
										if ad2 == 'lang' and tur2 == dil:
											birskor = []
											maxskor = 0
											for i in liste:
												birskor.append(Levenshtein.ratio(i, unicode(child2.text)))
												if not max(birskor) == maxskor:
													maxskor = max(birskor)
													merge_type = str(liste.index(i) + 1)
											skor_str = str(maxskor)
											if maxskor > sonucsinir:
												child.set('merged-score', skor_str)
												child.set('merged-text', 'True')
												child.set('merge-type', merge_type)
								elif child.tag == 'title':
									for ad3, tur3 in child2.attrib.iteritems():
										if ad3 == 'lang' and tur3 == dil:
											basskor = []
											maxskor = 0
											for i in liste2:
												basskor.append(Levenshtein.ratio(i, unicode(child2.text)))
												if not max(basskor) == maxskor:
													maxskor = max(basskor)
													merge_type = str(liste2.index(i) + 5)
											skor_str = str(maxskor)
											if maxskor > sonucsinir:
												child.set('merged-score', skor_str)
												child.set('merged-text', 'True')
												child.set('merge-type', merge_type)
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
			
		birlist = []
		baslist = []
		baslist.append(baslik1 + ' ' + baslik3)
		baslist.append(baslik3 + ' ' + baslik1)
		birlist.append(ozet1 + ' ' + ozet3)
		birlist.append(ozet3 + ' ' + ozet1)
		birlist.append(ozet1 + ' ' + baslik3 + ' ' + ozet3)
		birlist.append(ozet3 + ' ' + baslik1 + ' ' + ozet1)

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
				yeniliste = []
				for keys in kok[1].findall('keywords'):
					if keys.attrib == {"lang": "en"}:
						r = False
						if liste1 == ['21']: liste1 = []
						for key in keys.findall('keyword'):
                                                        if key.text.startswith("Key words:  "): key.text = key.text[12:]
							r = True
							anahtar2 = unicode(key.text)
							liste1.append(str(Levenshtein.ratio(anahtar, anahtar2)))
						if r == False:
							for dil in diller:
								if not dil == 'en':
									for anaht in kok[1].findall('keywords'):
										if anaht.attrib == {'lang': dil}:
											for deger in anaht.findall('keyword'):
												anahtar3 = unicode(deger.text)
												yeniliste.append(str(Levenshtein.ratio(anahtar, anahtar3)))
											if not yeniliste == []:
												keyword.set('score', max(yeniliste))
												keyword.set('cross-lang', dil)
				if not liste1 == []:
					keyword.set('score', max(liste1))
				else:
					keyword.set('info', '21')
			if p == False: keywords.set('info', '22')
		elif keywords.attrib == {"lang": "tr"}:
			q = False
			for keyword in keywords.findall('keyword'):
				q = True
				anahtar = unicode(keyword.text)
				liste2 = ['21']
				yeniliste = []
				for keys in kok[1].findall('keywords'):
					if keys.attrib == {"lang": "tr"}:
						r = False
						if liste2 == ['21']: liste2 = []
						for key in keys.findall('keyword'):
                                                        if key.text.startswith("Key words:  "): key.text = key.text[12:]
							r = True
							anahtar2 = unicode(key.text)
							liste2.append(str(Levenshtein.ratio(anahtar, anahtar2)))
						if r == False:
							for dil in diller:
								if not dil == 'tr':
									for anaht in kok[1].findall('keywords'):
										if anaht.attrib == {'lang': dil}:
											for deger in anaht.findall('keyword'):
												anahtar3 = unicode(deger.text)
												yeniliste.append(str(Levenshtein.ratio(anahtar, anahtar3)))
											if not yeniliste == []:
												keyword.set('score', max(yeniliste))
												keyword.set('cross-lang', dil)
				if not liste2 == []:
					keyword.set('score', max(liste2))
				else:
					keyword.set('info', '21')
			if q == False: keywords.set('info', '22')

	for authors in kok[0].findall('authors'):
		o = False
		k = 0
		for author in authors.findall('author'):
			o = True
			yazar = unicode(author.text)
			liste3 = ['20']
			for aauthors in kok[1].findall('authors'):
				l = 0
				for aauthor in aauthors.findall('author'):
					if liste3 == ['20']: liste3 = []
					yazar2 = unicode(aauthor.text)
					liste3.append(str(Levenshtein.ratio(yazar, yazar2)))
					l += 1
			author.set('score', max(liste3))
			k += 1
		if o == False:
			authors.set('info', '22')
		if k < l: authors.set('info', '22')

	baslikskor = karsilastir(baslik1, baslik2)
	baslikskor2 = karsilastir(baslik3, baslik4)
	doiskor = karsilastir(doi1, doi2)
	ozetskor = karsilastir(ozet1, ozet2)
	ozetskor2 = karsilastir(ozet3, ozet4)

	for j in kok[0].findall('doi'):
		j.set('score', doiskor)

	skoryaz(baslikskor, baslikskor2, kok[0], 'title')
	skoryaz(ozetskor, ozetskor2, kok[0], 'abstract')

	hatayacevir(kok[0])

	caprazskor(kok[0],kok[1])

	birlesikskor(kok[0],kok[1],birlist,baslist)
	
	agac = ET.ElementTree(kok[0])
	agac.write('xmloutput/{}-skor.xml'.format(i))
