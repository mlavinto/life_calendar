import argparse
import cv2
from datetime import datetime, timedelta, date
import numpy as np
import webcolors

class Calendar():
    def __init__(self, 
                 resolution=(1920, 1080), 
                 startdate=date(1970, 1, 1), 
                 defcolor=[32, 192, 64],
                 enddate=date(2070, 1, 1),
                 lifetime=None):
            
        if lifetime is not None:
            enddate = startdate + lifetime

        self.resolution = resolution
        self.startdate = startdate
        self.enddate = enddate
        self.years = enddate.year - startdate.year + 1
        self.canvas = np.zeros([self.years, 371, 3])
        self.defcolor=defcolor
        
    def colorize(self, pos):
        """ Defines the pixel color mapping ruleset       
        """
        defcolor = self.defcolor[pos[2]]
        firstday = date(self.startdate.year + pos[0], 1, 1).weekday()
        
        ## Deal with first / last year
        if pos[0] == 0:
            firstday = firstday + (self.startdate - date(self.startdate.year, 1, 1)).days
        
        if ((pos[0] == 0) and (self.years == 1)):
            ndays = (self.enddate - self.startdate).days + 1
        elif pos[0] == 0:
            ndays = (date(self.startdate.year, 12, 31) - self.startdate).days + 1
        elif pos[0] == self.years - 1:
            ndays = (self.enddate - date(self.enddate.year, 1, 1)).days + 1
        else:
            ndays = (date(self.startdate.year + pos[0], 12, 31) - date(self.startdate.year + pos[0], 1, 1)).days + 1
        
        ## Todays pixel
        ytoday = datetime.today().date().year - self.startdate.year
        dtoday = (datetime.today().date() - date(datetime.today().date().year, 1, 1)).days + firstday
        
        ## Boundary 
        if ((pos[1] < firstday) | (pos[1] >= firstday + ndays)):
            return 0
        
        ## Blackout today's pixel
        if (ytoday == pos[0] ) & (dtoday == pos[1]):
            return 0
        
        ## Coloring grid
        if pos[1] % 14 < 7:
            defcolor = defcolor * 0.85
        if pos[0]%2 ==0:
            defcolor = defcolor * 0.85
        if pos[0]%10 ==0:
            defcolor = defcolor * 0.85        
        if pos[1]%2 ==0:
            defcolor = defcolor * 0.85
        
        ## Past is darkened
        if ((ytoday > pos[0]) | ((ytoday == pos[0]) & (dtoday > pos[1]))):
            defcolor = defcolor * 0.3
            
        return int(defcolor)
    
    def draw(self):
        """ Calculates the canvas and outputs a file
        """
        
        self.canvas = np.zeros([self.years, 371, 3])
        it = np.nditer(self.canvas, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = self.colorize(it.multi_index)
            it.iternext()
        res = cv2.resize(self.canvas, self.resolution, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite('img.png', res)
        return None

        

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--width', type=int, default=1920, help='Image width, pixels')
    p.add_argument('--height', type=int, default=1080, help='Image height, pixels')
    p.add_argument('--startdate', type=str, default='1970-01-01', help='Calendar start, format YYYY-MM-DD')
    p.add_argument('--enddate', type=str, default='2070-01-01', help='Calendar end, format YYYY-MM-DD')
    p.add_argument('--basecolor', type=str, default='limegreen', help='Base color in CSS3 names. Should be relatively light.')
    args = p.parse_args()
    c = Calendar(resolution = (args.width, args.height), 
                 startdate = datetime.strptime(args.startdate, '%Y-%m-%d').date(), 
                 enddate = datetime.strptime(args.enddate, '%Y-%m-%d').date(),
                 defcolor = list(reversed(webcolors.name_to_rgb(args.basecolor))))
    
    c.draw()
                    