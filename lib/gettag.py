'''def get_urltag(url):
	return url.split(".")[1]
truncado = input("url: ")
print(get_urltag(truncado))'''
'''from urllib.parse import urlparse

def get_urltag(url):
	dominio = urlparse(url).netloc
	#print(dominio)
	return dominio.split(".")[1]
'''	
	
'''truncado = input("url: ")
print(get_urltag(truncado))
'''
import tldextract

def get_urltag(url):
	ext = tldextract.extract(url)
	return ext.domain
