'''
2d lab
darrell dupas
dirtslayer@gmail.com

pong plus some draggable shapes
'''


import simplegui



class DragManager:
    
    def __init__(self):
        self.dragitems_waiting = []
        self.dragitems_being_dragged = []
        self.currently_dragging = False
        self.start_of_drag = (0,0)
        
       
    
    def add_dragable_item(self,i):
        self.dragitems_waiting.append(i)
    
    def check_for_hit(self,xy):
        
        #print("check for hit")
        for i in self.dragitems_waiting:
            
            if i.hit_test(xy):
                self.currently_dragging = True
                i.isdragging = True
                self.dragitems_being_dragged.append(i) 
                self.start_of_drag = xy
                i.set_drag_shift(xy)
                
    def drag_hit_items(self,xy):
        #print("drag")
        #print(str(self.dragitems_being_draged))
        for i in self.dragitems_being_dragged:
            i.move_to(xy)
       
    def release_at(self,xy):
        #print('release at')
        for i in self.dragitems_being_dragged:
            i.isdragging = False
        self.dragitems_being_dragged = []
  
        self.currently_dragging = False
       
        
class Glueable:
    '''
    a 2d shape primitive like rectangle / circle / point / image
    can glue to another primitave, which indicates that
    if one moves so should the other. these groupings will 
    have one primative as the glue master, so all members 
    of the group will point to the gloom master
    
    '''
    pass   
        
class Dragable:

    def __init__(self,xy):
        self.xy = xy
        self.isdragging = False
        self.enabled = True
        
     # virtual functions
    def move_to(self,xy):
        pass
        #self.xy = xy
     
    def set_drag_shift(self,xy):
        pass
    
    def hit_test(self,xy):
        pass
    
    
class Point(Dragable):
    
    def __init__(self,xy):
        self.xy = xy
        self.radius = 4
        self.color = "Red"

    def move_to(self,xy):
        #print('point moveto')
        self.xy = (xy[0] + self.drag_shift[0], xy[1] + self.drag_shift[1]) 
          
        
    def draw(self,c):
         c.draw_circle(self.xy, self.radius - 1, 1, self.color, self.color)
    
    def hit_test(self,xy):
        
        dx = abs(self.xy[0] - xy[0])
        if dx > self.radius :
            #print('point hit false')
            return False
        dy = abs(self.xy[1] - xy[1])
        if dy > self.radius :
            #print('point hit false')
            return False
        #print('point hit true')
        return True
    
    def set_drag_shift(self,xy):
        self.drag_shift = (self.xy[0]-xy[0] ,self.xy[1] - xy[1]) 
        #print('drag shift : ',self.drag_shift)

class Circle(Point):

    def __init__(self,center_xy,radius):
        self.xy = center_xy
        self.radius = radius
        self.radius_squared = radius * radius
        self.color = "yellow"
        
    def hit_test(self,xy):
        
        tl = (self.xy[0]-self.radius,self.xy[1]-self.radius)
        br = (self.xy[0]+self.radius,self.xy[1]+self.radius)

        if tl[0] > xy[0]:
            #print('left of')
            return False
        if br[0] < xy[0]:
            #print('right of')
            return False
        if tl[1] > xy[1]:
            #print('above')
            return False
        if br[1] < xy[1]:
            #print('below')
            return False

        # end quick test


        #print('circle hit test implementation')
        dx_squared = self.xy[0] - xy[0]
        dx_squared = dx_squared * dx_squared
        dy_squared = self.xy[1] - xy[1]
        dy_squared = dy_squared * dy_squared
        ds = dx_squared + dy_squared
        
        if ds > self.radius_squared :
            #print('circle hit false')
            return False
        #print('circle hit true')
        return True


