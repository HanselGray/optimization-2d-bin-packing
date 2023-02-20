import typing
from typing import Tuple,NamedTuple

#-------------------------------- ITEM CLASS --------------------------------------
class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height

class Item(typing.NamedTuple('Item', [('width', int), ('height', int), ('x', int), ('y', int), ('rotation',bool)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


#--------------------------------- MISC --------------------------------------- 
def read_input(file_path):
    with open(file_path) as f:
        rect_count, truck_count = map(int, f.readline().split())
        rects, trucks = list(), list()
        totalarea=0
        for _ in range(rect_count):
            width,height=map(int, f.readline().split())
            rects.append(Item(width,height,0,0,False))
            totalarea+=width*height

        for _ in range(truck_count):
            width,height,cost=map(int, f.readline().split())
            trucks.append(tuple(width,height,cost))

    return rect_count, truck_count, rects, trucks, totalarea

def fee_per_area(truck):
    '''return fee per area of the truck'''
    return truck[2] / (truck[0]*truck[1])

def area(rect:tuple):
    return rect[0]*rect[1]

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

def scoreBAF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Area Fit """
    return rect.area-item.area, min(rect.width-item.width, rect.height-item.height)
        

def scoreBSSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Shortside Fit """
    return min(rect.width-item.width, rect.height-item.height), max(rect.width-item.width, rect.height-item.height)


def scoreBLSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Longside Fit """
    return max(rect.width-item.width, rect.height-item.height), min(rect.width-item.width, rect.height-item.height)


def scoreWAF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Area Fit """
    return (0 - (rect.area-item.area)), (0 - min(rect.width-item.width, rect.height-item.height))
        

def scoreWSSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Shortside Fit """
    return (0 - min(rect.width-item.width, rect.height-item.height)), (0 - max(rect.width-item.width, rect.height-item.height))


def scoreWLSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Longside Fit """
    return (0 - max(rect.width-item.width, rect.height-item.height)), (0 - min(rect.width-item.width, rect.height-item.height))

#-------------------------------------- GUILLOTINE MAIN -------------------------------------

def item_fit(item:Item, rect:FreeRectangle, rotated:bool = False):
    if (item.width <= rect.width and item.height <= rect.height):
        return True

    if rotated and (item.height <= rect.width and item.width <= rect.width):
        return True
    
    return False

def find_best_score(item, free_rects,score:str):
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
    

def split_rect(rect: FreeRectangle, item):
    free_rect_list=[FreeRectangle]

    return free_rect_list


def guillotine(rect_count, truck_count, rects, trucks,remaining_area):
    remaining_rect = rect_count
    free_rects = [FreeRectangle]
    rect_id=0 
    rect_in_truck_no=[]
    #init free_rects  list
    id = 0
    free_rects.append(FreeRectangle(trucks[id][0],trucks[id][1],0,0))
    cost = trucks[id][2]

   
    while remaining_rect>0:
        no_fit = False
        
        #find best free rect to put item in 
        _, best_rect, rotated = find_best_score(rects[rect_id],free_rects)
        if best_rect == None: no_fit=True
        rect_in_truck_no.append((rect_id,id))
        #performing a free rect cut
        split_rect(best_rect, rects[rect_id])
        
        rect_id+=1
        
        #add new bin if cannot fit the rect 
        if no_fit == True:
            cost+=trucks[id][2]
            id += 1 
            free_rects.append(FreeRectangle(trucks[id][0],trucks[id][1],0,0))
            continue
        
        remaining_rect-=1
    
    print("TRUCKS USED: ",id)
    print("COST NEEDED TO PACK: ",cost)
            

if __name__ == '__main__':
    
    file_path = './optimization-project-main/files/generated_data/0950.txt'

    #limit the time taken per iteration to reduce runtime at the cost of maybe skipped a better optimized solution
    GLOBAL_TIME_LIMIT_PER_ITER = 0.1

    rect_count, truck_count, rects, trucks, remaining_area = read_input(file_path)

    # rects: sort them by area in descending order
    rects.sort(key=area, reverse=True)

    # trucks: sort them by fee per area in ascending order
    trucks.sort(key=fee_per_area)

    guillotine(rect_count,truck_count,rects,trucks,remaining_area)