
import typing
from functools import reduce
from collections import namedtuple
from sortedcontainers import SortedListWithKey 


#-------------------------------- ITEM CLASS --------------------------------------
class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height

class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, width, height,
                 CornerPoint: tuple = (0, 0),
                 rotation: bool = True) -> None:
        self.width = width
        self.height = height
        self.x = CornerPoint[0]
        self.y = CornerPoint[1]
        self.area = self.width * self.height
        self.rotated = False
        self.id = id


    def __repr__(self):
        return 'Item(width=%r, height=%r, x=%r, y=%r)' % (self.width, self.height, self.x, self.y, self.id)


    def rotate(self) -> None:
        self.width, self.height = self.height, self.width
        self.rotated = False if self.rotated == True else True



#--------------------------------- MISC --------------------------------------- 
def read_input(file_path):
    with open(file_path) as f:
        rect_count, truck_count = map(int, f.readline().split())
        rects, trucks = list(), list()
        totalarea=0
        for _ in range(rect_count):
            width,height=map(int, f.readline().split())
            rects.append(Item(width,height))
            totalarea+=width*height

        for _ in range(truck_count):
            trucks.append(tuple(map(int, f.readline().split())))

    return rect_count, truck_count, rects, trucks, totalarea

def fee_per_area(truck):
    '''return fee per area of the truck'''
    return truck[2] / (truck[0]*truck[1])

def area(rect:Item):
    return rect.width*rect.height

def best_score_remaining_area(remaining_area, trucks):
    best_score = trucks[0][0]*trucks[0][1]-remaining_area
    best_id = 0 
    for i in range(1,len(trucks)):
        tmp= trucks[i][0]*trucks[i][1]-remaining_area
        if best_score > tmp: 
            best_id = i
            best_score = tmp
        elif best_score == tmp: 
            if trucks[i][2] > trucks[best_id][2]: best_id=i
    
    return best_id



#--------------------------------- SCORING FUNCTIONS --------------------------------------- 

def scoreBAF(rect: FreeRectangle, item: Item) :
    """ Best Area Fit """
    return rect.area-item.area, min(rect.width-item.width, rect.height-item.height)
        

def scoreBSSF(rect: FreeRectangle, item: Item) :
    """ Best Shortside Fit """
    return min(rect.width-item.width, rect.height-item.height), max(rect.width-item.width, rect.height-item.height)


def scoreBLSF(rect: FreeRectangle, item: Item) :
    """ Best Longside Fit """
    return max(rect.width-item.width, rect.height-item.height), min(rect.width-item.width, rect.height-item.height)


def scoreWAF(rect: FreeRectangle, item: Item) :
    """ Worst Area Fit """
    return (0 - (rect.area-item.area)), (0 - min(rect.width-item.width, rect.height-item.height))
        

def scoreWSSF(rect: FreeRectangle, item: Item) :
    """ Worst Shortside Fit """
    return (0 - min(rect.width-item.width, rect.height-item.height)), (0 - max(rect.width-item.width, rect.height-item.height))


def scoreWLSF(rect: FreeRectangle, item: Item) :
    """ Worst Longside Fit """
    return (0 - max(rect.width-item.width, rect.height-item.height)), (0 - min(rect.width-item.width, rect.height-item.height))


#-------------------------------------- CHECK FITNESS -------------------------------------
def item_fit(item:Item, rect:FreeRectangle, rotation:bool = False):
    if (item.width <= rect.width and item.height <= rect.height):
        return True

    if rotation and (item.height <= rect.width and item.width <= rect.height):
        return True
    
    return False

#-------------------------------------- FINDING BEST SCORE TO PACK -------------------------------------
def find_best_score(item:Item, free_rects,score:str):
    rects=[]
    if score == "BAF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreBAF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreBAF(rect, item), rect, True))

    elif score == "BSSF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreBSSF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreBSSF(rect, item), rect, True))

    elif score == "BLSF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreBLSF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreBLSF(rect, item), rect, True))

    elif score == "WAF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreWAF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreWAF(rect, item), rect, True))

    elif score == "WSSF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreWSSF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreWSSF(rect, item), rect, True))

    elif score == "WLSF":
        for rect in free_rects:
            if item_fit(item, rect):
                rects.append((scoreWLSF(rect, item), rect, False))
            if item_fit(item,rect,rotation =True):
                rects.append((scoreWLSF(rect, item), rect, True))

    try:
        s,rect,rot = min(rects,key=lambda x:x[0])
        return s, rect, rot
    except ValueError:
        return None, None, False
    
