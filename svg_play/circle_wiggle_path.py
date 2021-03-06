import math
import random
from svg_generation import save_svg


def find_points(radius, num_points = 6):
    ''' Finds 12 (or how many are entered) points on the path of a circle and returns their coords '''
    points = []
    r = radius
    for index in range(num_points):
        points.append((r * math.cos((index * 2 * math.pi) / num_points), r * math.sin((index * 2 * math.pi) / num_points)))
    return points

def two_points(m, point, length):
    #returns two points for handles given one point
    px,py = point
    if m is None:
        x= px
        x1= px
        y= py - length
        y1= py + length
    else:    
        x = px + length * math.sqrt(1 / (1 + m ** 2))
        x1 = px - length * math.sqrt(1 / (1 + m ** 2))
        y = py + m * length * math.sqrt(1 / (1 + m ** 2))
        y1 = py - m * length * math.sqrt(1/ (1 + m ** 2)) 
    return ((x, y), (x1, y1))

def inv_grad(p1, p2 = (0, 0)):
    #Find the perpendicular gradient 
    x1, y1 = p1
    x2, y2 = p2
    m = (y2 - y1) / (x2 - x1)
    if m == 0:
        return None
    return -1 / m

def make_handles(flip_flag, points, length):
    #this function gets passed the points and returns the handles
    handles = []
    for i, point in enumerate(points):
        #C format past anchor, current anchor, current point
        m = inv_grad(point)
        a, b = two_points(m, point, length)
        if flip_flag:
            #handling an exception I don't understand the maths for, sorry purists
            if i == 9:
                handles.append((a, b))
            else:
                handles.append((b, a))
        else:
            handles.append((a, b))
        if m is None or m >80:
            flip_flag = not flip_flag
    return handles, flip_flag

def wiggle(px, py, length):
    #this function adjusts the point given by a small random amount
    #sets to -1 or 1 based on x direction from origin
    x_shift = (px < 0) * -2 + 1
    y_shift = (py < 0) * -2 + 1
    
    px += x_shift * random.random() * (length * 2)
    py += y_shift * random.random() * (length * 2)
    return px, py



def make_wiggly_circles(radius, size, moves):
    length = radius/6
    
    #used to get the order of the handles correct
    flip_flag  = False 
    
    output_string = ''
    # print(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{size*4}" height="{size*2}" viewBox="-{radius*1.5} -{radius*2} {size*2.5} {size*2.5} ">\n')
    # print(f'<style type="text/css"> .blk{{fill:none;stroke:{color};stroke-width:0.25;}}</style>\n')

    points = find_points(radius)
    #rotate points 4 times
    for _ in range(3):
        point = points.pop(0)
        points.append(point)

    handles, flip_flag = make_handles(flip_flag, points, length)

    for move in range(moves):
        x_trans = move * random.random() * radius / 10 + move * 10
        y_trans = move * random.random() * random.choice((-1, 1)) * radius / 20 
        p = f'<path transform="translate({x_trans} {y_trans})" class="blk" d="'

        first_point = points[-1] #need the circle to loop
        fx, fy = first_point
        fx, fy = wiggle(fx, fy, length)
        p+=f'M {fx} {fy} '

        #slightly adjust all the points in the circle

        for i, point in enumerate(points[:-1]):
            px, py = point
            handle1 = handles[i-1][1]
            h1x, h1y = handle1
            h1x, h1y = wiggle(h1x, h1y, length)
            handle2 = handles[i][0]
            h2x, h2y = handle2
            h2x, h2y = wiggle(h1x, h1y, length)
            px, py = wiggle(px, py, length)
            p+=f'C {round(h1x,2)} {round(h1y,2)} {round(h2x,2)} {round(h2y,2)} {round(px,2)} {round(py,2)} '

        #last point
        px, py = fx, fy
        handle1 = handles[-2][1]
        h1x, h1y = handle1
        h1x, h1y = wiggle(h1x, h1y, length)
        handle2 = handles[-1][0]
        h2x, h2y = handle2
        p+=f'C {round(h1x,2)} {round(h1y,2)} {round(h2x,2)} {round(h2y,2)} {round(px,2)} {round(py,2)} '
        #this fixes the stupid spiky join stupid
            
        p+=' Z"/>\n'
        
        output_string += p
    return output_string
    
def main(num,imageSize):
    grid = {}
    c_size = imageSize/num
    color='blue'
    final_string = f'<style type="text/css"> .blk{{fill:none;stroke:{color};stroke-width:0.25;}}</style>'
    for r in range(num):
        for c in range(num):
            n = random.randint(0,4)
            s = 2
            rad = c_size/2
            twos = n//2
            ones = n%2

            x = c * c_size + (rad * int(twos != ones))
            y = r * c_size + rad + (rad * twos) - (rad * ones)	
            end_x=c * c_size + rad + (rad * int(twos != ones))
            end_y=r * c_size + (rad * int(ones)) + (rad * int(twos))
            large_a_f = 1
            small_a_f = 1 * twos
            
            # grid[(r,c)] =curve
            final_string += make_wiggly_circles(rad, s, n)

    save_svg(final_string, '/home/ruser/tmp/', 'svg_gen_play3.svg')


if __name__ == '__main__':
    main(5,1440)