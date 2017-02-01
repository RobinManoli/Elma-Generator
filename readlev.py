import sys
import os.path
import struct

if len(sys.argv) < 2: print ( "usage: read.py level.lev" )
else:
    f = open( os.path.join('levels',sys.argv[1]), 'rb' )
    f.read(7)
    print ( 'Reclink: ' + str(struct.unpack('i',f.read(4))[0]) )
    print ( 'Integrity 1: ' + str(struct.unpack('d',f.read(8))[0]) )
    print ( 'Integrity 2: ' + str(struct.unpack('d',f.read(8))[0]) )
    print ( 'Integrity 3: ' + str(struct.unpack('d',f.read(8))[0]) )
    print ( 'Integrity 4: ' + str(struct.unpack('d',f.read(8))[0]) )
    print ( 'Level name: "' + str(''.join(struct.unpack('51c',f.read(51)))) + '"' )
    print ( 'LGR: "' + str(''.join(struct.unpack('16c',f.read(16)))) + '"' )
    print ( 'Ground: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"' )
    print ( 'Sky: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"' )

    polys = int(struct.unpack('d',f.read(8))[0])
    print ( 'Polygons: ' + str(polys) )
    for p in range(polys):
        print ( 'Polygon ' + str(p) + ':' )
        if struct.unpack('i',f.read(4))[0] == 1:
            print ( ' Grass: Yes' )
        else:
            print ( ' Grass: No' )
        vs = int(struct.unpack('i',f.read(4))[0])
        vstr = ( ' Verteces: ' + str(vs) + ' (' )
        for v in range(vs):
            vstr += str(struct.unpack('d',f.read(8))[0]) + ', '
            vstr += str(struct.unpack('d',f.read(8))[0]) + ', '
        vstr = vstr[:-2] + ')'
        print vstr
            
    obs = int(struct.unpack('d',f.read(8))[0])
    print ( 'Objects: ' + str(obs) )
    for o in range(obs):
        ostr = ' Object ' + str(o) + ': '
        ostr += 'x=' + str(struct.unpack('d',f.read(8))[0]) + ' '
        ostr += 'y=' + str(struct.unpack('d',f.read(8))[0]) + ' '
        otype = struct.unpack('i',f.read(4))[0]
        if otype == 1: ostr += 'flower(1) '
        elif otype == 2: ostr += 'apple(2) '
        elif otype == 3: ostr += 'killer(3) '
        elif otype == 4: ostr += 'start(4) '
        else: ostr += 'errortype(' + str(otype) + ') '
        ostr += 'gravity='
        ograv = struct.unpack('i',f.read(4))[0]
        if ograv == 0: ostr += 'normal(0) '
        elif ograv == 1: ostr += 'up(1) '
        elif ograv == 2: ostr += 'down(2) '
        elif ograv == 3: ostr += 'left(3) '
        elif ograv == 4: ostr += 'right(4) '
        else: ostr += 'errorvalue(' + str(ograv) + ') '
        ostr += ( 'animation#=' + str(struct.unpack('i',f.read(4))[0]) )
        print ( ostr )

    f.close()



