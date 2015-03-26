import json

class Tileset:
    def __self__(self, path, w, h, tileh, tilew, margin, spacing):
        self.path = path
        self.w = w
        self.h = h

gindex = {}       
def index_gid(tileset, gindex, gid):
    for i in range(0, tileset.h/(tileset.tileh + tileset.spacing)):
        for j in range(0, tileset.w/(tileset.tilew + tileset.spacing)):
            x = j * (tileset.tilew + tileset.spacing) + tileset.margin
            y = i * (tileset.tileh + tileset.spacing) + tileset.margin 
            gindex[gid] = [x, y, tileset]
            gid += 1



json_data = open('map-sm.json')
data = json.load(json_data)
height = data['height']
width = data['width']
tilewidth = data['tilewidth']

print height
print width
print tilewidth

tilesets = data['tilesets']
for t in tilesets:
    tileset = Tileset(t['image'], t[''])


#for i in data:
#    print i, '->',data[i]
#print data
json_data.close()
