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

class py2htmlTk( Frame ):
    def toHtml( self ):
        filename = filedialog.askopenfilename()
        if not filename: return
        path = os.path.dirname(filename)
        os.chdir(path)
        
        out = filedialog.asksaveasfilename()
        #out = f.name + '.txt'
        if not out: return

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
                #print ( 'Verteces: ' + str(vs) )
                for v in range(vs):
                    #print ( 'Vertex ' + str(v) + ':' )
                    vxx = struct.unpack('d',f.read(8))[0]
                    vxy = struct.unpack('d',f.read(8))[0]
                    # if not first vertex, a line can be calculated
                    # only do lines that are not vertical
                    if v and abs(vxx-vxx0) > 0.001 and not grass:
                        # d:\programs\games\eol\lev
                        # haircut 5.0;0.03 makes you look at level high
                        # haircut 50;0.7 wild f-up
                        steps = float( self.step.get() )
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
                obj.append( struct.unpack('d',f.read(8))[0] ) #x
                obj.append( struct.unpack('d',f.read(8))[0] ) #y
                obj.append( struct.unpack('i',f.read(4))[0] ) #type
                obj.append( struct.unpack('i',f.read(4))[0] ) #gravity
                obj.append( struct.unpack('i',f.read(4))[0] ) #animation
                lev.objs.append( obj )
            lev.write()
        f.close()
        messagebox.showinfo( 'Success', 'Wrote ' + out + ' successfully!' )

    def __init__( self, master=None ):
        self.line_break='<br />'
        self.nb_space='&nbsp;'
        Frame.__init__( self, master )
        self.grid( sticky='nsew' )
        self.stepText = Label( self, text='Steps (2-999)' )
        self.stepText.grid()
        self.step = Entry( self )
        self.step.insert(0, "50")
        self.step.grid()
        self.disturbText = Label( self, text='Disturbance (0-1)' )
        self.disturbText.grid()
        self.disturb = Entry( self)
        self.disturb.insert(0, "0")
        self.disturb.grid()
        self.defaultPathText = Label( self, text='Default Path' )
        self.defaultPathText.grid()
        self.defaultPath = Entry( self)
        self.defaultPath.insert(0, "d:\programs\games\eol\lev")
        self.defaultPath.grid()
        self.button = Button( self, text='Create', command=self.toHtml )
        self.button.grid()
        
if __name__ == '__main__':
    root = Tk()
    app = py2htmlTk( master=root )
    app.mainloop()

