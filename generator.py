import sys
import random
import level

def r( max ):
    return random.random() * max

class generator( level.level ):
    def create_flat( self, args ):
        i = 0
        x0 = x = 24.0
        y0 = y = ymin = -8.0
        poly = [x0,y0]
        # generate floor
        if 'short' in args: steps = 10
        elif 'medium' in args: steps = 20
        elif 'long' in args: steps = 40
        else: steps = r(40) + 10
        while ( i < steps ):
            i += 1
            x -= r(4) + 1
            y += r(2) - 1
            if y < ymin: ymin = y
            poly.append(x)
            poly.append(y)
            if x0 - x > 150: break # too wide lev causes error
        # set flower/start to bottom left
        self.objs = []
        if 'right' in args: self.objs.append( [x+1, y-1, 4, 0, 0] ) # start
        else: self.objs.append( [x+1, y-1, 1, 0, 0] ) # flower
        print 'width: ' + str(x0-x)
        # generate top left corner
        x += r(2) - 1
        y = ymin -r(5) -5 # make sure ceiling is higher than hill
        poly.append(x)
        poly.append(y)
        # generate top right corner
        y += r(2) - 1
        x = x0 + r(5) - 2.5
        poly.append(x)
        poly.append(y)
        self.polys = []
        self.polys.append( poly )
        if 'right' in args: self.objs.append( [21.0, -10, 1, 0, 0] )
        else: self.objs.append( [21.0, -10, 4, 0, 0] ) # 4=start, 2=apples, 3=killers
        self.name = "genR flatula o,o " + self.filename
        print self.name

    def create_pipe( self, args ):
        i = 0
        x0 = x = 24.0
        y0 = y = ymin = -8.0
        poly = [x0,y0]
        # generate floor
        if 'short' in args: steps = 10
        elif 'medium' in args: steps = 20
        elif 'long' in args: steps = 40
        else: steps = r(20) + 10
        while ( i < steps ):
            i += 1
            x -= r(4) + 1
            y += r(2) - 1
            if y < ymin: ymin = y
            poly.append(x)
            poly.append(y)
            if x0 - x > 150: break # too wide lev causes error
        # set flower/start to bottom left
        self.objs = []
        if 'right' in args: self.objs.append( [x, y-1, 4, 0, 0] ) # start
        else: self.objs.append( [x, y-1, 1, 0, 0] ) # flower
        print 'width: ' + str(x0-x)
        # generate top left corner
        x += r(2) - 1
        y = ymin -r(5) -5 # make sure ceiling is higher than hill
        poly.append(x-3)
        poly.append(y)
        poly.append(x)
        poly.append(y)
        while ( i ):
            i -= 1
            x = poly[i*2]
            y = poly[i*2+1] - r(1.6) - 1.4 # pipe height
            self.objs.append( [poly[i*2], poly[i*2+1]-1, 2, 0, 0] ) # apples
            poly.append(x)
            poly.append(y)            
        # generate top right corner
        y = poly[1] - 14
        x = poly[0]
        poly.append(x)
        poly.append(y)
        poly.append(x+6)
        poly.append(y)
        # move start point (just a fix)
        poly[0] += 5
        self.polys = []
        self.polys.append( poly )
        if 'right' in args: self.objs.append( [x+3, y+13, 1, 0, 0] )
        else: self.objs.append( [x+3, y+13, 4, 0, 0] ) # 4=start, 2=apples, 3=killers
        self.name = "genR piPulA o,o " + self.filename
        print self.name

    def create_bang( self, args ):
        i = 0
        x0 = x = 24.0
        y0 = y = -8.0
        poly = [x0,y0]
        # generate floor
        if 'short' in args: steps = 10
        elif 'medium' in args: steps = 20
        elif 'long' in args: steps = 40
        else: steps = r(40) + 10
        while ( i < steps ):
            i += 1
            x -= r(4) + 2
            y += r(4) + 1
            poly.append(x)
            poly.append(y)
            if x0 - x > 140: break # too wide lev causes error
            if -y0 + y > 130: break # too high lev causes error
        # make tiny area for easily catching flower
        x -= r(5) + 3
        poly.append(x)
        poly.append(y)
        # set flower to bottom left
        self.objs = []
        if 'right' not in args: self.objs.append( [x+3, y-1, 1, 0, 0] ) # flower
        print 'width: ' + str(x0-x)
        print 'height: ' + str(-y0+y)
        # generate ceiling based on underlying verteces
        while (i):
            i -= 1
            x = poly[i*2] + r(1) - 0.5
            y = poly[i*2+1] - r(5) - 3
            if i < 2: y = poly[i*2+1] - 10
            poly.append(x)
            poly.append(y)
        # mirrorize level horizontally
        if 'right' in args:
            j = 0
            for v in poly:
                if j%2 == 1: poly[j] = -poly[j]
                j += 1
        self.polys = []
        self.polys.append( poly )
        if 'right' in args:
            self.objs.append( [poly[-4]+1, poly[-3]-1, 1, 0, 0] ) # 4=start, 2=apples, 3=killers
            self.objs.append( [poly[len(poly)/2]+.5, poly[len(poly)/2+1]-.5, 4, 0, 0] ) # flower
            poly[len(poly)/2-1] = poly[len(poly)/2+1] - 10 # make safe ceiling for start
            poly[len(poly)/2-2] = poly[len(poly)/2] # make safe ceiling for start
            # make outer square based on max points (because anti-clockwise polygons should be inside a polygon)
            poly2 = [poly[len(poly)/2-2]-1,poly[len(poly)/2-1]-1,poly[-2]+1,poly[len(poly)/2-1]-1,poly[-2]+1,poly[-1]+1,poly[len(poly)/2-2]-1,poly[-1]+1]
            self.polys.append(poly2) # add outer square
        else: self.objs.append( [22.0, -10, 4, 0, 0] )
        self.name = "genR bangulonia o,o " + self.filename
        print self.name


if __name__ == "__main__":
    lev = generator()
    # args can be short, medium or long; right (otherwise left direction)
    if 'genF' in sys.argv: lev.create_flat( sys.argv )
    elif 'genB' in sys.argv: lev.create_bang( sys.argv )
    elif 'genP' in sys.argv: lev.create_pipe( sys.argv )
    else: lev.create_bang( sys.argv )
    lev.write()
    