#-------------------------------------- SPLITTING FREE RECTS -------------------------------------
def split_along_axis(rect:FreeRectangle,item:Item,split:bool):
    top_x = rect.x
    top_y = rect.y + item.height
    top_h = rect.height - item.height

    right_x = rect.x + item.width
    right_y = rect.y
    right_w = rect.width - item.width

    # horizontal split
    if split:
        top_w = rect.width
        right_h = item.height
    # vertical split
    else:
        top_w = item.width
        right_h = rect.height

    result = []

    if right_w > 0 and right_h > 0:
        right_rect = FreeRectangle(right_w, right_h, right_x, right_y)
        result.append(right_rect)

    if top_w > 0 and top_h > 0:
        top_rect = FreeRectangle(top_w, top_h, top_x, top_y)
        result.append(top_rect)

    return result


def split_rect(rect: FreeRectangle, item:Item, rotated:bool = False):
    if rotated: item.rotate()

    #edit this for different spliting heuristic
    split_heuristic = 'default'

    #LEFTOVER LENGTHS
    w = rect.width - item.width
    h = rect.height - item.height

    if split_heuristic == 'SplitShorterLeftoverAxis': split = (w <= h)
    elif split_heuristic == 'SplitLongerLeftoverAxis': split = (w > h)
    elif split_heuristic == 'SplitMinimizeArea': split = (item.width * h > w * item.height)
    elif split_heuristic == 'SplitMaximizeArea': split = (item.width * h <= w * item.height)
    elif split_heuristic == 'SplitShorterAxis': split = (rect.width <= rect.height)
    elif split_heuristic == 'SplitLongerAxis': split = (rect.width > rect.height)
    else: split = True

    return split_along_axis(rect, item, split)


#-------------------------------------- MERGING RECTS -------------------------------------


#-------------------------------------- GUILLOTINE MAIN -------------------------------------
def guillotine(rect_count, truck_count, rects, trucks,remaining_area,score:str="BAF"):
    free_rects = []
    rect_id=0 
    rect_in_truck_no=[]
    #init free_rects  list
    id = 0
    free_rects.append(FreeRectangle(trucks[id][0],trucks[id][1],0,0))
    cost = trucks[id][2]

   
    while rect_id<rect_count:
        no_fit = False

        
        #find best free rect to put item in 
        _, best_rect, rotated = find_best_score(rects[rect_id],free_rects,score="BAF")
        #performing a free rect cut
        free_rects+=split_rect(best_rect, rects[rect_id],rotated)

        #check if there's no free rects suitable to pack the current item
        if best_rect == None: no_fit=True

        #debug
        print("BEST_RECT_IS:", best_rect)
        print("LIST OF FREE RECTS at step:", rect_id)
        for rect in free_rects: print(rect)

        free_rects.remove(best_rect)
        
        print()
        print()

        print("LIST OF FREE RECTS AT STEP (%r) after remove best_rect: " % (rect_id) )
        for rect in free_rects: print(rect)

        print()
        print()

        #keeping track of which bin is containing which item
        rect_in_truck_no.append((rect_id,id))   
        rect_id+=1
        
        #add new bin if cannot fit the rect 
        if no_fit == True:
            cost+=trucks[id][2]
            id += 1 
            free_rects.append(FreeRectangle(trucks[id][0],trucks[id][1],0,0))
            continue
    
    id+=1
    print("TRUCKS USED: ",id)
    print("COST NEEDED TO PACK: ",cost)
            

if __name__ == '__main__':
    
    file_path = './generated_data/0006.txt'

    #limit the time taken per iteration to reduce runtime at the cost of maybe skipped a better optimized solution
    GLOBAL_TIME_LIMIT_PER_ITER = 0.1

    rect_count, truck_count, rects, trucks, total_area = read_input(file_path)

    # rects: sort them by area in descending order
    rects.sort(key=area, reverse=True)

    # trucks: sort them by fee per area in ascending order
    trucks.sort(key=fee_per_area)

    print("list of rects")
    guillotine(rect_count,truck_count,rects,trucks,total_area)