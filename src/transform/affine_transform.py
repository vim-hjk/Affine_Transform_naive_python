import math
import numpy as np


class AffineTransform2D(object):
    def __init__(self, img=None):
        super().__init__()
        if img is not None:
            self.width, self.height = img.size
            self.img = np.array(img.getdata()).reshape(self.height, self.width, 3).tolist()
            self.cx = self.width // 2
            self.cy = self.height // 2        


    def translate(self, tx, ty, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2

        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    try:
                        output_img[y + ty][x + tx][ch] = img[y][x][ch]
                    except:
                        continue

        return output_img
    

    def scaling(self, sx, sy, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2           

        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    try:
                        output_img[cy + (y - cy) * sy][cx + (x - cx) * sx][ch] = img[y][x][ch]
                    except:
                        continue
        return output_img


    def back_scaling(self, sx, sy, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2           

        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]

        sx, sy = 1 / sx, 1 / sy

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    origin_pos_x = cx + (x - cx) * sx
                    origin_pos_y = cy + (y - cy) * sy

                    x_low = math.floor(origin_pos_x)
                    x_up = math.ceil(origin_pos_x)
                    y_low = math.floor(origin_pos_y)
                    y_up = math.ceil(origin_pos_y)
                    
                    s = origin_pos_x - x_low
                    t = origin_pos_y - y_low

                    try:
                        p1 = img[y_low][x_low][ch]
                        p2 = img[y_low][x_up][ch]
                        p3 = img[y_up][x_low][ch]
                        p4 = img[y_up][x_up][ch]

                        output_img[y][x][ch] = int((1 - s) * (1 - t) * p1 + (1 - s) * t * p3 + (1 - t) * s * p2 + s * t * p4)
                    except:
                        continue
        return output_img


    def rotate(self, degree, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2
        
        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]

        theta = degree * math.pi / 180.0    

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    rx = round(cx + math.cos(theta) * (x - cx) - math.sin(theta) * (y - cy))
                    ry = round(cy + math.sin(theta) * (x - cx) + math.cos(theta) * (y - cy))
                    if 0 <= ry <= height - 1 and 0 <= rx <= width - 1:
                        try:
                            output_img[ry][rx][ch] = img[y][x][ch]
                        except:
                            continue
        return output_img


    def back_rotate(self, degree, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2
        
        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]

        theta = degree * math.pi / 180.0

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    origin_pos_x = cx + math.cos(-theta) * (x - cx) - math.sin(-theta) * (y - cy)
                    origin_pos_y = cy + math.sin(-theta) * (x - cx) + math.cos(-theta) * (y - cy)

                    if 0 <= origin_pos_y <= height - 1 and 0 <= origin_pos_x <= width - 1:
                        x_low = math.floor(origin_pos_x)
                        x_up = math.ceil(origin_pos_x)
                        y_low = math.floor(origin_pos_y)
                        y_up = math.ceil(origin_pos_y)
                        
                        s = origin_pos_x - x_low
                        t = origin_pos_y - y_low

                        try:
                            p1 = img[y_low][x_low][ch]
                            p2 = img[y_low][x_up][ch]
                            p3 = img[y_up][x_low][ch]
                            p4 = img[y_up][x_up][ch]

                            output_img[y][x][ch] = int((1 - s) * (1 - t) * p1 + (1 - s) * t * p3 + (1 - t) * s * p2 + s * t * p4)
                        except:
                            continue
        return output_img


    def affine(self, tx, ty, degree, sx, sy, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2

        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]
        
        theta = math.radians(degree)

        a = sx * math.cos(theta)
        b = sy * -math.sin(theta)
        c = tx
        d = sx * math.sin(theta)
        e = sy * math.cos(theta)
        f = ty

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    ax = int(cx + (a * (x - cx) + b * (y - cy) + c))
                    ay = int(cy + (d * (x - cx) + e * (y - cy) + f))
                    if 0 <= ay <= height - 1 and 0 <= ax <= width - 1:
                        try:
                            output_img[ay][ax][ch] = img[y][x][ch]
                        except:
                            continue

        return output_img


    def back_affine(self, tx, ty, degree, sx, sy, img=None):
        if img is None:            
            width, height = self.width, self.height
            img = self.img
            cx, cy = self.cx, self.cy
        else:                        
            width, height = img.size
            img = np.array(img.getdata()).reshape(height, width, 3).tolist()
            cx, cy = width // 2, height // 2

        output_img = [[[0 for _ in range(3)] for _ in range(width)] for _ in range(height)]
        
        theta = math.radians(degree)

        sx, sy = 1 / sx, 1 / sy

        a = sx * math.cos(-theta)
        b = sy * -math.sin(-theta)
        c = tx
        d = sx * math.sin(-theta)
        e = sy * math.cos(-theta)
        f = ty

        for y in range(self.height):
            for x in range(self.width):
                for ch in range(3):
                    origin_pos_x = cx + (a * (x - cx) + b * (y - cy) + c)
                    origin_pos_y = cy + (d * (x - cx) + e * (y - cy) + f)
                    
                    if 0 <= origin_pos_y <= height - 1 and 0 <= origin_pos_x <= width - 1:
                        x_low = math.floor(origin_pos_x)
                        x_up = math.ceil(origin_pos_x)
                        y_low = math.floor(origin_pos_y)
                        y_up = math.ceil(origin_pos_y)
                        
                        s = origin_pos_x - x_low
                        t = origin_pos_y - y_low

                        try:
                            p1 = img[y_low][x_low][ch]
                            p2 = img[y_low][x_up][ch]
                            p3 = img[y_up][x_low][ch]
                            p4 = img[y_up][x_up][ch]

                            output_img[y][x][ch] = int((1 - s) * (1 - t) * p1 + (1 - s) * t * p3 + (1 - t) * s * p2 + s * t * p4)                    
                        except:
                            continue

        return output_img