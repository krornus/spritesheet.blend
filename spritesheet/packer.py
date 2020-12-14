import math
from PIL import Image

class Packer:
    def __init__(self, files, mode="RGBA", maxcol=10, step=1):
        if not len(files):
            raise ValueError("Missing files")

        if step <= 0:
            raise ValueError("Invalid step size")

        self.files = files
        self.mode = mode
        self.maxcol = maxcol

        self.tilesize, self.frames = self.load_all(files, step=step)
        self.sheetsize = self.sheetdim(self.tilesize, len(self.frames), maxcol)

    def load_all(self, files, step=1):
        data = [self.load(files[0])]
        size = data[0].size

        for fn in files[step::step]:
            im = self.load(fn)
            if im.size != size:
                raise ValueError("Mismatched size for file %s" % fn)
            data.append(im)

        return size, data

    def load(self, filepath):
        with Image.open(filepath) as im:
            return im.getdata()

    def sheetdim(self, tilesize, framecount, maxcol):
        if framecount > maxcol:
            maxrow = int(math.ceil(framecount/float(maxcol)))
            width = tilesize[0] * maxcol
            height = tilesize[1] * maxrow
        else:
            width = width * len(frames)
            height = tilesize[1]

        return width, height

    def pack(self):
        sheet = Image.new(self.mode, self.sheetsize)

        for i, frame in enumerate(self.frames):
            top = self.tilesize[1] * (i // self.maxcol)
            left = self.tilesize[0] * (i % self.maxcol)
            bottom = top + self.tilesize[1]
            right = left + self.tilesize[0]

            box = (left, top, right, bottom)

            sheet.paste(frame, box)

        return sheet
