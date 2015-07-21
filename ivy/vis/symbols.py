"""
Convenience functions for drawing shapes on TreePlots.
"""
try:
    import Image
except ImportError:
    from PIL import Image
from numpy import pi
from matplotlib.collections import RegularPolyCollection, CircleCollection
from matplotlib.transforms import offset_copy
from matplotlib.patches import Rectangle, Wedge, Circle, PathPatch
from matplotlib.offsetbox import DrawingArea
from itertools import izip_longest
from matplotlib.axes import Axes
from numpy import array
from matplotlib.path import Path


try:
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
except ImportError:
    pass
from ..tree import Node
import colors as _colors

def _xy(plot, p):
    if isinstance(p, Node):
        c = plot.n2c[p]
        p = (c.x, c.y)
    elif isinstance(p, (list, tuple)):
        p = [ _xy(plot, x) for x in p ]
    else:
        pass
    return p

def image(plot, p, imgfile,
          maxdim=100, border=0,
          xoff=4, yoff=4,
          halign=0.0, valign=0.5,
          xycoords='data', boxcoords=('offset points')):
    if xycoords == "label":
        xycoords = plot.node2label[p]
        x, y = (1, 0.5)
    else:
        x, y = _xy(plot, p)
    img = Image.open(imgfile)
    if max(img.size) > maxdim:
        img.thumbnail((maxdim, maxdim))
    imgbox = OffsetImage(img)
    abox = AnnotationBbox(imgbox, (x, y),
                          xybox=(xoff, yoff),
                          xycoords=xycoords,
                          box_alignment=(halign,valign),
                          pad=0.0,
                          boxcoords=boxcoords)
    plot.add_artist(abox)
    plot.figure.canvas.draw_idle()

def images(plot, p, imgfiles,
          maxdim=100, border=0,
          xoff=4, yoff=4,
          halign=0.0, valign=0.5,
          xycoords='data', boxcoords=('offset points')):
    for x, f in zip(p, imgfiles):
        image(plot, x, f, maxdim, border, xoff, yoff, halign, valign,
              xycoords, boxcoords)

def pie(plot, p, values, colors=None, size=16, norm=True,
        xoff=0, yoff=0,
        halign=0.5, valign=0.5,
        xycoords='data', boxcoords=('offset points')):
    x, y = _xy(plot, p)
    da = DrawingArea(size, size); r = size*0.5; center = (r,r)
    x0 = 0
    S = 360.0
    if norm: S = 360.0/sum(values)
    if not colors:
        c = _colors.tango()
        colors = [ c.next() for v in values ]
    for i, v in enumerate(values):
        theta = v*S
        if v: da.add_artist(Wedge(center, r, x0, x0+theta,
                                  fc=colors[i], ec='none'))
        x0 += theta
    box = AnnotationBbox(da, (x,y), pad=0, frameon=False,
                         xybox=(xoff, yoff),
                         xycoords=xycoords,
                         box_alignment=(halign,valign),
                         boxcoords=boxcoords)
    plot.add_artist(box)
    plot.figure.canvas.draw_idle()
    return box

def hbar(plot, p, values, colors=None, height=16,
         xoff=0, yoff=0,
         halign=1, valign=0.5,
         xycoords='data', boxcoords=('offset points')):
    x, y = _xy(plot, p)
    h = height; w = sum(values) * height#; yoff=h*0.5
    da = DrawingArea(w, h)
    x0 = -sum(values)
    if not colors:
        c = _colors.tango()
        colors = [ c.next() for v in values ]
    for i, v in enumerate(values):
        if v: da.add_artist(Rectangle((x0,0), v*h, h, fc=colors[i], ec='none'))
        x0 += v*h
    box = AnnotationBbox(da, (x,y), pad=0, frameon=False,
                         xybox=(xoff, yoff),
                         xycoords=xycoords,
                         box_alignment=(halign,valign),
                         boxcoords=boxcoords)
    plot.add_artist(box)
    plot.figure.canvas.draw_idle()