class Rectangle(Dragable):
          
    def __init__(self,top_left,bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.color = "Silver"
        self.nhits = 0

    def draw(self,c):
        '''
        this is the ugliest line of code i have ever written it makes me want to barf
        '''
        c.draw_polygon([[self.tl[0], self.tl[1]], [self.br[0], self.tl[1]], 
                        [self.br[0],self.br[1]], [self.tl[0],self.br[1]]], 
                       1, self.color, self.color)
    
    def hit_test(self,xy):
        #print('rectangle hit test implementation')
        if self.tl[0] > xy[0]:
            #print('left of')
            return False
        if self.br[0] < xy[0]:
            #print('right of')
            return False
        if self.tl[1] > xy[1]:
            #print('above')
            return False
        if self.br[1] < xy[1]:
            #print('below')
            return False
        #print('rect hit')
        self.nhits += 1
        return True
        
    def width(self):
        return self.br[0] - self.tl[0]
   
    def height(self):
        return self.br[1] - self.tl[1]
    
    def move_to(self,xy):
        h = self.height()
        w = self.width()
        self.tl = (xy[0] + self.drag_shift[0], xy[1] + self.drag_shift[1]) 
        self.br = ( self.tl[0] + w, self.tl[1] + h )
     
    @property
    def xy(self):
        return self.tl
    
    def set_drag_shift(self,xy):
        self.drag_shift = (self.tl[0]-xy[0] ,self.tl[1] - xy[1]) 
        #print('drag shift : ',self.drag_shift)
    
    
    
class Triangle(Dragable):
    
    def __init__(self,p0,p1,p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.color = "Green"

    def draw(self,c):
       c.draw_polygon([self.p0,self.p1,self.p2],1, self.color, self.color)
    
    def quick_hit(self,xy):
        tl = ( min(self.p0[0],self.p1[0],self.p2[0]), min(self.p0[1],self.p1[1],self.p2[1]))
        br = ( max(self.p0[0],self.p1[0],self.p2[0]), max(self.p0[1],self.p1[1],self.p2[1]))
        
        if tl[0] > xy[0]:
            #print('left of')
            return False
        if br[0] < xy[0]:
            #print('right of')
            return False
        if tl[1] > xy[1]:
            #print('above')
            return False
        if br[1] < xy[1]:
            #print('below')
            return False
        return True
    
    def hit_test(self,p):
        if not self.quick_hit(p):
            return False
        pX = p[0]
        pY = p[1]
        p0X = self.p0[0]
        p0Y = self.p0[1]
        p1X = self.p1[0]
        p1Y = self.p1[1]
        p2X = self.p2[0]
        p2Y = self.p2[1]

        s = p0Y * p2X - p0X * p2Y + (p2Y - p0Y) * pX + (p0X - p2X) * pY
        t = p0X * p1Y - p0Y * p1X + (p0Y - p1Y) * pX + (p1X - p0X) * pY

        if ((s < 0) != (t < 0)):
            return False

        A = -p1Y * p2X + p0Y * (p2X - p1X) + p0X * (p1Y - p2Y) + p1X * p2Y
    
        if (A < 0):
            s = -s
            t = -t
            A = -A
            
        return s > 0 and t > 0 and (s + t) < A
       
    def move_to(self,xy):
        w1 = self.p1[0] - self.p0[0]
        h1 = self.p1[1] - self.p0[1]
        
        w2 = self.p2[0] - self.p0[0]
        h2 = self.p2[1] - self.p0[1]
          
        self.p0 = ( xy[0] + self.drag_shift[0], xy[1] + self.drag_shift[1]) 
        self.p1 = ( self.p0[0] + w1, self.p0[1] + h1 )
        self.p2 = ( self.p0[0] + w2, self.p0[1] + h2 )
        
        
    @property
    def xy(self):
        return self.p0
    
    def set_drag_shift(self,xy):
        self.drag_shift = (self.p0[0]-xy[0] ,self.p0[1] - xy[1]) 
     
'''
http://stackoverflow.com/questions/2049582/how-to-determine-a-point-in-a-triangle

public static bool PointInTriangle(Point p, Point p0, Point p1, Point p2)
{
    var s = p0.Y * p2.X - p0.X * p2.Y + (p2.Y - p0.Y) * p.X + (p0.X - p2.X) * p.Y;
    var t = p0.X * p1.Y - p0.Y * p1.X + (p0.Y - p1.Y) * p.X + (p1.X - p0.X) * p.Y;

    if ((s < 0) != (t < 0))
        return false;

    var A = -p1.Y * p2.X + p0.Y * (p2.X - p1.X) + p0.X * (p1.Y - p2.Y) + p1.X * p2.Y;
    if (A < 0.0)
    {
        s = -s;
        t = -t;
        A = -A;
    }
    return s > 0 && t > 0 && (s + t) < A;
}
'''


class Ball(Circle):
    '''
    can move and bounce (10px,20px),10px,(5.0px/s,5.0px/s)
    '''
    def __init__(self,center_xy = (30,200),radius = 10 ,motion_vector=(1.0,0.5)):
        self.xy = center_xy
        self.radius = radius
        self.radius_squared = radius * radius
        self.color = "orange"
        
        self.tics = 0
        self.last_move_1_or_more = (0,0)
        self.mv = motion_vector # px/s x , px/s y
        self.timer_interval = 20.0
        self.tic_freq = self.timer_interval / 1000.0
        self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
        
        if self.d_per_tic[0] == 0.0:
            move_freq_x =  999999
        else:
            move_freq_x = abs(1.0 / self.d_per_tic[0])
            
        if self.d_per_tic[1] == 0.0:
            move_freq_y = 999999
        else:
            move_freq_y = abs(1.0 / self.d_per_tic[1])
        self.move_freq = (move_freq_x,move_freq_y)
        
        self.timer = simplegui.create_timer(int(self.timer_interval),self.tic)
        self.timer.start()
        
        self.last_hit = -1
        
        self.walls = []
        
    def get_top(self):
        return ( self.xy[0], self.xy[1] - self.radius)
        
    def get_bottom(self):
        return ( self.xy[0], self.xy[1] + self.radius)
    
    def get_left(self):
        return ( self.xy[0] - self.radius, self.xy[1])
    
    def get_right(self):
        return ( self.xy[0] + self.radius, self.xy[1])
    
    def is_moving_down(self):
        return ( self.mv[1] > 0 )
    
    def is_moving_up(self):
        return ( self.mv[1] < 0 )
    
    def is_moving_right(self):
        return ( self.mv[0] > 0 )
    
    def is_moving_left(self):
        return ( self.mv[0] < 0 )
        
    
    def tic(self):
        #print(self.mv)
        self.tics += 1
        #if ( self.tics > 30 ):
        #    return
        moved = False
        if abs(self.d_per_tic[0]) < 1.0 :
            if self.tics - self.last_move_1_or_more[0] > self.move_freq[0]:
                self.last_move_1_or_more = ( self.tics , self.last_move_1_or_more[1] )
                moved = True
                if self.is_moving_right():
                    self.xy = ( self.xy[0] + 1, self.xy[1] )
                else:
                    self.xy = ( self.xy[0] - 1, self.xy[1] )
        else:
            moved = True
            self.xy = ( self.xy[0] + int(self.d_per_tic[0]), self.xy[1] ) 

        #print(    self.d_per_tic[1]    )
        if abs(self.d_per_tic[1]) < 1.0 :
            if self.tics - self.last_move_1_or_more[1] > self.move_freq[1]:
                moved = True
                self.last_move_1_or_more = ( self.last_move_1_or_more[0] , self.tics )
                if self.is_moving_down():
                    self.xy = ( self.xy[0], self.xy[1] + 1)
                else:
                    self.xy = ( self.xy[0] , self.xy[1] - 1 )
        else:
            moved = True
            self.xy = ( self.xy[0], self.xy[1] + int(self.d_per_tic[1] ) )
       
    
        if moved:
            
            #self.tic_freq = self.timer_interval / 1000.0
           
            #print(self.d_per_tic)
            #print(self.mv)
            
            hit = False
            for w in self.walls:
                if self.is_moving_right():
                    if w.hit_test(self.get_right()):
                        hit = True
                        #print('hit moving right')
                        #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball right: ',self.get_right(), )
                        #print('self.d_per_tic:',self.d_per_tic)
                        self.xy = ( self.xy[0] - int(self.d_per_tic[0]), self.xy[1] ) 
                        self.last_hit = 0
                        self.mv = ( -1.0 * self.mv[0] , self.mv[1] )
                        self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])                      
                else:                        
                    if self.is_moving_left():
                        if w.hit_test(self.get_left()):
                            hit = True
                            #print('hit moving left tics: ',self.tics)
                            #p#rint('wall tl: ',w.tl, 'ball center: ',self.xy,'ball left: ',self.get_left(), )
                            #print('self.d_per_tic:',self.d_per_tic)
                            self.xy = ( self.xy[0] - int(self.d_per_tic[0]), self.xy[1] ) 
                            self.last_hit = 1
                            self.mv = ( -1.0 * self.mv[0]  , self.mv[1] )
                            self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                    
                if ( not hit ):
                        if self.is_moving_down():
                            if w.hit_test(self.get_bottom()):
                                hit = True
                                #print('hit moving down tics: ',self.tics)
                                #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball bottom: ',self.get_bottom(), )                    
                                self.xy = ( self.xy[0], self.xy[1] - int(self.d_per_tic[1] ) )
                                self.last_hit = 2
                                self.mv = ( self.mv[0] , -1.0 * self.mv[1]  )
                                self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                        else:        
                            if self.is_moving_up():
                                if w.hit_test(self.get_top()):
                                    hit = True
                                    #print('hit moving up tics: ', self.tics)
                                    #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball top: ',self.get_top(), )
                                    self.xy = ( self.xy[0], self.xy[1] - int(self.d_per_tic[1] ) )
                                    self.last_hit = 3
                                    self.mv = ( self.mv[0] , -1.0 * self.mv[1]  )
                                    self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                                    
                if ( hit ) :
                    #print(self.d_per_tic, self.mv)
                    return
                        
            '''
        
    if npixels per tick < 1 :
        if current_tick - last_move_1_or_more > move_freq = abs(1 / npixels per tick):
            move 1
            last_move_1_or_more = current_tick
    else
        move npixels per tick
           '''
        
