from cmath import sin, cos
import math


inlist = []
figure = []
LFig = []
RFig = []
temp = []
MovTemp = []


######## Functions ########

# The rotation formula used for sin and cos


def rot(d):
    r = (-d * math.pi) / 180
    return r


# Initial Figure creator & RFig rotator and point creator
def setup(t, tempx, tempy, oldx, oldy):
    x = cos(rot(t)) * (tempx - oldx) + (tempy - oldy) * sin(rot(t)) + oldx
    y = -sin(rot(t)) * (tempx - oldx) + cos(rot(t)) * (tempy - oldy) + oldy
    x = x.real
    y = y.real
    x = round(x, 3)
    y = round(y, 3)
    return [x, y]


# Rotates and creates points for LFig
def rotate(a, b, t):
    x = a * cos(rot(t)) - b * sin(rot(t))
    y = b * cos(rot(t)) + a * sin(rot(t))
    x = x.real
    y = y.real
    x = round(x, 3)
    y = round(y, 3)
    return [x, y]


# shifts the values in order for the left most value to be in (0,0)
def move(x, y, xshift, yshift):
    x = x - xshift
    y = y - yshift
    x = x.real
    y = y.real
    return [x, y]


# checks for intersection between given points and created points
def intersect(x0, y0, x1, y1, x2, y2, x3, y3):
    p0 = (y3 - y2) * (x3 - x0) - (x3 - x2) * (y3 - y0)
    p1 = (y3 - y2) * (x3 - x1) - (x3 - x2) * (y3 - y1)
    p2 = (y1 - y0) * (x1 - x2) - (x1 - x0) * (y1 - y2)
    p3 = (y1 - y0) * (x1 - x3) - (x1 - x0) * (y1 - y3)
    # if both product below are negative, the segments don't intersect
    alpina = p0 * p1
    Blpina = p2 * p3
    if (alpina < 0):
        if Blpina < 0:
            return 1
        else:
            return 0
    else:
        return 0


################ The main work ################
foo = len(open('input.txt').readlines())
bar = foo - 1
# File opener
lncnt = len(open('input.txt').readlines())

with open('input.txt', 'r') as f:
    n = f.readline()
    n = int(n)  # <== Number of iterations
    for i in range(bar):  # <== makes a list of points given from input
        elem = f.readline().split()
        # for i in elem:
        apu = float(elem[0])
        bpu = float(elem[1])
        cpu = float(elem[2])
        dpu = float(elem[3])
        inlist.append([apu, bpu])
        inlist.append([float(elem[2]), float(elem[3])])

if n >= 1:
    # creates the initial figure with known points
    figure.append(setup(0, 0, 0, 0, 0))
    figure.append(setup(60, 1, 0, 0, 0))
    figure.append(setup(120, 0, 0, 0.5, 0.866))
    figure.append(setup(120, 0.5, 0.866, 1.5, 0.866))
for Main_index in range(n - 1):
    # !Tip: select section and press tab to shift all / Shift Tab to remove shift

    if n >= 2:
        # these help find the last values to input into RFig and set the rotation point
        lenfig = len(figure) - 1
        LstofFig = [figure[lenfig][0], figure[lenfig][1]]

        # LFig and Rfig collect and grab values from figure to clone and orientate themselves
        for i in figure:
            LFig.append(rotate(i[0], i[1], 120))
            RFig.append(setup(120, i[0], i[1], LstofFig[0], LstofFig[1]))
            pass

        LFig.reverse()  # <= reversed list so when moved, the first point starts at (0,0)
        LFig.pop()  # <= removes the last point that is a copy of figure's first point
        temp.extend(LFig)
        figure.pop()  # <= removes the last point that is a copy of RFig's first point
        temp.extend(figure)
        RFig.reverse()  # <= reverses so the right most value is the last value in list
        temp.extend(RFig)

        # looks for where the first point values and sees how much is needed to move
        xshift = temp[00][0]
        yshift = temp[00][1]
        for i in temp:
            xscan = i[0]
            yscan = i[1]
            MovTemp.append(move(xscan, yscan, xshift, yshift))

        # Clears all values and stores the new values into Figure for next iteration
        figure.clear()
        LFig.clear()
        RFig.clear()
        figure.extend(MovTemp)
        temp.clear()
        MovTemp.clear()
        LstofFig.clear()
        # Loop end hopefully

output = open('output.txt', 'w+')

intcnt = 0
# ^^ this will keep track if any segments intersect, if yes + 1.
# When the for loop ends it will check if: value > 0 print 1 else: print 0
# print('figure length', len(figure))
for zz in range(len(inlist)):
    if zz >= len(inlist):
        pass
    else:
        zz = zz * 2  # made to iterate by 2 instead of 1 b/c inlist is grouped by 4's such that [0] and [1] are a pair
        pp = zz + 1  # grabs the odd pair of inlist aka [1], [3] etc...
        if pp <= len((inlist)):
            intcnt = 0
            for i in range(len(figure)):
                j = i + 1
                if intcnt > 0:
                    break
                #if inlist[zz][0]<figure[i][0]<inlist[pp][0] or inlist[zz][0]<figure[i][0]<inlist[pp][0]:
                #    print("it works")
                if j < len(figure):
                    intcnt += intersect(figure[i][0], figure[i][1], figure[j][0], figure[j][1], inlist[zz][0],
                                        inlist[zz][1], inlist[pp][0], inlist[pp][1])  # the Main fnc of the loop
                else:
                    pass
            if (intcnt > 0):
                print('true')
                output.write('1\n')
            else:
                print('false')
                output.write('0\n')
        else:
            pass
