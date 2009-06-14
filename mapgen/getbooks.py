import urllib
from pyaws import ecs
import os
license_key = '1263N1HAP1PCKYCB9682'
resource_dir = r'/home/badri/git/smooth-scroll/res/books/'

def get_books(query, license=license_key, base_dir=resource_dir, useful_till=40):
	ecs.setLicenseKey(license)
	books = ecs.ItemSearch(query, SearchIndex='Books', ResponseGroup='Images')
	books_with_large_images = []
	#print len(books)
	for i in range(useful_till):
	    if hasattr(books[i], 'LargeImage'):
		# print books[i].LargeImage.Width,books[i].MediumImage.Height
		books_with_large_images.append(books[i])

	#print len(books_with_large_images)

	for i,each_book in enumerate(books_with_large_images):
            os.chdir(base_dir)
            if not os.path.exists(query):
                os.mkdir(query)
	    urllib.urlretrieve(each_book.LargeImage.URL, base_dir + os.path.sep + query + os.path.sep + str(i) +'.jpg')
        return len(books_with_large_images)