class Paddle(Rectangle):
    
    def __init__(self,top_left,bottom_right,motion_vector=(0.0,0.0)):
        self.tl = top_left
        self.br = bottom_right
        self.color = "white"
        self.nhits = 0
    
        self.up_key = simplegui.KEY_MAP["up"]
        self.down_key = simplegui.KEY_MAP["down"]
        
        self.tics = 0
        self.last_move_1_or_more = (0,0)
        self.mv = motion_vector # px/s x , px/s y
        self.timer_interval = 20.0
        self.tic_freq = self.timer_interval / 1000.0
        self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
        
        if self.d_per_tic[0] == 0.0:
            move_freq_x =  999999
        else:
            move_freq_x = abs(1.0 / self.d_per_tic[0])
            
        if self.d_per_tic[1] == 0.0:
            move_freq_y = 999999
        else:
            move_freq_y = abs(1.0 / self.d_per_tic[1])
        self.move_freq = (move_freq_x,move_freq_y)
        
        
        
        self.timer = simplegui.create_timer(int(self.timer_interval),self.tic)
        self.timer.start()
        
        
        self.last_hit = -1
        
        self.walls = []
    
    # should be a line but will settle for a point for now
    def get_top(self):
        return self.tl
        
    def get_bottom(self):
        return self.br
    
    def get_left(self):
        return self.tl
    
    def get_right(self):
        return self.br
    
    def is_moving_down(self):
        return ( self.mv[1] > 0 )
    
    def is_moving_up(self):
        return ( self.mv[1] < 0 )
    
    def is_moving_right(self):
        return ( self.mv[0] > 0 )
    
    def is_moving_left(self):
        return ( self.mv[0] < 0 )
    
    def accel_y(self,a):
        self.mv = ( self.mv[0], self.mv[1] + a )
        self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1]) 
        if self.d_per_tic[1] == 0.0:
            move_freq_y = 999999
        else:
            move_freq_y = abs(1.0 / self.d_per_tic[1])
        self.move_freq = (self.move_freq[0],move_freq_y)
        
    def stop(self) :
        self.mv = ( 0.0, 0.0  )
        self.d_per_tic = ( 0.0,0.0)
        self.move_freq = ( 999999, 999999 )
        
    def accel_up(self):
        #print('paddle accel up')
        
        if self.is_moving_down():
            self.stop()
        else:
            self.accel_y(-13.3)
       
    
    def accel_down(self):
        #print('paddle accell down')
        if ( self.is_moving_up() ):
            self.stop()         
        else:
            self.accel_y(13.3)
        
    
    def tic(self):
        #print(self.mv)
        self.tics += 1
        #if ( self.tics > 30 ):
        #    return
        moved = False
        if abs(self.d_per_tic[0]) < 1.0 :
            if self.tics - self.last_move_1_or_more[0] > self.move_freq[0]:
                self.last_move_1_or_more = ( self.tics , self.last_move_1_or_more[1] )
                moved = True
                if self.is_moving_right():
                    self.tl = ( self.tl[0] + 1, self.tl[1] )
                    self.br = ( self.br[0] + 1, self.br[1] )
                else:
                    self.tl = ( self.tl[0] - 1, self.tl[1] )
                    self.br = ( self.br[0] - 1, self.br[1] )
        else:
            moved = True
            self.tl = ( self.tl[0] + int(self.d_per_tic[0]), self.tl[1] )
            # could use get_widht and height from tl before last line and added
            # or we can do this
            self.br = ( self.br[0] + int(self.d_per_tic[0]), self.br[1] )

        #print(    self.d_per_tic[1]    )
        if abs(self.d_per_tic[1]) < 1.0 :
            if self.tics - self.last_move_1_or_more[1] > self.move_freq[1]:
                moved = True
                self.last_move_1_or_more = ( self.last_move_1_or_more[0] , self.tics )
                if self.is_moving_down():
                    #self.xy = ( self.xy[0], self.xy[1] + 1)
                    self.tl = ( self.tl[0], self.tl[1] + 1)
                    self.br = ( self.br[0], self.br[1] + 1)
                       
                else:
                    #self.xy = ( self.xy[0] , self.xy[1] - 1 )
                    self.tl = ( self.tl[0] , self.tl[1] - 1 )
                    self.br = ( self.br[0] , self.br[1] - 1)
        else:
            moved = True
            #self.xy = ( self.xy[0], self.xy[1] + int(self.d_per_tic[1] ) )
            self.tl = ( self.tl[0] , self.tl[1] + int(self.d_per_tic[1]) )
            self.br = ( self.br[0], self.br[1] + int(self.d_per_tic[1]) )        
                       
    
        if moved:
            
            #self.tic_freq = self.timer_interval / 1000.0
           
            #print(self.d_per_tic)
            #print(self.mv)
            
            hit = False
            for w in self.walls:
                if self.is_moving_right():
                    if w.hit_test(self.get_right()):
                        hit = True
                        #print('hit moving right')
                        #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball right: ',self.get_right(), )
                        #print('self.d_per_tic:',self.d_per_tic)
                        #self.xy = ( self.xy[0] - int(self.d_per_tic[0]), self.xy[1] ) 
                        self.tl = ( self.tl[0] - int(self.d_per_tic[0]), self.tl[1] )
                        self.br = ( self.br[0] - int(self.d_per_tic[0]), self.br[1] )
                        self.last_hit = 0
                        self.mv = ( -1.0 * self.mv[0] , self.mv[1] )
                        self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])                      
                else:                        
                    if self.is_moving_left():
                        if w.hit_test(self.get_left()):
                            hit = True
                            #print('hit moving left tics: ',self.tics)
                            #p#rint('wall tl: ',w.tl, 'ball center: ',self.xy,'ball left: ',self.get_left(), )
                            #print('self.d_per_tic:',self.d_per_tic)
                            #self.xy = ( self.xy[0] - int(self.d_per_tic[0]), self.xy[1] )
                            self.tl = ( self.tl[0] - int(self.d_per_tic[0]), self.tl[1] )
                            self.br = ( self.br[0] - int(self.d_per_tic[0]), self.br[1] )
                            self.last_hit = 1
                            self.mv = ( -1.0 * self.mv[0]  , self.mv[1] )
                            self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                    
                if ( not hit ):
                        if self.is_moving_down():
                            if w.hit_test(self.get_bottom()):
                                hit = True
                                #print('hit moving down tics: ',self.tics)
                                #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball bottom: ',self.get_bottom(), )                    
                                #self.xy = ( self.xy[0], self.xy[1] - int(self.d_per_tic[1] ) )
                                self.tl = ( self.tl[0], self.tl[1] - int(self.d_per_tic[1] ) )
                                self.br = ( self.br[0], self.br[1] - int(self.d_per_tic[1] ) )
                                self.last_hit = 2
                                self.mv = ( self.mv[0] , -1.0 * self.mv[1]  )
                                self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                        else:        
                            if self.is_moving_up():
                                if w.hit_test(self.get_top()):
                                    hit = True
                                    #print('hit moving up tics: ', self.tics)
                                    #print('wall tl: ',w.tl, 'ball center: ',self.xy,'ball top: ',self.get_top(), )
                                    #print('self.d_per_tic[1]: ', self.d_per_tic[1])
                                    #self.xy = ( self.xy[0], self.xy[1] - int(self.d_per_tic[1] ) )
                                    
                                    self.tl = ( self.tl[0] , self.tl[1] + int(self.d_per_tic[1] ) )
                                    self.br = ( self.br[0], self.br[1] + int(self.d_per_tic[1] ) )
                                    self.last_hit = 3
                                    self.mv = ( self.mv[0] , -1.0 * self.mv[1]  )
                                    self.d_per_tic = (self.tic_freq * self.mv[0],self.tic_freq * self.mv[1])
                                    
                if ( hit ) :
                    #print(self.d_per_tic, self.mv)
                    return
                        
    
        
