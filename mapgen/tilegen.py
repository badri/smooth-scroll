import Image
import random
import os
from getbooks import license_key, resource_dir, get_books
import operator

res_dir = '/opt/git-repos/smooth-scroll/res/'

big_tile = Image.open(res_dir + 'tile.jpg')
nr_of_books_per_shelf = 5
nr_of_shelves = 8
gap_between_shelves = 100
x_offset = 300

def generate_meta_shelf(shelf_title,where_to_put=res_dir, background_tile=big_tile, nr_of_books_per_shelf=5, nr_of_shelves=8, gap_between_shelves=100, x_offset=300):
        'generate a single shelf for a given query'
        tile = big_tile.resize((529, 529))
	shelf_width = 40 + nr_of_books_per_shelf*300 + 40 + x_offset
	shelf_height = 240 * nr_of_shelves + (gap_between_shelves * (nr_of_shelves + 1))
	round_off_to_hundred = lambda x:(x/100+1)*100
	shelf_height = round_off_to_hundred(shelf_height)
	shelf_width = round_off_to_hundred(shelf_width)

	shelf = Image.new('RGB', (shelf_width, shelf_height))

	tile_x = range(0, shelf_width, 529)
	tile_y = range(0, shelf_height, 529)

	[shelf.paste(tile, (x,y)) for x in tile_x for y in tile_y]

	mask_right = Image.open(res_dir + 'mask_right.png')
	mask_left = Image.open(res_dir + 'mask_left.png')
	bkgnd = Image.open(res_dir + 'background.jpg')

	y = range(gap_between_shelves, shelf_height + 1, 240+gap_between_shelves)
        print y
	for j in range(len(y)-1):
	    shelf.paste(mask_left, (x_offset/2,y[j]))
	    x = range(40 + x_offset/2, shelf_width + 1, 300)
            print x
	    for i in range(len(x) - 1):
		shelf.paste(bkgnd, (x[i],y[j]))
                print x[i], y[j]
		book_file = res_dir + os.path.sep + 'books' + os.path.sep + shelf_title + os.path.sep +  str(nr_of_books_per_shelf*(j) + i)+ '.jpg'
		if os.path.exists(book_file):
                    print book_file
		    book = Image.open(book_file)
		    if book.size[1] > 400:
		        book = book.resize((book.size[0]/2, book.size[1]/2), Image.ANTIALIAS)
		        if book.size[1] > 200:
		            book = book.resize((book.size[0]/2, book.size[1]/2), Image.ANTIALIAS)
		    if book.size[1] > 300:
		        diff = book.size[1] - 300
		        shelf.paste(book, (x[i] + 10,y[j]-diff-80))
		    else:
		        diff = 300 - book.size[1]
		        shelf.paste(book, (x[i] + 10, y[j]+diff-80))
	    shelf.paste(mask_right, (x[i+1],y[j]))
        return shelf

def generate_empty_shelf():
    'generate an empty shelf with no books, used for aligning the library'
    return generate_meta_shelf(shelf_title='')


def generate_library(shelves):
        'generate a library from given list of shelves'
	if len(shelves)%2:
	    shelves.append(generate_meta_shelf(shelf_title=''))
	meta_x = reduce(operator.add, [x.size[0] for x in shelves])
	meta_y = reduce(operator.add, [x.size[1] for x in shelves])
	meta_shelf = Image.new('RGB', (meta_x/2, meta_y/len(shelves)*2))
	for i,each_shelf in enumerate(shelves):
	    if i%2:
		meta_shelf.paste(each_shelf, (shelves[0].size[0]*((i+1)/2-1), shelves[0].size[1]))
	    else:
		meta_shelf.paste(each_shelf, (shelves[0].size[0]*i/2, 0))
	return meta_shelf



# map_tiles
def split_tiles(meta_shelf, tilex=100, tiley=100, zoom=0):
    'split the library into 100x100 tiles'
    map_tile_x = range(0, meta_shelf.size[0], tilex)
    map_tile_y = range(0, meta_shelf.size[1], tiley)
    [meta_shelf.crop((x,y,x+100,y+100)).save(res_dir + os.path.sep + 'map-tiles/x'+str(x/tilex)+'y'+str(y/tiley)+'z'+ str(zoom) +'.jpg', "JPEG") for x in map_tile_x for y in map_tile_y]



queries = ['java', 'perl', 'python', 'lisp', 'sql']

shelves = []
for query in queries:
    #get_books(query)
    shelves.append(generate_meta_shelf(shelf_title=query))
    pass

split_tiles(generate_library(shelves))
os.chdir(r'/home/badri/git/smooth-scroll/res')

# meta_shelf.save('final.jpg', "JPEG")

