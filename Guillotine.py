import typing
from typing import NamedTuple

class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height

def read_input(file_path):
    with open(file_path) as f:
        rect_count, truck_count = map(int, f.readline().split())
        rects, trucks = list(), list()

        for _ in range(rect_count):
            rects.append(tuple(map(int, f.readline().split())))

        for _ in range(truck_count):
            trucks.append(tuple(map(int, f.readline().split())))

    return rect_count, truck_count, rects, trucks

#--------------------------------- SUPPORT FUNCTIONS --------------------------------------- 
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

#-------------------------------------- GUILLOTINE MAIN -------------------------------------
def guillotine(rect_count, truck_count, rects, trucks):
    free_rects = [FreeRectangle]






if __name__ == '__main__':
    
    file_path = './optimization-project-main/files/generated_data/0950.txt'

    #limit the time taken per iteration to reduce runtime at the cost of maybe skipped a better optimized solution
    GLOBAL_TIME_LIMIT_PER_ITER = 0.1

    rect_count, truck_count, rects, trucks = read_input(file_path)

    # rects: sort them by area in descending order
    rects.sort(key=area, reverse=True)

    # trucks: sort them by fee per area in ascending order
    trucks.sort(key=fee_per_area)

    rect_in_truck_no= [0 for _ in range(rect_count)]