class Scene:
    pass
'''
zorder so dragging item is on top
collection of drawable items 

'''
    
    
class App:
    
    def draw(self,c):
        # canvas.draw_text('A', (20, 20), 12, 'Red')
        c.draw_text(str(self.arectangle2.nhits),(22,18),10,'silver')
        c.draw_text(str(self.arectangle.nhits),(290,18),10,'silver')
        self.acircle.draw(c)
        self.arectangle.draw(c)
        self.arectangle1.draw(c)
        self.arectangle2.draw(c)
        self.arectangle3.draw(c)
        
        self.apoint.draw(c)
        self.bpoint.draw(c)
        self.cpoint.draw(c)
        self.aball.draw(c)
        self.ab2.draw(c)
        self.apaddle.draw(c)
        self.bpaddle.draw(c)
        
        self.atri.draw(c)
        
    
    def mouse_click_handler(self,xy):
        #print('mouse click handler')
        if self.drag_manager.currently_dragging:
            #print('calling release')
            self.drag_manager.release_at(xy)
            self.drag_manager.currently_dragging = False
       
       
    
    def mouse_drag_handler(self,xy):
        if not self.drag_manager.currently_dragging:
            self.drag_manager.check_for_hit(xy)
        else:
            self.drag_manager.drag_hit_items(xy)
            
    def key_down(self,k):
        #print(k)
        if k == 38:
            self.bpaddle.accel_up()
            return
        if k == 40:
            self.bpaddle.accel_down()
            return
        if k == 87:
            self.apaddle.accel_up()
            return
        if k == 83:
            self.apaddle.accel_down()
            return
    
    def __init__(self):
        self.drag_manager = DragManager()
        
        self.apoint = Point((10,110))
        self.drag_manager.add_dragable_item(self.apoint)
        
        
        self.bpoint = Point((30,110))
        self.drag_manager.add_dragable_item(self.bpoint)
       
        self.cpoint = Point((50,110))
        self.drag_manager.add_dragable_item(self.cpoint)
               
        self.arectangle = Rectangle((20,20),(40,220))    # a square is a rectangle smh
        #self.drag_manager.add_dragable_item(self.arectangle)
        self.arectangle1 = Rectangle((40,200),(300,220))
        self.arectangle2 = Rectangle((280,20),(300,220))
        self.arectangle3 = Rectangle((20,20),(300,40))
        
        self.acircle = Circle((100,300),50)
        self.drag_manager.add_dragable_item(self.acircle)
        
        self.aball = Ball()
        #self.drag_manager.add_dragable_item(self.aball)
        #self.aball.walls.append(self.arectangle)
        
        self.apaddle = Paddle((45,41),(55,91))
        self.apaddle.walls.append(self.arectangle1)
        self.apaddle.walls.append(self.arectangle3)
       
        self.bpaddle = Paddle((265,41),(275,91))
        self.bpaddle.walls.append(self.arectangle1)
        self.bpaddle.walls.append(self.arectangle3)
        
        
        self.ab2 = Ball((43,151),5,(-100.0,55.0))
        self.ab2.color = "purple"
        self.ab2.walls.append(self.arectangle)
        self.ab2.walls.append(self.arectangle1)
        self.ab2.walls.append(self.arectangle2)
        self.ab2.walls.append(self.arectangle3)	
        self.ab2.walls.append(self.apaddle)
        self.ab2.walls.append(self.bpaddle)
        
        self.drag_manager.add_dragable_item(self.bpaddle)
        self.drag_manager.add_dragable_item(self.apaddle)
        self.drag_manager.add_dragable_item(self.ab2)
        
        self.atri = Triangle((25,200),(40,240),(60,150))
        self.drag_manager.add_dragable_item(self.atri)
        
        self.frame = simplegui.create_frame('Testing', 400, 400)
       
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.mouse_click_handler)
        self.frame.set_mousedrag_handler(self.mouse_drag_handler)
        
        self.frame.set_keydown_handler(self.key_down)
        
        self.frame.start()
        
   
        
a = App()

