#given a url get the html text back
#reference: http://docs.python-requests.org/en/master/api
#reference: 
import requests
from bs4 import BeautifulSoup
import bs4
import json

class ParseUrl(object):
	timeout = None
	allow_redirects = True
	stream = True
	metadata = {}


	def __init__(self, timeout=None, allow_redirects=True, stream=True):
		self.timeout = timeout
		self.allow_redirects = allow_redirects
		self.stream = stream
		self.metadata = {}

	def get_html_from_url(self, url):
		if not isinstance(url, str):
			raise ValueError("Expecting a url string.")

		if not url:
			raise ValueError("url is empty string.")

		try:
			r = requests.get(url, allow_redirects=self.allow_redirects, stream=self.stream, timeout = self.timeout)

			if r.status_code != 200:
				raise Exception("Cannot fetch any data from url {}".format(url))

			return r.text
		except Exception as ex:
			raise Exception("Encountered an error while fetching information for the url: {}. Error: {}".format(url, ex))

	def get_metadata_from_html_content(self, html):
		if not isinstance(html, str):
			raise ValueError("Expecting html text.")

		if not html:
			raise ValueError("html text is empty.")

		soup = BeautifulSoup(html, "html.parser")

		return soup.html.head.findAll(name="meta")

	def get_meta_tags(self, meta_data):
		if not isinstance(meta_data, bs4.element.ResultSet):
			raise ValueError("Expecting soup resultset object.")

		if not meta_data:
			raise ValueError("Soup resultset object should not be null.")
				
		for m in meta_data:
			k = None
			v = None
			attrs = m.attrs
			if 'name' in attrs:
				k = 'name'
			elif 'property' in attrs:
				k = 'property'
			elif 'http-equiv' in attrs:
				k = 'http-equiv'
			if k:
				k = attrs[k].strip()
				if 'content' in attrs:
					v = attrs['content'].strip()
				if (len(k) > 3) and (k[:3] == 'dc:'):
					self.metadata['dc'][k[3:]] = v
				else:
					if('meta' not in self.metadata.keys()):
						self.metadata['meta'] = {k : ''}
					self.metadata['meta'][k] = v
		return self.metadata
 
if __name__ == "__main__":
	p = ParseUrl()
	html = p.get_html_from_url("https://stackoverflow.com/questions/38662791/monitor-access-to-a-symlink-with-pyinotify")
	meta_data = p.get_metadata_from_html_content(html)
	meta_data_tags = p.get_meta_tags(meta_data)
	meta_attrs_txt = "meta_attrs.txt"
	with open(meta_attrs_txt, 'w+') as file_handler:
		file_handler.writelines("{}\n".format(data.attrs) for data in meta_data)
	meta_tags_txt = "meta_tags.txt"
	with open(meta_tags_txt, 'w+') as file_handler:
		file_handler.writelines("{}\n".format(json.dumps(meta_data_tags, indent=4, sort_keys=True)))