def hbars(plot, p, values, colors=None, height=16,
          xoff=0, yoff=0,
          halign=1, valign=0.5,
          xycoords='data', boxcoords=('offset points')):
    for x, v in zip(p, values):
        hbar(plot, x, v, colors, height, xoff, yoff, halign, valign,
             xycoords, boxcoords)

def squares(plot, p, colors='r', size=15, xoff=0, yoff=0, alpha=1.0,
            zorder=1000):
    points = _xy(plot, p)
    trans = offset_copy(
        plot.transData, fig=plot.figure, x=xoff, y=yoff, units='points')

    col = RegularPolyCollection(
        numsides=4, rotation=pi*0.25, sizes=(size*size,),
        offsets=points, facecolors=colors, transOffset=trans,
        edgecolors='none', alpha=alpha, zorder=zorder
        )

    plot.add_collection(col)
    plot.figure.canvas.draw_idle()

def tipsquares(plot, p, colors='r', size=15, pad=2, edgepad=10):
    x, y = _xy(plot, p) # p is a single node or point in data coordinates
    n = len(colors)
    da = DrawingArea(size*n+pad*(n-1), size, 0, 0)
    sx = 0
    for c in colors:
        sq = Rectangle((sx,0), size, size, color=c)
        da.add_artist(sq)
        sx += size+pad
    box = AnnotationBbox(da, (x, y), xybox=(-edgepad,y),
                         frameon=False,
                         pad=0.0,
                         xycoords='data',
                         box_alignment=(1, 0.5),
                         boxcoords=('axes points','data'))
    plot.add_artist(box)
    plot.figure.canvas.draw_idle()
    

def circles(plot, p, colors='g', size=15, xoff=0, yoff=0):
    points = _xy(plot, p)
    trans = offset_copy(
        plot.transData, fig=plot.figure, x=xoff, y=yoff, units='points'
        )

    col = CircleCollection(
        sizes=(pi*size*size*0.25,),
        offsets=points, facecolors=colors, transOffset=trans,
        edgecolors='none'
        )

    plot.add_collection(col)
    plot.figure.canvas.draw_idle()
    return col

def legend(plot, colors, labels, shape='rectangle', loc='upper left', **kwargs):
    if shape == 'circle':
        shapes = [ Circle((0.5,0.5), radius=1, fc=c) for c in colors ]
        #shapes = [ CircleCollection([10],facecolors=[c]) for c in colors ]
    else:
        shapes = [ Rectangle((0,0),1,1,fc=c,ec='none') for c in colors ]
        
    return Axes.legend(plot, shapes, labels, loc=loc, **kwargs)

def leafspace_triangles(plot, color='black', rca=0.5):
    """
    rca = relative crown age
    """
    leaves = plot.root.leaves()
    leafspace = [ float(x.leafspace) for x in leaves ]
    #leafspace = array(raw_leafspace)/(sum(raw_leafspace)/float(len(leaves)))
    pv = []
    for i, n in enumerate(leaves):
        if leafspace[i] > 0:
            p = plot.n2c[n]
            pp = plot.n2c[n.parent]
            spc = leafspace[i]
            yoff = spc/2.0
            x0 = pp.x + (p.x - pp.x)*rca
            verts = [(x0, p.y),
                     (p.x, p.y-yoff),
                     (p.x, p.y+yoff),
                     (x0, p.y)]
            codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
            path = Path(verts, codes)
            patch = PathPatch(path, fc=color, lw=0)
            pv.append(plot.add_patch(patch))
    return pv

def text(plot, x, y, s, color='black', xoff=0, yoff=0, valign='center',
         halign='left', fontsize=10):
    txt = plot.annotate(
        s, xy=(x, y),
        xytext=(xoff, yoff),
        textcoords="offset points",
        verticalalignment=valign,
        horizontalalignment=halign,
        fontsize=fontsize,
        clip_on=True,
        picker=True
    )
    txt.set_visible(True)
    return txt
    
