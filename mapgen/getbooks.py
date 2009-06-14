import urllib
from pyaws import ecs
ecs.setLicenseKey('1263N1HAP1PCKYCB9682')
# books = ecs.ItemSearch('python', SearchIndex='Books')
books = ecs.ItemSearch('lisp', SearchIndex='Books', ResponseGroup='Images')
books_with_large_images = []
print len(books)
for i in range(40):
    if hasattr(books[i], 'LargeImage'):
        # print books[i].LargeImage.Width,books[i].MediumImage.Height
        books_with_large_images.append(books[i])
 
print len(books_with_large_images)
 
for i,each_book in enumerate(books_with_large_images):
    urllib.urlretrieve(each_book.LargeImage.URL, r'/home/badri/git/smooth-scroll/res/books/'+ str(i+80) +'.jpg')
