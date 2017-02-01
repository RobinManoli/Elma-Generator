import sys
import os.path
import struct
import random

# a class for writing elasto mania levels -- doesn't support pictures
class level:
    def __init__( self ):
        self.polys = []
        self.polys.append( [-24.0, -8.0, 24.0, -8.0, 24.0, 2.0, -24.0, 2.0] ) # std lev
        self.objs = []
        self.objs.append( [-2.0, -0.85, 1, 0, 0] ) # flower
        self.objs.append( [2.0, -0.85, 4, 0, 0] ) # 4=start, 2=apples, 3=killers
        self.name = "generated by fourth dimension";
        if len(sys.argv) > 1: self.filename = sys.argv[1]
        else: self.filename = 'gen.lev'

    def write( self ):
        # checksum
        PSUM = 0
        for i in range( len(self.polys) ):
            for j in range( int(len(self.polys[i])/2) ):
                PSUM += self.polys[i][j*2] + self.polys[i][j*2+1];
        OSUM = 0
        for i in range( len(self.objs) ):
            OSUM += self.objs[i][0] + self.objs[i][1] + self.objs[i][2]
        PICSUM = 0

        sum1 = (PSUM + OSUM + PICSUM) * 3247.764325643;
        sum2 = 3261 + 11877 - sum1;
        sum3 = 83 + 11877 - sum1; # there is an if unknown possibility that changes this value
        sum4 = 40 + 12112 - sum1;

        # write lev
        self.path = os.path.join('levels',self.filename)
        f = open( self.path, 'wb' )
        f.write(b'POT14') # elma level id

        reclink = struct.pack( 'i', int(1633737894 * random.random()) ) # a random number for linking recs with this level
        f.write( reclink[:2] + reclink )

        # properties such as level is locked, etc
        #levproperties = struct.pack( '8i', -2142987195, -1059911771, -1071493598, 1088481298, -2142987195, 1088337317, -2142987195, 1088349605 )
        #f.write( levproperties )
        checksum = struct.pack( '4d', sum1, sum2, sum3, sum4 )
        f.write( checksum )

        while len(self.name) < 51: self.name += '\x00';
        self.name = self.name[:51] # make sure lev name is not too long
        f.write( str.encode(self.name) ) # lev name
        f.write(b'DEFAULT\x00\x00\x00\x00\x00\x00\x00\x00\x00') # lgr
        f.write(b'ground\x00\x00\x00\x00') # ground texture
        f.write(b'sky\x00\x00\x00\x00\x00\x00\x00') # sky texture

        npolys = struct.pack( 'd', len(self.polys) + 0.4643643 ) # number of polygons + .4643643
        f.write( npolys )
        for p in self.polys:
            # 0 normal|1 grass, nverteces
            f.write( struct.pack('ii',0,int(len(p)/2)) )
            for v in p: f.write( struct.pack('d',v) ) # vertex x|y as double

        nobjs = struct.pack( 'd', len(self.objs) + 0.4643643 ) # number of objects + .4643643
        f.write( nobjs )
        for o in self.objs: f.write( struct.pack('ddiii', o[0], o[1], o[2], o[3], o[4]) )
        print( str(len(self.objs)) + ' objects')
        print( str(len(self.polys)) + ' polygons')

        # END STUFF
        npics = struct.pack( 'd', 0.2345672 ) # number of pictures + .2345672
        f.write( npics )
        f.write(b'\x3A\x10\x67\x00') # end of data
        #top10
        tt = struct.pack( '86i', -1217788651, -1000739447, 1938816840, -1066353546, 800348127, -1140351475, -1972434845, 950872073, -1594264608, -1979711360, 1617522487, 1098320151, 874941612, -1733885268, -2130795063, -1265123105, -904014000, 1207648580, 945871095, -2108896380, -1852169167, 1796131190, -855870004, -1737185800, 1757086350, -1119040700, -197868391, 1749842571, 1889162072, -869576755, -2132796719, 879988526, 1188302567, -1711096547, -2077805633, -1542367226, 1964893200, 796438570, -276429082, -50735708, 1951674001, -1315833763, -111828234, -1907885277, -403421937, -1942399907, 948907729, 1757122495, -925681504, 999377289, -2013068611, -1669387035, 1465881525, 1273274784, 1811766289, -54119292, 152547729, -1516881007, -1119905676, -1985577634, 1390421892, -1566202012, 1934573712, -1878747084, -1514615521, -997702783, 432851416, 1704402477, 1479932998, 757782322, -1743369475, -1652237695, -1332978919, -1101720187, -1795250888, -622605419, 73998934, 1174900145, 883322003, -120564643, -518025084, -311970109, -161441736, 39569504, -1480450977, -813784227 )
        f.write( tt )
        tt = struct.pack( '86i', 2132518692, -1488789893, -1414531373, 56927180, -1105910996, 1162821806, 2114277620, -36964375, 1385168780, 491997179, -1413712333, -524795713, 218165015, 325467714, -1896459274, 1354020124, -1205945654, 1292894747, -326858266, -586944031, -1078419733, -805424471, 750985600, -1068620161, -475174840, 297462805, 1960070728, 681190513, -1732987475, -749331964, -795558174, 1471216402, 1454095461, 1004668535, 1161753947, -1343941375, 560923753, 886387172, 604975276, 1017579221, 716528785, -2073309592, -933218751, -54938605, -1281399893, -658237125, -1558338543, -863389944, 40683, -987837453, 679245799, -1991737184, -1999365303, -838445628, -1879070042, -1858589253, -1952203855, -322652327, -1595389392, -1176274212, -1024640864, 674807509, -814901226, 1259558259, -1443751604, 1122737412, 1272390029, -610597077, -2106699741, 872732885, -315048427, 1404440757, 844690809, -689364856, -1746998632, -1553295830, 804785245, 1449897157, -766412346, -312007383, 949813081, -880498733, -982562812, 918656802, -1782377297, 1290363096 )
        f.write( tt )
        f.write(b'\x52\x5D\x84\x00') # end of file
        f.close()


if __name__ == "__main__":
    lev = level()
    lev.write()
    print ( "polys: " + str(len(lev.polys)) )