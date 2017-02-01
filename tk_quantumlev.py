import sys
import os
import level
import struct
import random

if sys.version_info < (3, 0):
    from Tkinter import *
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
else:
    from tkinter import *
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox

def r( max ):
    #return max # for testing without random values
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
        print ( 'width: ' + str(x0-x) )
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
        self.name = "genR flatula o,o "
        print ( self.name )

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
        print ( 'width: ' + str(x0-x) )
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
        self.name = "genR piPulA o,o "
        print ( self.name )

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
        print ( 'width: ' + str(x0-x) )
        print ( 'height: ' + str(-y0+y) )
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
        self.name = "genR bangulonia o,o "
        print ( self.name )

    def create_flagtag( self, args ):
        if 'short' in args: size = 1.5
        elif 'medium' in args: size = 2
        elif 'long' in args: size = 3
        else: size = 2

        # start vertex in center right
        xmax = xmin = x = 24.0 # not exactly true
        ymax = ymin = righty = y = 0.0
        vx = -1
        vy = -size*4
        poly = [x,y]
        # create surrounding circle-like poly
        # create circle anti-clockwise
        # first go from 3 o'clock to 12 o'clock
        while ( vy < 0 ):
            vx -= size + r(1) * 0.01 - r(1) * 0.01
            vy += size + r(1) * 0.01 - r(1) * 0.01
            x = x + vx
            y = y + vy
            poly.append(x)
            poly.append(y)
            if y < ymin:
                ymin = y
                topx = x
            print ( "x: %.2f, y:%.2f" %(x,y) )
        while ( vx < 0 ):
            vx += size + r(1) * 0.01 - r(1) * 0.01
            vy += size + r(1) * 0.01 - r(1) * 0.01
            x = x + vx
            y = y + vy
            poly.append(x)
            poly.append(y)
            if x < xmin:
                xmin = x
                lefty = y
            if y < ymin:
                ymin = y
                topx = x
            print ( "x: %.2f, y:%.2f" %(x,y) )

        # upper half is done, now make a non-symmetric mirror (as otherwise the result is more the start of a spiral than a circle)
        # enumerate half the list, as two values are taken each time, and skip the last vertex pair
        # () vertex duplicates causes (by elma unexplained) internal error, and they are not needed
        for i, v in enumerate( poly[0:int(len(poly)/2)-2] ):
            x = x + poly[i*2] - poly[i*2+2] # subtract first line's x value from last x
            y = y + poly[i*2+1] - poly[i*2+3] # subtract first line's y value from last y
            poly.append(x)
            poly.append(y)
            if x > xmax:
                xmax = x
                righty = y
            if y > ymax:
                ymax = y
                bottomx = x
            print ( "x: %.2f, y:%.2f" %(x,y) )

        # set flower to bottom left
        self.objs = []
        width = xmax - xmin
        height = ymax - ymin
        centerx = xmax - width/2
        centery = ymax - height/2
        print ( 'width: ' + str(xmax-xmin), xmax, xmin )
        print ( 'height: ' + str(ymax-ymin), ymax, ymin )
        # reverse the order of verteces
        corrected_poly = []
        for i, v in enumerate( poly[:int(len(poly)/2)] ):
            # first insert y-value
            corrected_poly.insert( 0, poly[i*2+1] )
            corrected_poly.insert( 0, poly[i*2] )
        self.polys = []
        # somehow, there's always internal error here
        self.polys.append( corrected_poly )
        # add outer poly
        #self.polys.append([ xmax+5, ymin-5, xmin-5, ymin-5, xmin-5, ymax+5, xmax+5, ymax+5 ])
        flower = 1
        start = 4
        apple = 2
        gravity_normal = 0
        gravity_left = 3
        gravity_right = 4
        gravity_down = 2
        gravity_up = 1

        self.objs = []
        self.objs.append( [centerx, centery, flower, 0, 0] )
        self.objs.append( [bottomx-2, ymax-2, start, 0, 0] )
        # index will not likely fail, as every x-extreme is followed by a y-value, and every y-extreme is preceded by a x-value
        # unless perhaps if a y-extreme equals an x-extreme; though doesn't raise error in 1000 runs

        # ie fiskmas
        def mas( x, y, angle=None ):
            p = [x,y]
            # if no angle is requested, make it random
            if not angle:
                angle = ['up','down','left','right'][ int(r(2)) ]#[ int(r(4)) ] #r(2) wil generate only gravity up/down, 4 will generate all types
            if angle == 'up':
                # add one vertex to the right and down of x,y
                p += [x+r(2)+2, y+r(1)*.5+.5]
                # add an apple almost there too, easy catch, easy skip
                self.objs.append( [p[-2]+.5, p[-1]+.5, apple, gravity_up, 0] )
                # next, add next clockwise vertex, above x,y
                p += [x, y-r(1)-.5]
                # next, add next clockwise vertex, to the left
                p += [x-r(2)-2, y+r(1)*.5+.5]
            elif angle == 'down':
                # add one vertex to the left and up of x,y
                p += [x-r(2)-2, y-r(1)*.5-.5]
                # add an apple almost there too, easy catch, easy skip
                self.objs.append( [p[-2]+.5, p[-1]-.5, apple, gravity_down, 0] )
                # add next anti-clockwise vertex, below x,y
                p += [x, y+r(1)+.5]
                # add next anti-clockwise vertex, to the right
                p += [x+r(2)+2, y-r(1)*.5-.5]
            elif angle == 'left':
                # add one vertex to the right and up of x,y
                p += [x+r(1)*.5+.5, y-r(2)-2]
                # add an apple almost there too, easy catch, easy skip
                self.objs.append( [p[-2]+1, p[-1]-.5, apple, gravity_left, 0] )
                # add next anti-clockwise vertex, to the left of x,y
                p += [x-r(1)-.5, y]
                # add next anti-clockwise vertex, below and right
                p += [x+r(1)*.5+.5, y+r(2)+2]
            elif angle == 'right':
                # add next anti-clockwise vertex, below and left
                p += [x-r(1)*.5-.5, y+r(2)+2]
                # add an apple almost there too, easy catch, easy skip
                self.objs.append( [p[-2]-1, p[-1]-.5, apple, gravity_right, 0] )
                # add next anti-clockwise vertex, to the right of x,y
                p += [x+r(1)+.5, y]
                # add one vertex to the left and up of x,y
                p += [x-r(1)*.5-0.5, y-r(2)-2]
            return p


        # create apples at all extreme points
        #self.objs.append( [xmax, righty, apple, gravity_left, 0] )
        #self.objs.append( [xmin, lefty, apple, gravity_right, 0] )
        self.objs.append( [topx, ymin, apple, gravity_down, 0] )
        self.objs.append( [bottomx, ymax, apple, gravity_up, 0] )

        # create fiskmasar near extreme points
        mas_spacing = 8
        self.polys.append( mas(topx,ymin+mas_spacing,'down') )
        self.polys.append( mas(bottomx,ymax-mas_spacing,'up') )
        #self.polys.append( mas(xmax-mas_spacing,righty,'left') )
        #self.polys.append( mas(xmin+mas_spacing,lefty,'right') )

        width_left = width-mas_spacing*2
        height_left = height-mas_spacing*2

        for i in range( int(width_left/mas_spacing) ):
            for j in range( int(height_left/mas_spacing) ):
                self.polys.append( mas(xmin+mas_spacing*i+mas_spacing*2,ymin+mas_spacing*j+mas_spacing*2) )
        

        #print ( "width left, height left: ", width-mas_spacing*2, height-mas_spacing*2 )
        """
        mas_layers = 1
        # create layers of fiskmasar leaving the center free
        while width_left/2 > mas_spacing * 2:
            mas_layers += 1
            for i in range( mas_layers ):
                # find out spacing between this layer's fiskmasar
                width_segment = width/mas_layers/2
                # set y to the layer's first fiskmas position
                y = width_segment*(mas_layers-1)/mas_layers
                # populate map with fiskmasar, in random directions, based on level width
                self.polys.append( mas(xmax-mas_spacing*mas_layers,righty+width_segment*i-y) ) # relative to extreme right point
                self.polys.append( mas(xmin+mas_spacing*mas_layers,lefty+width_segment*i-y) ) # relative to extreme left point
            width_left -= mas_spacing * 2
        mas_layers = 1
        # create layers of fiskmasar leaving the center free
        while height_left/2 > mas_spacing * 2:
            mas_layers += 1
            for i in range( mas_layers ):
                # find out spacing between this layer's fiskmasar
                height_segment = height/mas_layers/2
                # set y to the layer's first fiskmas position
                x = height_segment*(mas_layers-1)/mas_layers
                # populate map with fiskmasar, in random directions, based on level width
                self.polys.append( mas(topx+height_segment*i-x, ymax-mas_spacing*mas_layers) ) # relative to extreme right point
                self.polys.append( mas(bottomx+height_segment*i-x, ymin+mas_spacing*mas_layers) ) # relative to extreme left point
            height_left -= mas_spacing * 2"""


        self.name = "genR flat goat o,o "
        print ( self.name )

