import cv2
import numpy as np
from datetime import datetime, timedelta, date

class Calendar():
    def __init__(self, 
                 resolution=(1920, 1080), 
                 startdate=date(1970, 1, 1), 
                 enddate=None,
                 lifetime=None):
        
        if enddate is None:
            if lifetime is None:
                enddate = startdate + timedelta(days=100*365)
            else:
                enddate = startdate + lifetime

        self.resolution = resolution
        self.startdate = startdate
        self.enddate = enddate
        self.years = (self.enddate - self.startdate).days // 365
        self.yearsize = self.resolution[1] // self.years
        self.daysize = self.resolution[0] // 365
        self.totoday = (datetime.today().date() - startdate).days
        
        self.canvas = np.zeros([self.years, 365, 3])
        self.yearsize=1
        self.daysize=1
        
    def coloring(self, pos):
        j = pos[0]
        i = pos[1]
        defcolo = np.array([32, 192, 64])
        if (i//self.daysize) % 2 == 0:
            defcolo = defcolo * 0.75
        if (i//self.daysize) % 14 < 7:
            defcolo = defcolo * 0.75
        if (j//self.yearsize) % 2 == 0:
            defcolo = defcolo * 0.75
        if i//self.daysize + (j//self.yearsize)*365  < self.totoday:
            defcolo = defcolo * 0.5
        if i//self.daysize + (j//self.yearsize)*365 == self.totoday:
            defcolo = defcolo * 0       
        return int(defcolo[pos[2]])
    
    def draw(self):
        it = np.nditer(self.canvas, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = self.coloring(it.multi_index)
            it.iternext()
        res = cv2.resize(self.canvas, self.resolution, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite('img.png', res)
        return None
        

if __name__ == '__main__':
    c = Calendar(startdate=date(1970,1,1), lifetime=timedelta(days=75*365))
    c.draw()
                    