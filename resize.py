import sys
import os.path
import struct
import random
import level

if len(sys.argv) < 4: print ( "usage (ratio in percent): resize.py origlev.lev output.lev xratio [yratio]" )
else:
    if len(sys.argv) < 5:
        yratio = int (50 + random.random() * 100) # a number between 50 and 150 
    try:
        xratio = int( sys.argv[3] )
    except ValueError:
        xratio = 100
    try:
        yratio = int( sys.argv[4] )
    except ValueError:
        yratio = 100
    except IndexError:
        pass
    if ( xratio == 100 and yratio == 100 ): # this may happen if user sets this, not only if user sends erroneous data
        xratio = int (50 + random.random() * 100) # a number between 50 and 150
        yratio = int (50 + random.random() * 100) # a number between 50 and 150

    lev = level.level()
    lev.filename = sys.argv[2]
    lev.polys = []
    lev.objs = []
    lev.name = "rsz " + sys.argv[2] + ", x%: " + str(xratio) + " y%: " + str(yratio)

    f = open( os.path.join('levels',sys.argv[1]), 'rb' )
    f.read(7)
    reclink = 'Reclink: ' + str(struct.unpack('i',f.read(4))[0])
    integrity1 = 'Integrity 1: ' + str(struct.unpack('d',f.read(8))[0])
    integrity2 = 'Integrity 2: ' + str(struct.unpack('d',f.read(8))[0])
    integrity3 = 'Integrity 3: ' + str(struct.unpack('d',f.read(8))[0])
    integrity4 = 'Integrity 4: ' + str(struct.unpack('d',f.read(8))[0])
    levname = 'Level name: "' + str(''.join(struct.unpack('51c',f.read(51)))) + '"'
    lgr = 'LGR: "' + str(''.join(struct.unpack('16c',f.read(16)))) + '"'
    ground = 'Ground: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"'
    sky = 'Sky: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"'

    polys = int(struct.unpack('d',f.read(8))[0])
    # print ( 'Polygons: ' + str(polys) )
    for p in range(polys):
        #print ( 'Polygon ' + str(p) + ':' )
        if struct.unpack('i',f.read(4))[0] == 1:
            grass = 1 # grass poly
        else:
            grass = 0
        vs = int(struct.unpack('i',f.read(4))[0])
        vcs = []
        for v in range(vs):
            vcs.append( struct.unpack('d',f.read(8))[0]*(xratio/100.0) )
            vcs.append( struct.unpack('d',f.read(8))[0]*(yratio/100.0) )
        if not grass: lev.polys.append( vcs )
            
    obs = int(struct.unpack('d',f.read(8))[0])
    # print ( 'Objects: ' + str(obs) )
    for o in range(obs):
        obj = []
        obj.append( struct.unpack('d',f.read(8))[0]*(xratio/100.0) ) #x
        obj.append( struct.unpack('d',f.read(8))[0]*(yratio/100.0) ) #y
        obj.append( struct.unpack('i',f.read(4))[0] ) #type
        obj.append( struct.unpack('i',f.read(4))[0] ) #gravity
        obj.append( struct.unpack('i',f.read(4))[0] ) #animation
        lev.objs.append( obj )
    lev.write()
    print lev.filename
    f.close()