class quantumlevTk( Frame ):
    def generate( self ):
        out = filedialog.asksaveasfilename()
        if not out: return
        if not out.endswith(".lev"): out += ".lev"
        try:
            fo = open( out, 'w' )
        except IOError:
            print ( 'Cannot open file ', fo.name, ' for writing: ', sys.exc_info() )
        else:
            print ( 'will write to: ' + out ) 
            args = "%s %s %s" % (self.levType.get(), self.levLength.get(), self.levDirection.get())
            print ( 'args: ' + args ) 
            lev = generator()
            lev.filename = out
            # args can be short, medium or long; right (otherwise left direction)
            if 'flat' in args: lev.create_flat( args )
            elif 'pipe' in args: lev.create_bang( args )
            elif 'flagtag' in args: lev.create_flagtag( args )
            else: lev.create_bang( args )
            lev.write()

    def quantize( self ):
        filename = filedialog.askopenfilename()
        if not filename: return
        path = os.path.dirname(filename)
        os.chdir(path)
        
        out = filedialog.asksaveasfilename()
        #out = f.name + '.txt'
        if not out: return
        if not out.endswith(".lev"): out += ".lev"

        try:
            fo = open( out, 'w' )
        except IOError:
            print ( 'Cannot open file ', fo.name, ' for writing: ', sys.exc_info() )
        else:
            lev = level.level()
            lev.filename = out
            print ( 'will write to: ' + out ) 
            lev.polys = []
            lev.objs = []
            

            f = open( filename, 'rb' )
            print ( 'reading ' + filename )
            f.read(7)
            lev.reclink = 'Reclink: ' + str(struct.unpack('i',f.read(4))[0])
            lev.integrity1 = 'Integrity 1: ' + str(struct.unpack('d',f.read(8))[0])
            lev.integrity2 = 'Integrity 2: ' + str(struct.unpack('d',f.read(8))[0])
            lev.integrity3 = 'Integrity 3: ' + str(struct.unpack('d',f.read(8))[0])
            lev.integrity4 = 'Integrity 4: ' + str(struct.unpack('d',f.read(8))[0])
            levname = str(''.join(struct.unpack('51c',f.read(51))))
            lev.lgr = 'LGR: "' + str(''.join(struct.unpack('16c',f.read(16)))) + '"'
            lev.ground = 'Ground: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"'
            lev.sky = 'Sky: "' + str(''.join(struct.unpack('10c',f.read(10)))) + '"'

            lev.name = "disturbized: " + levname
            polys = int(struct.unpack('d',f.read(8))[0])
            #print ( 'Polygons: ' + str(polys) )
            for p in range(polys):
                #print ( 'Polygon ' + str(p) + ':' )
                if struct.unpack('i',f.read(4))[0] == 1:
                    grass = 1 # grass poly
                else:
                    grass = 0
                #print ( 'Grass: ' + str(grass) )
                vs = int(struct.unpack('i',f.read(4))[0])
                vcs = []
                xscale = float( self.xscale.get() )
                yscale = float( self.yscale.get() )
                #print ( 'Verteces: ' + str(vs) )
                for v in range(vs):
                    #print ( 'Vertex ' + str(v) + ':' )
                    vxx = struct.unpack('d',f.read(8))[0]*(xscale)
                    vxy = struct.unpack('d',f.read(8))[0]*(yscale)
                    steps = float( self.step.get() )
                    # if not first vertex, a line can be calculated
                    # only do lines that are not vertical
                    if v and abs(vxx-vxx0) > 0.001 and not grass and steps >= 1:
                        # d:\programs\games\eol\lev
                        # haircut 5.0;0.03 makes you look at level high
                        # haircut 50;0.7 wild f-up
                        # maximum 1000 vertices
                        if vs * steps > 999: steps = 999.0/vs
                        disturbized = float( self.disturb.get() )
                        xstep = (vxx-vxx0)/steps
                        k = (vxy-vxy0)/(vxx-vxx0) # k = y1-y2/x1-x2
                        m = vxy - k*vxx# y = kx + m, m = y-kx
                        for step in range(1,int(steps)):
                            x = vxx0+xstep*step
                            y = k*x+m + random.random()*disturbized - random.random()*disturbized
                            vcs.append( x )
                            vcs.append( y )
                    elif not grass:
                        vcs.append( vxx )
                        vcs.append( vxy )
                    vxx0 = vxx
                    vxy0 = vxy
                if not grass: lev.polys.append( vcs )
                    
            obs = int(struct.unpack('d',f.read(8))[0])
            # print ( 'Objects: ' + str(obs) )
            for o in range(obs):
                obj = []
                obj.append( struct.unpack('d',f.read(8))[0] * xscale ) #x
                obj.append( struct.unpack('d',f.read(8))[0] * yscale ) #y
                obj.append( struct.unpack('i',f.read(4))[0] ) #type
                obj.append( struct.unpack('i',f.read(4))[0] ) #gravity
                obj.append( struct.unpack('i',f.read(4))[0] ) #animation
                lev.objs.append( obj )
            lev.write()
        f.close()
        messagebox.showinfo( 'Success', 'Wrote ' + out + ' successfully!' )
        
    def __init__( self, master=None ):
        Frame.__init__( self, master )
        self.grid( sticky='nsew' )
        self.generateText = Label( self, text='Generate Lev' )
        self.generateText.grid( row=0, column=0 )
        self.generateTypeText = Label( self, text='Lev Type' )
        self.generateTypeText.grid( column=0 )
        self.levType = StringVar()
        self.levType.set("bang")
        self.typeBang = Radiobutton( self, text='Headbanger', variable=self.levType, value='bang' )
        self.typeBang.grid( column=0 )
        self.typePipe = Radiobutton( self, text='Pipe', variable=self.levType, value='pipe' )
        self.typePipe.grid( column=0 )
        self.typeFlat = Radiobutton( self, text='Chris Lev', variable=self.levType, value='flat' )
        self.typeFlat.grid( column=0 )
        self.typeFlatT = Radiobutton( self, text='Flat tag Lev', variable=self.levType, value='flagtag' )
        self.typeFlatT.grid( column=0 )
        self.generateLengthText = Label( self, text='Lev Direction' )
        self.generateLengthText.grid( column=0 )
        self.levDirection = StringVar()
        self.levDirection.set("left")
        self.directionRight = Radiobutton( self, text='Right', variable=self.levDirection, value='right' )
        self.directionRight.grid( column=0 )
        self.directionLeft = Radiobutton( self, text='Left', variable=self.levDirection, value='left' )
        self.directionLeft.grid( column=0 )
        self.generateLengthText = Label( self, text='Lev Length' )
        self.generateLengthText.grid( column=0 )
        self.levLength = StringVar()
        self.levLength.set("short")
        self.generateShort = Radiobutton( self, text='Short', variable=self.levLength, value='short' )
        self.generateShort.grid( column=0 )
        self.generateMedium = Radiobutton( self, text='Medium', variable=self.levLength, value='medium' )
        self.generateMedium.grid( column=0 )
        self.generateLong = Radiobutton( self, text='Long', variable=self.levLength, value='long' )
        self.generateLong.grid( column=0 )
        self.button = Button( self, text='Generate Lev', command=self.generate )
        self.button.grid( column=0 )

        self.quantizeText = Label( self, text='Quantize Level' )
        self.quantizeText.grid( row=0, column=1 )
        self.stepText = Label( self, text='Steps (2-999) - 0 means no effect' )
        self.stepText.grid( row=1, column=1 )
        self.step = Entry( self )
        self.step.insert(0, "50")
        self.step.grid( row=2, column=1 )
        self.disturbText = Label( self, text='Disturbance (0.00-1.00) - 0 means no effect; you can do steps without disturbance but not disturbance without steps' )
        self.disturbText.grid( row=3, column=1 )
        self.disturb = Entry( self )
        self.disturb.insert(0, "0")
        self.disturb.grid( row=4, column=1 )
        self.xscaleText = Label( self, text='xscale: 1 means no effect; -1 means horizontal mirror, 2 means double width, 0.5 means half width' )
        self.xscaleText.grid( row=5, column=1 )
        self.xscale = Entry( self )
        self.xscale.insert(0, "1")
        self.xscale.grid( row=6, column=1 )
        self.yscaleText = Label( self, text='yscale: 1 means no effect; -1 means vertical mirror, 2 means double height, 0.5 means half height' )
        self.yscaleText.grid( row=7, column=1 )
        self.yscale = Entry( self )
        self.yscale.insert(0, "1")
        self.yscale.grid( row=8, column=1 )
        self.button = Button( self, text='Create Quantized Lev (click button to open lev, then choose filename to save as)', command=self.quantize )
        self.button.grid( row=9, column=1 )

        self.agreementText = Label( self, text='Agreement' )
        self.agreementText.grid( row=16, column=0, columnspan=2 )
        agreement = "By using this software I agree to doing everything I can to be as happy as I can"
        self.agreement = Entry( self, width=len(agreement) )
        self.agreement.insert(0, agreement )
        self.agreement.grid( row=17, column=0, columnspan=2 )
        
if __name__ == '__main__':
    root = Tk()
    root.title("Ribot's Lev Toolz")
    app = quantumlevTk( master=root )
    app.mainloop()

