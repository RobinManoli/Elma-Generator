"""
This script, made by Tyrtko, was taken from http://snippets.dzone.com/posts/show/5330
updated and modified into a Tk application.
Then modified by Robin Manoli to code2html, and here recreated as this file.
"""

import sys
import os
import level
import struct

if sys.version_info < (3, 0) or True:
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
            xratio = 50
            yratio = 50
            

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

            lev.name = "Quantized: " + levname
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
                    vxx = struct.unpack('d',f.read(8))[0]*(xratio/100.0)
                    vxy = struct.unpack('d',f.read(8))[0]*(yratio/100.0)
                    vcs.append( vxx )
                    vcs.append( vxy )
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
        f.close()
        messagebox.showinfo( 'Success', 'Wrote ' + out + ' successfully!' )

    def __init__( self, master=None ):
        self.line_break='<br />'
        self.nb_space='&nbsp;'
        Frame.__init__( self, master )
        self.grid( sticky='nsew' )
        self.button = Button( self, text='Convert', command=self.toHtml )
        self.button.grid()
        
if __name__ == '__main__':
    root = Tk()
    app = py2htmlTk( master=root )
    app.mainloop()

