import Image

res_dir = '/opt/git-repos/smooth-scroll/res/'

big_tile = Image.open(res_dir + 'tile.jpg')
tile = big_tile.resize((529, 529))

nr_of_books_per_shelf = 5
nr_of_shelves = 2
gap_between_shelves = 100
x_offset = 300
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
for j in range(len(y)-1):
    shelf.paste(mask_left, (x_offset/2,y[j]))
    x = range(40 + x_offset/2, shelf_width + 1, 300)
    for i in range(len(x) - 1):
        shelf.paste(bkgnd, (x[i],y[j]))
        book = Image.open(res_dir + 'books/' + str(random.randint(1,4))+ '.jpg')
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
shelf.save(res_dir + 'final.jpg', "JPEG")
# map_tiles
map_tile_x = range(0, shelf.size[0], 100)
map_tile_y = range(0, shelf.size[1], 100)
[shelf.crop((x,y,x+100,y+100)).save(res_dir + 'map-tiles/x'+str(x/100)+'y'+str(y/100)+'z'+ str(0) +'.jpg', "JPEG") for x in map_tile_x for y in map_tile_y]
