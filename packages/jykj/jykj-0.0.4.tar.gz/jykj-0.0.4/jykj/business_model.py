import cv2
import sys
import jieba
import joblib
import numpy as np
from typing import Union
import math
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter

reading_list = [[0, 0.5],
                [0.5, 1], 
                [1, 1.5],
                [1.5, 2],
                [2, 2.5]]
scale_list = ["0", "0.5", "1", "1.5", "2", "2.5"]
index_buffer = {"0": [], "0.5": [], "1": [], "1.5": [], "2": [], "2.5": []} # 每半秒更新一下识别模型检测的数字，用这个buffer预防识别模型的抖动


def rela_to_abs(coords: list, resolution: list) -> np.array:
    '''
    相对坐标转换为绝对坐标。

    参数:
        coords (list): [center_x, center_y, width, height]

        resolution (list):  [width, height]
    
    返回:
        Union[np.array, list]: 绝对坐标
    '''
    w, h = resolution
    coords = np.array(coords)
    if coords.shape == (2,):
        coords[0]*=w
        coords[1]*= h
    elif coords.shape == (4,):
        coords[::2] *= w
        coords[1::2] *= h
    elif coords.dtype == float:
        coords[:, ::2] *= w
        coords[:, 1::2] *= h
    return coords.astype(int).tolist()


def rela_to_abs_batch(coords: list, resolution: list) -> np.array:
    '''
    相对坐标转换为绝对坐标。

    参数:
        coords (list): [center_x, center_y, width, height]

        resolution (list):  [width, height]
    
    返回:
        Union[np.array, list]: 绝对坐标
    '''
    coords = np.array(coords)
    if coords.dtype == float:
        w, h = resolution
        coords[:, ::2] *= w
        coords[:, 1::2] *= h
    return coords.astype(int).tolist()


def pnpoly(verts: list, testx: int, testy: int) -> bool:
    '''
    判断点是否在多边形内部, PNPoly算法。

    参数:
        verts (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

        testx (int): 点的x坐标, 例如123

        testy (int): 点的y坐标, 例如234

    返回:
        True: 点在多边形内

        False: 点不在多边形内
    '''

    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]
    nvert = len(verts)
    c = False
    j = nvert - 1
    for i in range(nvert):
        if ((verty[i] > testy) !=
            (verty[j] > testy)) and (testx < (vertx[j] - vertx[i]) *
                                     (testy - verty[i]) /
                                     (verty[j] - verty[i]) + vertx[i]):
            c = not c
        j = i
    return c


def persons_in_areas(persons_coords: list,
                     areas: list,
                     resolution: list = [],
                     h_offset: float = 0,
                     w_thresh: float = -1,
                     h_thresh: float = -1) -> bool:
    '''
    判断人是否在区域内, 支持单人坐标和多人坐标, 支持单区域和多区域, 支持过滤人检测框的宽度和高度, 支持人的位置偏移。
    坐标可以使用相对坐标或绝对坐标, 人和区域的坐标类型不一致时必须指定分辨率。使用过滤高度、宽度功能且人使用绝对坐标时须指定分辨率。

    参数:
        persons_coords (list): 单人[cx, cy, w, h], 多人[[cx1, cy1, w1, h1],[cx2, cy2, w2, h2],...]

        area (list): 单区域[[x1, y1], [x2, y2], [x3, y3]], 多区域[[[x1, y1], [x2, y2], [x3, y3]], [[x4, y4], [x5, y5], [x6, y6], [x7, 7]], ...]

        resolution (list): 视频分辨率, [width, height] 

        h_offset (float): 人的位置纵向偏移量, -0.5 <= h_thresh <= 0.5

        w_thresh (float): 检测框宽度过滤阈值, 0 <= w_thresh <= 1

        h_thresh (flost): 检测框高度过滤阈值, 0 <= h_thresh <= 1

    返回:
        True: 有人在区域内

        False: 无人在区域内
    '''

    # 全部转换为多人和多区域
    assert np.array(persons_coords).ndim in [1, 2]
    assert np.array(areas).ndim in [2, 3]
    if np.array(persons_coords).ndim == 1:
        persons_coords = [persons_coords]
    if np.array(areas).ndim == 2:
        areas = [areas]

    assert -0.5 <= h_offset <= 0.5

    # 判断是相对坐标还是绝对坐标(不严格)
    abs_person = True if np.array(persons_coords).dtype == int else False
    abs_area = True if np.array(areas[0]).dtype == int else False

    if abs_person != abs_area and not resolution:
        raise ValueError("未指定视频分辨率")

    # 如果坐标类型不一致就全部转为绝对坐标
    if abs_person == True and abs_area == False:
        for area in areas:
            area = rela_to_abs_batch(area, resolution)
    elif abs_person == False and abs_area == True:
        persons_coords = rela_to_abs_batch(persons_coords, resolution)

    # 宽度过滤
    if w_thresh != -1:
        assert 0 < w_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                w_thresh = int(w_thresh * resolution[0])
        persons_coords = [p for p in persons_coords if p[2] <= w_thresh]

    # 高度过滤
    if h_thresh != -1:
        assert 0 < h_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                h_thresh = int(h_thresh * resolution[1])
        persons_coords = [p for p in persons_coords if p[3] <= h_thresh]

    for p in persons_coords:
        cx = p[0]
        cy = p[1] + int(h_offset * p[3])
        for area in areas:
            if pnpoly(area, cx, cy):
                return True
    return False


def compute_polygon_area(x: list, y: list) -> float:
    '''
    计算多边形面积

    参数：
        x(list):[x1,x2,...,xn]
        y(list):[y1,y2,...,yn]

    返回：
        float :多边形面积

    '''

    point_num = len(x)
    if (point_num < 3): return 0.0

    s = y[0] * (x[point_num - 1] - x[1])
    for i in range(1, point_num):
        s += y[i] * (x[i - 1] - x[(i + 1) % point_num])
    return abs(s / 2.0)


def mean_fliter(x: list, y: list, step: int) -> (list, list):
    '''
    自定义均值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.mean(result_x, axis=1)
    result_y = np.mean(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def mid_filter(x: list, y: list, step: int) -> (list, list):
    '''
    自定义中值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.median(result_x, axis=1)
    result_y = np.median(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def get_scan_area(basis_x: list, basis_y: list, cur_x: list, cur_y: list,
                  step: int) -> float:
    '''
    计算当坐标和基础坐标构成多边形面积

    参数：
        basis_x(list):基础x坐标[x1,x2,x3,.....,xn]

        basis_y(list):基础y坐标[y1,y2,y3,.....,yn]

        cur_x(list): 当前x坐标[x1,x2,x3,.....,xn]

        cur_y(list): 当前y坐标[y1,y2,y3,.....,yn]
    返回：
        result(float):两次激光点云构成多边形的面积
    '''
    basis_x, basis_y = mean_fliter(basis_x, basis_y, step=step)
    basis_x = list(reversed(basis_x))
    basis_y = list(reversed(basis_y))

    cur_x, cur_y = mean_fliter(cur_x, cur_y, step)
    cur_x += basis_x
    cur_y += basis_y
    return compute_polygon_area(cur_x, cur_y)


def get_IOU(gt_box: Union[list, tuple], b_box: Union[list, tuple]) -> float:
    '''
        计算两个矩形区域的IOU

        参数：
            gt_box (list) : 真实区域坐标 [100,100,500,500] ,shape: [1,4]

            b_box (list) : 目标区域坐标 [150,150,400,400] ,shape: [1,4]

        返回：
            两个框的重叠程度(IOU)
    '''
    assert len(gt_box) == 4 and len(b_box) == 4, '请输入正确的坐标'
    gt_box = [int(i) for i in gt_box]
    b_box = [int(i) for i in b_box]

    width0 = gt_box[2] - gt_box[0]
    height0 = gt_box[3] - gt_box[1]
    width1 = b_box[2] - b_box[0]
    height1 = b_box[3] - b_box[1]
    max_x = max(gt_box[2], b_box[2])
    min_x = min(gt_box[0], b_box[0])
    width = width0 + width1 - (max_x - min_x)
    max_y = max(gt_box[3], b_box[3])
    min_y = min(gt_box[1], b_box[1])
    height = height0 + height1 - (max_y - min_y)

    interArea = width * height
    boxAArea = width0 * height0
    boxBArea = width1 * height1
    iou = interArea / (boxAArea + boxBArea - interArea)

    return iou


def compute_density(target_area: Union[list, tuple],
                    coords: Union[list, tuple]) -> (int, float):
    '''
        输入一个目标区域，一组目标坐标，计算目标数量、密度

        参数：
            target_area (list) : [[129,89],[342,68],[397,206],[340,373],[87,268]] ,shape : [n,2]

            coords (list) : [[[左上x，左上y],[右下x,右下y]]]   [[[0,0],[500,500]],[[700,700],[400,400]], [[0,0],[100,100]],[[200,200],[300,300]]] ,shape : [3,n,2]

        返回：
            return (int、float) : 目标在区域中的数量、密度
    '''
    assert len(coords) != 0, '目标数量不能为0'
    assert np.array(target_area).shape[0] > 2, '区域坐标不能少于2'
    assert len(np.array(coords).shape) >= 3, '请输入正确目标坐标'
    assert np.array(coords).shape[1] >= 2 and np.array(
        coords).shape[2] == 2, '请输入正确区域坐标'
    number = len(coords)
    if type(coords) == list:
        coords = np.array(coords)
    minx = np.min(coords[:, :, 0])
    miny = np.min(coords[:, :, 1])
    maxx = np.max(coords[:, :, 0])
    maxy = np.max(coords[:, :, 1])
    p1, p2 = ((minx, miny, maxx, maxy)), (target_area[0][0], target_area[0][1],
                                          target_area[2][0], target_area[2][1])
    iou = get_IOU(p1, p2)
    # print(iou)
    density = iou / number
    return number, float(density)


def __sst(y_no_fitting: list) -> float:
    '''
        计算SST(total sum of squares) 总平方和

        参数：

           y_no_predicted: 待拟合的y

        返回：

           总平方和SST
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_no_fitting]
    sst = sum(s_list)
    return sst


def __ssr(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSR(regression sum of squares) 回归平方和

        参数：

            y_fitting: 拟合好的y值

            y_no_fitting: 待拟合y值

        返回:

            回归平方和SSR
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_fitting]
    ssr = sum(s_list)
    return ssr


def __sse(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSE(error sum of squares) 残差平方和

        参数：

            y_fitting:  拟合好的y值

            y_no_fitting: 待拟合y值

        返回：

            残差平方和SSE
    '''
    s_list = [(y_fitting[i] - y_no_fitting[i])**2 for i in range(len(y_fitting))]
    sse = sum(s_list)
    return sse


def goodness_of_fit(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算拟合优度R^2
        
        参数：

             y_fitting: 拟合好的y值

             y_no_fitting: 待拟合y值

        返回:

            拟合优度R^2
    '''
    SSR = __ssr(y_fitting, y_no_fitting)
    SST = __sst(y_no_fitting)
    rr = SSR /SST
    return rr


def fit_line(x_: list,y_: list) -> (float, float):
    '''
        最小二乘法拟合点集为直线
           参数：
              x_ : 拟合好的y值
              y_ : 待拟合y值
           返回:
              k: 直线斜率
              b: 直线偏移
        '''
    k,b = np.polyfit(x_,y_,1)
    k,b = round(k,3),round(b,3)
    return k,b


def pd(centers: list,thr: float) -> int:
    '''
        是否排队  根据多个目标中心点拟合直线，根据r2阈值判断是否排队

        参数：

            centers (list) : [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]]

            thr (float) : 取值范围0~1，越接近1，表示拟合效果越好

        返回：

            return (int) :0 不排队 、1 排队
    '''

    cen = np.array(centers)
    x_ = np.array(cen[:, 0])
    y_ = np.array(cen[:, 1])
    k,b = fit_line(x_, y_)
    y_fit = k*x_+b
    if (goodness_of_fit(y_fit,y_)>thr):
        return 1
    return 0





def update_index_buffer(key: str,
                        value: tuple) -> None:
    """
    向buffer里存放bbox中心点的坐标, buffer 的长度是10帧,目的是防止识别模型检测的抖动现象。

    参数：
        key: key
        value: value

    返回：
        None
    """
    if len(index_buffer[key]) < 10:
        index_buffer[key].append(value)
    else:
        index_buffer[key].pop(0)
        index_buffer[key].append(value)


def segment_detect(gray: np.ndarray) -> tuple:
    """
    利用霍夫曼直线检测原理，检测指针的直线特征

    参数：
        gray (ndarray): 指针的patch

    返回：
        4darray: 线段的起止点坐标
    """
    minValue = 50
    maxValue = 70
    SobelKernel = 3
    minLineLength = 50 # height/32
    maxLineGap = 10 # height/40

    edges = cv2.Canny(gray, minValue, maxValue, apertureSize=SobelKernel)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=minLineLength, maxLineGap=maxLineGap)
    return lines[0]


def line_segment_inter(line: tuple, segment: tuple) -> tuple:
    """
    根据直线的斜截距方程,求直线和线段的交点

    参数：
        line (tuple): x0, y0, x1, y1
        segment (tuple): xs, ys, xe, ye
    
    返回：
        tuple: x, y
    """
    x0, y0, x1, y1 = np.squeeze(line)
    xa, ya, xb, yb = segment
    k_line = (y0 - y1) / (x0 - x1 + 1e-6)
    b_line = y0 - k_line * x0
    delta_ya = k_line * (xa - x0) + y0 - ya
    delta_yb = k_line * (xb - x0) + y0 - yb
    if delta_ya == 0:
        return xa, ya
    if delta_yb == 0:
        return xb, yb
    
    if delta_ya * delta_yb > 0:
        return -1, -1
    else:
        k_segment = (ya - yb) / (xa - xb + 1e-6)
        b_segment = ya - k_segment * xa
        x_inter = (b_segment - b_line) / (k_line - k_segment + 1e-6)
        y_inter = k_line * x_inter + b_line
        return x_inter, y_inter


def show_reading(seg: tuple,
                inter: tuple,
                index: int) -> float:
    """
    根据起止点的坐标,指针与起止点之间连线的交点,以及起止点所对应的刻度值,按照交点所对应的比例,还原出指针对应的读数。

    参数：
        seg (tuple or list): (start_x, start_y, end_x, end_y)
        inter (tuple): (x, y)
        index (int): int

    返回：
        reading (float): float
    """
    xs, ys, xe, ye = seg
    x0, y0 = inter
    ratio = np.linalg.norm((x0 - xs, y0 - ys)) / np.linalg.norm((xe - xs, ye - ys))
    scale_min, scale_max = reading_list[index]
    reading = scale_min + ratio * (scale_max - scale_min)
    return reading


def get_coor(obj: dict,
             img_shape: tuple) -> tuple:
    """
    将相对坐标转换成绝对坐标。

    参数：
        obj (dict): {"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": } 
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)

    返回：
        tuple: cx, cy, w, h
    """
    cx = obj['relative_coordinates']['center_x'] * img_shape[0]
    cy = obj['relative_coordinates']['center_y'] * img_shape[1]
    w = obj['relative_coordinates']['width'] * img_shape[0]
    h = obj['relative_coordinates']['height'] * img_shape[1]
    return cx, cy, w, h


def topological_reading(objects: list,
                        patch: np.ndarray,
                        img_shape: tuple) -> float:
    """
    识别仪表盘显示的读数。
    
    参数：
        objects (class list): list 里面存放了多个类,每个类里面保存了关于这个bbox的信息。[{"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": }, ...]
        patch (np.ndarray): 使用opencv读取图像后的ndarray格式。
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)
    
    返回：
        reading (float): 最终的读数
    """

    # 用来存放刻度的坐标
    bboxs = [(0, 0, 0, 0)] + [(0, 0) for i in range(6)]
    # 用来表示刻度围成的多边形区域
    reading_heatmap = []
    # 提取信息
    for obj in objects:
        if obj["name"] == "Zhizhen":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[0] = (cx, cy, w, h)

        if obj["name"] == "0":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[1] = (cx, cy)

            update_index_buffer("0", (cx, cy))

            bc_0 = (cx, int(min(cy + h/2, img_shape[1])))
            br_0 = (int(min(cx + w/2, img_shape[0])), int(min(cy + h/2, img_shape[1])))
            reading_heatmap.extend([bc_0, br_0])

        if obj["name"] == "05":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[2] = (cx, cy)

            update_index_buffer("0.5", (cx, cy))
            
            bc_05 = (cx, int(min(cy + h/2, img_shape[1])))
            reading_heatmap.append(bc_05)

        if obj["name"] == "1":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[3] = (cx, cy)

            update_index_buffer("1", (cx, cy))

            lc_1 = (int(max(0, cx - w/2)), cy)
            reading_heatmap.append(lc_1)

        if obj["name"] == "15":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[4] = (cx, cy)

            update_index_buffer("1.5", (cx, cy))

            lc_15 = (int(max(0, cx - w/2)), cy)
            reading_heatmap.append(lc_15)

        if obj["name"] == "2":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[5] = (cx, cy)
            
            update_index_buffer("2", (cx, cy))

            tc_2 = (cx, int(max(0, cy - h/2)))
            reading_heatmap.append(tc_2)

        if obj["name"] == "25":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[6] = (cx, cy)

            update_index_buffer("2.5", (cx, cy))

            tr_25 = (int(min(cx + w/2, img_shape[0])), int(max(0, cy - h/2)))
            br_25 = (int(min(cx + w/2, img_shape[0])), int(min(cy + h/2, img_shape[1])))
            reading_heatmap.extend([tr_25, br_25])

    bboxs = [int(item) for box in bboxs for item in box]

    assert bboxs[:4] != [0, 0, 0, 0], "通用模型无法检测到指针"

    # 获得指针左上角和右下角的坐标
    cx, cy, w, h = bboxs[:4]
    t, l, b, r = max(0, cx - w/2), max(0, cy - h/2), min(img_shape[0], cx + w/2), min(img_shape[1], cy + h/2)
    t, l, b, r = [int(item) for item in [t, l, b, r]]
    # 霍夫曼直线检测
    line = segment_detect(patch)
    tl = np.array([t, l, t, l])
    # 将patch坐标转成图像坐标
    line = line + tl
    # 用来存放数字区域的中心位置
    scales = [(0, 0) for _ in range(6)]
    for index, item in enumerate(scale_list):
        scales[index] = np.mean(np.array(index_buffer[item]), axis=0)
    # 计算指针与读数片段的交点
    nums = len(scales)
    keep_inter = []
    keep_reading = []
    for i in range(nums - 1):
        if np.max(scales[i]) != 0 and np.max(scales[i+1]) != 0:
            seg = (scales[i][0], scales[i][1], scales[i+1][0], scales[i+1][1])
            inter_point = line_segment_inter(line, seg)
            if inter_point != (-1, -1):
                reading = show_reading(seg, inter_point, i)
                keep_inter.append(inter_point)
                keep_reading.append(reading)
        else:
            if np.max(scales[i]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i]))
                sys.stdout.flush()
            if np.max(scales[i+1]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i+1]))
                sys.stdout.flush()
    # 过滤交点
    # 获得指针bbox四个边的中心点
    bbox_edge_center = [(cx, l),
                        (b, cy),
                        (cx, r),
                        (t, cy)]
    # 判断四个边的中点哪个不在指针读数围成的区域内，那个中点就是指针的方向
    anchor = []
    for tx, ty in bbox_edge_center:
        if not pnpoly(reading_heatmap, tx, ty):
            anchor.append((tx, ty))

    assert len(anchor) == 1, "无法获得指针的方向"

    anchor = np.array(anchor[0])
    keep_inter = np.array(keep_inter)
    dist = np.linalg.norm(anchor - keep_inter, axis=1)
    keep_index = np.argmin(dist)
    ret_reading = keep_reading[keep_index]
    return ret_reading


def move_and_cover(picture_previous:np.ndarray, picture_now: np.ndarray, shutter_th:float, move_th:float) -> int:
    """
    判断摄像头是否遮挡或移动。
    
    参数：
        picture_previous (np.ndarray): 初始帧，使用opencv读取图像后的ndarray格式；
        picture_now (np.ndarray): 当前帧，使用opencv读取图像后的ndarray格式；
        shutter_th (float): 遮挡阈值，为0-1之间的小数，可默认0.5；
        move_th (float): 移动阈值，为0-1之间的小数，可默认0.3；
    返回：
        result (int): 0为正常；1为遮挡；2为移动
    """

    def calculate(image1 : np.ndarray, image2:np.ndarray)-> float:
        """
        计算图像单通道的直方图的相似值。
        
        参数：
            image1 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            image2 (np.ndarray): 使用opencv读取图像后的ndarray格式；
        返回：
            degree (float): 两张图片单通道的相似度
        """

        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + \
                    (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree


    def classify_hist_with_split(image1:np.ndarray, image2:np.ndarray, size:tuple) -> float:
        """
        将图像resize后，分离为RGB三个通道，再计算每个通道的相似值。
        
        参数：
            image1 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            image2 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            size (tuple): resize后的宽高，默认（256，256）
        返回：
            sub_data  (float): 两张图片RGB每个通道的直方图相似度的平均
        """

        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data   

    corner = 150
    size = picture_previous.shape
    corner_list = [[0, corner, 0, corner],\
                [0, corner, size[0] - corner, size[0]],\
                [size[1] - corner, size[1], 0, corner],\
                [size[1] - corner, size[1], size[0] - corner, size[0]]]
    cropImg_previous = list()
    for i in range(0,4):
        cropImg_previous.append(picture_previous[corner_list[i][0]:corner_list[i][1], corner_list[i][2]:corner_list[i][3]])
    
    cropImg_current = list()
    for i in range(0,4):
        cropImg_current.append(picture_now[corner_list[i][0]:corner_list[i][1], corner_list[i][2]:corner_list[i][3]])
    
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
    differ_count = []
    for i in range(0, 4):
        n4 = classify_hist_with_split(cropImg_previous[i], cropImg_current[i], (256, 256))
        differ_count.append(float(n4))

    blurred = cv2.GaussianBlur(picture_now, (3, 3), 0)   
    img_gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)     
    edge_all = cv2.Canny(img_gray, 0, 20)
    edge_all_dilate = cv2.dilate(edge_all, es, iterations = 2)      
    if int(np.sum(edge_all_dilate==255))/(size[0] * size[1]) < shutter_th:  
        result = 1            
        print("遮挡")
    elif np.mean(differ_count) < move_th:  
        result = 2                      
        print("移动")
    else:
        result = 0
        print("正常")
    
    return result


def coal_quantity_grade(coal_position: list,
                        belt_left: list,
                        belt_right: list,
                        grade_list: list,
                        resolution: list) -> int:
    '''
    根据皮带左右坐标、煤炭目标检测结果、以及煤量等级列表，输出煤量等级。如皮带左右坐标和煤炭检测结果坐标系不一致，则需提供分辨率参数。
    参数：
        coal_position (list): 煤炭目标检测结果框[x, y, w, h];
        belt_left (list): 皮带左坐标[x, y];
        belt_right (list): 皮带右坐标[x, y];
        grade_list (list): 煤量等级列表[threshold1, threshold2, ...]，等级分别是0-threshold1、threshold1-threshold2、threshold2-1...;
        resolution (list): 分辨率[w, h].
    返回值：
        煤量等级值;
    '''
    # 参数检查
    if np.array(coal_position).shape != (4,) or np.array(belt_left).shape != (2,) or np.array(belt_right).shape != (2,):
        raise ValueError("参数维数有误！")
    if len(grade_list) == 0:
        raise ValueError("煤量等级列表为空序列！")
    # 判断相对/绝对坐标
    abs_coal = 0
    abs_left = 0
    abs_right = 0
    if coal_position[0] > 1 or coal_position[1] > 1 or coal_position[2] > 1 or coal_position[3] > 1:
        abs_coal = 1
    if belt_left[0] > 1 or belt_left[1] > 1:
        abs_left = 1
    if belt_right[0] > 1 or belt_right[1] > 1:
        abs_right = 1

    if abs_coal + abs_left + abs_right > 0 and abs_coal * abs_left * abs_right == 0 and len(resolution) == 0:
        raise ValueError("坐标不一致时，请提供分辨率参数！")
    if len(resolution) > 0 and np.array(resolution).shape != (2,):
        raise ValueError("分辨率格式有误！")
    if belt_left[0] > belt_right[0]:
        raise ValueError("belt_left应在belt_right左边！")
    # 统一坐标
    if abs_coal == 0:
        coal_position = rela_to_abs(coal_position, resolution)
    if abs_left == 0:
        belt_left = rela_to_abs(belt_left, resolution)
    if abs_right == 0:
        belt_right = rela_to_abs(belt_right, resolution)
    # 计算煤量等级
    width_ratio = coal_position[2] / (belt_right[0] - belt_left[0])
    coal_level = 1
    last_grade = 0
    for grade in grade_list:
        if grade <= last_grade:
            raise ValueError("煤量等级列表应为大于0的升序序列！")
        if grade >= 1:
            raise ValueError("煤量等级列表应小于1！")
        last_grade = grade
        if width_ratio >= grade:
            coal_level += 1
    return coal_level


def belt_deviation(roller_position: list,
                   belt_mid: list,
                   differrent: int,
                   resolution=None) -> int:
    '''
    根据皮带左右托辊数目判断皮带跑偏情况。
    参数：
        roller_position (list): 托辊位置[[x1, y1, w1, h1],[x2, y2, w2, h2],...];
        belt_mid (list): 皮带中线附近的任意坐标[x1, y1];
        differrent (int): 托辊左右差阈值;
        resolution (list): 分辨率[w, h].
    返回值：
        1: 右跑偏;
        -1: 做跑偏;
        0: 未跑偏;
    '''
    if resolution is None:
        resolution = [1, 1]
    if len(roller_position) == 0:
        return 0
    # 参数检查
    if len(np.array(roller_position).shape)!=2 or np.array(roller_position).shape[1]!=4 or np.array(belt_mid).shape!=(2,):
        raise ValueError("参数维数有误！")
    # 判断相对/绝对坐标
    abs_roller = 0
    abs_mid = 0
    for roller in roller_position:
        for x in roller:
            if x>=1:
                abs_roller = 1
                break
    for x in belt_mid:
        if x >= 1:
            abs_mid = 1

    if abs_roller + abs_mid > 0 and abs_roller * abs_mid == 0 and len(resolution) == 0:
        raise ValueError("坐标不一致时，请提供分辨率参数！")
    if len(resolution) > 0 and np.array(resolution).shape != (2,):
        raise ValueError("分辨率格式有误！")
    # 统一坐标
    if abs_roller == 0:
        roller_position = rela_to_abs(roller_position, resolution)
    if abs_mid == 0:
        belt_mid = rela_to_abs(belt_mid, resolution)
    #判断跑偏
    roller_left = [r for r in roller_position if r[0]<= belt_mid[0]]
    roller_right = [r for r in roller_position if r[0] > belt_mid[0]]
    if len(roller_left) - len(roller_right) >= differrent:
        return 1
    elif  len(roller_right) - len(roller_left) >= differrent:
        return -1
    else:
        return 0
    

def find_max_contour(src:np.ndarray =None ,path: str =None)->np.ndarray:
    '''
    输入一个图片或图片的路径，将图片中最大的轮廓找到并裁剪出来

    参数：
        src (np.mdarray) : 读取的图片 shape : [w,h,3]

        path (str) : 输入图像路径

    返回：
        return (np.ndarray) : 裁剪后的图片
    '''

    if src is None and path is None:
        raise '请输入图像或图片路径'
    if src is not None and path is not None:
        raise '不能同时输入图像和图片路径'
    img=None
    # x,y,w,h=None,None,None,None
    if path is not None:
        if os.path.exists(path):
            # print(str(len(img_list))+'--读取文件--')
            img = cv2.imread(path)
    if src is not None:
        img=src
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用阈值
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    thresh_inv = cv2.bitwise_not(thresh)

    # 找到所有的轮廓
    contours, hierarchy = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    area = []
    # 找到最大的轮廓
    height, width, channel = img.shape

    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    max_idx = np.argmax(np.array(area))
    max_contour=contours[max_idx]
    hull = cv2.convexHull(max_contour, returnPoints=True)
    point = np.squeeze(hull)
    new_list = sorted(point.tolist(), key=lambda x: x[0] ** 2 + x[1] ** 2)
    top_right = sorted(point.tolist(), key=lambda x: (0 - x[0]) ** 2 + (height - x[1]) ** 2)
    left_buttom = sorted(point.tolist(), key=lambda x: (width - x[0]) ** 2 + (0 - x[1]) ** 2)
    pts1 = np.float32([new_list[0], top_right[0], new_list[-1], left_buttom[0]])
    pts2 = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped


def vague_detection(src :np.ndarray,blur_threshold:int=1000)->[bool,float]:
    '''
    判断图像是否模糊

    参数：

        src (np.mdarray) : 读取的图片 shape : [w,h,3]

        blur_threshold : 模糊阈值

    返回值：

        是否模糊
        图像方差值
    
    '''
    assert src is not None,'输入图像不能为空'
    im_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    fm = cv2.Canny(im_gray, 500, 100).var()
    if fm < blur_threshold:
        return True,fm
    return False,fm


def get_points_rect_contours(points:list)->list:
	'''
	    求解点的最小外接矩形。

	    参数:
	        points (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

	    返回:
	        list: 最小外接矩形的四个顶点 [[106 178],[124 142],[200 180],[182 216]]
	    '''
	points = np.array([points], dtype=np.int32)
	rect = cv2.minAreaRect(points)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	return box


def get_points_mincircle(points:list)->tuple:
	'''
	求解点的最小外接圆。

	    参数:
	        points (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

	    返回:
	        x,y,radius(tuple): 最小外接圆的中心坐标和半径
	'''
	cnt = np.array(points)
	(x,y),radius = cv2.minEnclosingCircle(cnt)
	return tuple(int(item) for item in (x,y,radius) )


MODEL = None
TF = None
def load_model(model_path: str, tf_path: str) -> None:
    """"
    加载贝叶斯分类器的模型和权重
    参数：
        model_path (str): 贝叶斯分类器模型的路径
        tf_path (str): 贝叶斯分类器权重的路径

    返回：
        None
    """
    global MODEL 
    global TF

    MODEL = joblib.load(model_path)
    TF = joblib.load(tf_path)


def text_classification(name: str) -> str:
    """
    输入精英科技产品的系统名称，返回对应的产品线名称。

    参数：
        name (str): 精英科技产品的系统名称

    返回：
        str: 该系统对应的产品线名称
    """
    assert MODEL != None and TF != None
    
    words = jieba.cut(name)
    s = ' '.join(words)

    test_features = TF.transform([s]) 
    predicted_labels = MODEL.predict(test_features)
    predicted_probs = MODEL.predict_proba(test_features)
    label, prob = predicted_labels[0], np.max(predicted_probs)
    if prob < 0.3:
        return "该系统没有对应的产品线！"
    else:
        return name + ": " + label


def min_bbox(kpts: np.array) -> tuple:
    """
    求最小外接矩形的坐标

    参数：
        kpts (ndarray): 17个骨骼关键点的坐标

    返回：
        tuple: x1, y1, x2, y2
    """
    kpts = np.array(kpts)
    min_x, min_y = np.min(kpts, axis=0)
    max_x, max_y = np.max(kpts, axis=0)
    return min_x, min_y, max_x, max_y
    
    
def sleeping_monitor(kpts: np.array,
                     kpts_score: np.array, 
                     area: list, 
                     resolution: tuple) -> tuple:
    """
    根据人体骨骼关键点的坐标、置信度，判断人体是否在睡觉

    参数：
        kpts (np.array): 人体骨骼关键点的坐标
        kpts_score (np.array): 人体骨骼关键点的置信度
        area (2d list): 工作台区域的坐标点集合， [[x1, y1], [x2, y2], ..., [xn, yn]]
        resolution (tuple): 视频的分辨率

    返回：
        is_sleeping (bool): 是否在睡觉
        ave_angle_y (float): 视线与图像坐标系y正半轴的夹角
        ave_gaze_score (float): 视线的置信度
    """

    # 保留关键点的最低置信度
    use_kpt_threshold = 0.05
    # 关键点在列表中的位置
    kpts_map = {"nose": 0,
                "leye": 1,
                "reye": 2,
                "lear": 3,
                "rear": 4,
                "lshoulder": 5,
                "rshoulder": 6,
                "lelbow": 7,
                "relbow": 8,
                "lwrist": 9,
                "rwrist": 10,
                "lhip": 11,
                "rhip": 12,
                "lknee": 13,
                "rknee": 14,
                "lankle": 15,
                "rankle": 16}
    # 姿态角度的阈值
    gaze_angle = 30 #视线与y正半轴的夹角
    spine_angle = 30 #脊柱与x正半轴的夹角
    look_up_angle_gaze = 145 # 仰睡视线角度的阈值
    look_up_angle_spine = 120 # 仰睡脊柱角度的阈值
    big_leg_angle_diff = 25 # 大腿方向向量与x轴正半轴的夹角，小于这个阈值判定为站立
    pose_area_ratio = 0.5 # 包含pose的矩形框占图像的百分比

    # initial
    frame_w, frame_h = resolution
    is_sleeping = False 
    # 过滤掉score小于use_kpt_threshold(0.05)的keypoints
    kpts_index = np.where(kpts_score > use_kpt_threshold)[0]
    kpts_keep = np.zeros((17, 2), dtype=float)
    kpts_keep[kpts_index] = kpts[kpts_index]
    # 取出关键点
    lear_kpt, leye_kpt, rear_kpt, reye_kpt = kpts_keep[kpts_map["lear"]], kpts_keep[kpts_map["leye"]], kpts_keep[kpts_map["rear"]], kpts_keep[kpts_map["reye"]]
    ls_kpt, rs_kpt, lhip_kpt, rhip_kpt = kpts_keep[kpts_map["lshoulder"]], kpts_keep[kpts_map["rshoulder"]], kpts_keep[kpts_map["lhip"]], kpts_keep[kpts_map["rhip"]]
    lk_kpt, rk_kpt, la_kpt, ra_kpt = kpts_keep[kpts_map["lknee"]], kpts_keep[kpts_map["rknee"]], kpts_keep[kpts_map["lankle"]], kpts_keep[kpts_map["rankle"]]
    nose_kpt, lelbow_kpt, relbow_kpt = kpts_keep[kpts_map["nose"]], kpts_keep[kpts_map["lelbow"]], kpts_keep[kpts_map["relbow"]]
    lw_kpt, rw_kpt = kpts_keep[kpts_map["lwrist"]], kpts_keep[kpts_map["rwrist"]]
    ch_kpt = np.array([0, 0])
    if np.max(kpts_keep[:5, :]) != 0:
        ch_kpt = np.sum(kpts_keep[:5, :], axis=0) / np.sum(kpts_score[:5] > use_kpt_threshold)
    # 计算同侧耳朵到眼睛方向向量与y轴的夹角
    y_axis = np.array([0, 1])
    count, l_angle_y, r_angle_y, ave_angle_y, l_gaze_score, r_gaze_score, ave_gaze_score = 0, 0, 0, 90, 0, 0, 0
    if max(lear_kpt) != 0 and max(leye_kpt) != 0:
        lear_index, leye_index = 3, 1
        l_ear2eye = leye_kpt - lear_kpt
        cost = np.dot(l_ear2eye, y_axis) / (np.linalg.norm(l_ear2eye) + 1e-6)
        l_angle_y = np.arccos(cost) * 180 / np.pi
        # 计算左侧视线的置信度
        l_gaze_score = (kpts_score[lear_index] + kpts_score[leye_index]) / 2
        count += 1
    if max(rear_kpt) != 0 and max(reye_kpt) != 0:
        rear_index, reye_index = 4, 2
        r_ear2eye = reye_kpt - rear_kpt
        cost = np.dot(r_ear2eye, y_axis) / (np.linalg.norm(r_ear2eye) + 1e-6)
        r_angle_y = np.arccos(cost) * 180 / np.pi
        # 计算右侧视线的置信度
        r_gaze_score = (kpts_score[rear_index] + kpts_score[reye_index]) / 2
        count += 1
    if count != 0:
        ave_angle_y = (l_angle_y + r_angle_y) / count
        ave_gaze_score = (l_gaze_score + r_gaze_score) / count
        ave_gaze_score = ave_gaze_score[0]
    # 计算脊柱方向向量与x轴的夹角
    x_axis = np.array([1, 0])
    count, l_angle_x, r_angle_x, ave_angle_x = 0, 0, 0, 90
    if max(ls_kpt) != 0 and max(lhip_kpt) != 0:
        l_hip2s = ls_kpt - lhip_kpt  
        cost = np.dot(l_hip2s, x_axis) / (np.linalg.norm(l_hip2s) + 1e-6)
        l_angle_x = np.arccos(cost) * 180 / np.pi
        count += 1
    if max(rs_kpt) != 0 and max(rhip_kpt) != 0:
        r_hip2s = rs_kpt - rhip_kpt
        cost = np.dot(r_hip2s, x_axis) / (np.linalg.norm(r_hip2s) + 1e-6)
        r_angle_x = np.arccos(cost) * 180 / np.pi
        count += 1
    if count != 0:
        ave_angle_x = (l_angle_x + r_angle_x) / count
    # 计算大腿(膝臀向量)与x正半轴的夹角，从而判断人体是否直立
    count, l_angle_leg, r_angle_leg, ave_angle_leg = 0, 0, 0, 0
    if max(lk_kpt) != 0 and max(lhip_kpt) != 0:
        l_k2hip = lhip_kpt - lk_kpt  
        cost = np.dot(l_k2hip, x_axis) / (np.linalg.norm(l_k2hip) + 1e-6)
        l_angle_leg = np.arccos(cost) * 180 / np.pi
        count += 1
    if max(rk_kpt) != 0 and max(rhip_kpt) != 0:
        r_k2hip = rhip_kpt - rk_kpt
        cost = np.dot(r_k2hip, x_axis) / (np.linalg.norm(r_k2hip) + 1e-6)
        r_angle_leg = np.arccos(cost) * 180 / np.pi
        count += 1
    if count != 0:
        ave_angle_leg = (l_angle_leg + r_angle_leg) / count
    # 判断头部的中心点是否在工作台上
    in_area = pnpoly(area, ch_kpt[0], ch_kpt[1])
    # 综合夹角和区域分析，得出是否是睡姿的结果
    # 1.1 如果低头，脊柱的角度低于阈值，而且面部中心点在案台区域的话，判定为睡觉。
    if (abs(ave_angle_y) < gaze_angle  and abs(ave_angle_x) < spine_angle and in_area):
        is_sleeping = True
    # 1.2 如果脊柱倾斜，视线的置信度低于0.5（很有可能视线不可见是预估的），而且面部中心点在案台区域的话，判定为睡觉。
    if (abs(ave_angle_x) < spine_angle and ave_gaze_score < 0.4 and in_area):
        is_sleeping = True
    # 2.如果头往后仰卧的角度太大而且脊柱的角度也要大于阈值，判定为睡觉
    lhip_id, rhip_id = 11, 12
    ave_hip_score = (kpts_score[lhip_id] + kpts_score[rhip_id]) / 2
    # 主要用来排除臀部不可见的那种误识别现象
    ave_hip_thresh = 0.16
    if abs(ave_angle_y) > look_up_angle_gaze and (abs(ave_angle_x) > look_up_angle_spine and ave_hip_score[0] > ave_hip_thresh):
        is_sleeping = True
    # 3.如果站立的话，肯定没睡觉
    diff = np.abs(ave_angle_leg - 90)
    if diff < big_leg_angle_diff:
        is_sleeping = False
    # 4.如果人体挨着镜头太近的话应该不是在睡觉
    min_x, min_y, max_x, max_y = min_bbox(kpts[kpts_index])
    pose_area = (max_x - min_x) * (max_y - min_y)
    pose_area_ratio = pose_area / (frame_w * frame_h)
    if pose_area_ratio > pose_area_ratio:
        is_sleeping = False
    # 5.如果很确信视线正对着屏幕的话，不管脊椎的角度再怎么弯曲都不管用
    if np.abs(ave_angle_y - 90) < 25 and ave_gaze_score > 0.4:
        is_sleeping = False
    # 6. 如果脊柱的角度大于35度，且视线的角度小于30度的时候，认为人们在案台上写字（排除误识别！！）
    if (abs(ave_angle_y) < 30 and abs(ave_angle_x) > 40):
        is_sleeping = False
    # 7. 在前面6个逻辑的基础上，再加强逻辑限定人在正睡的情况(这种情况没有考虑视线的角度，因为有不准的情况，所以就采用了绝对距离的判断准则)
    dist_ear2eye = np.linalg.norm(rear_kpt - reye_kpt)
    dist_rw2re = np.linalg.norm(rw_kpt - reye_kpt)
    dist_lw2re = np.linalg.norm(lw_kpt - reye_kpt)
    if dist_rw2re < dist_ear2eye and dist_lw2re < dist_ear2eye and abs(ave_angle_x) < 50 and in_area:
        is_sleeping = True
    # 8. 在前边6个逻辑的基础上，再加强逻辑限定人在左睡的情况（这里边视线和脊椎与坐标轴的夹角就不要动了）
    l_arm_angle, l_arm_angle_diff = 0, 20
    if max(ls_kpt) != 0 and max(lelbow_kpt) != 0 and max(lw_kpt) != 0:
        l_elbow2s = ls_kpt - lelbow_kpt
        l_elbow2w = lw_kpt - lelbow_kpt
        cost = np.dot(l_elbow2s, l_elbow2w) / ((np.linalg.norm(l_elbow2s) * np.linalg.norm(l_elbow2w)) + 1e-6)
        l_arm_angle = np.arccos(cost) * 180 / np.pi
        dist_lelbow2reye = np.linalg.norm(lelbow_kpt - reye_kpt)
        l_elbow_in_area = pnpoly(area, lelbow_kpt[0], lelbow_kpt[1])
        l_wrist_in_area = pnpoly(area, lw_kpt[0], lw_kpt[1])
        if abs(l_arm_angle - 180) < l_arm_angle_diff and dist_lelbow2reye < dist_ear2eye and l_elbow_in_area and l_wrist_in_area and abs(ave_angle_x) < 55 and abs(ave_angle_y) < 50 and in_area:
            is_sleeping = True
    # 9. 在前边6个逻辑的基础上， 再加强逻辑限定人在左侧手臂弯曲的情况
    l_arm_length = np.linalg.norm(ls_kpt - lelbow_kpt) + np.linalg.norm(lelbow_kpt - lw_kpt)
    r_arm_length = np.linalg.norm(rs_kpt - relbow_kpt) + np.linalg.norm(relbow_kpt - rw_kpt)
    l_s_x, r_s_x = ls_kpt[0], rs_kpt[0]
    delta_x = (10 / 1280) * frame_w
    if abs(ave_angle_x) < 50 and abs(ave_angle_y) < 50 and (l_s_x - r_s_x) > delta_x and l_arm_length < (r_arm_length/2) and l_elbow_in_area and l_wrist_in_area and in_area:
        is_sleeping = True
    return is_sleeping, ave_angle_y, ave_gaze_score
    


def get_angle(dot1,dot0,dot2):
    """
        dot0->dot1，dot0—>dot2,两个向量的夹角
        参数:
            dot1: [x0,y0]
            dot0: [x1,y1]
            dot2: [x2,y2]
        返回：
            角度值，范围 0~360
    """
    x1 = dot1[0] - dot0[0]
    y1 = dot1[1] - dot0[1]
    # 向量 b（x2，y2）
    x2 = dot2[0] - dot0[0]
    y2 = dot2[1] - dot0[1]
    angle = math.degrees(
        math.acos((x1 * x2 + y1 * y2) / (((x1 ** 2 + y1 ** 2) ** 0.5) * ((x2 ** 2 + y2 ** 2) ** 0.5))))
    return angle

# 关键点距离
def eu_2(a,b):
    """
            dot0->dot1，dot0—>dot2,两个向量的夹角
            参数:
                dot1: [x0,y0]
                dot0: [x1,y1]
                dot2: [x2,y2]
            返回：
                角度值，范围 0~360
    """
    distance=np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) #求两点的距离用两点横纵坐标的差值开根号
    return distance

def cross_point(line1, line2):
    """
        两条直线交叉点是否存在,存在时的交点坐标
        参数:
            line1: [x0,y0,x1,y1]
            line2: [x2,y2,x3,y3]
        返回：
            是否存在交叉点(true,false),交叉点坐标[x,y]
    """
    point_is_exist = False
    x = y = 0
    x1,y1,x2,y2 = line1
    x3,y3,x4,y4 = line2

    if (x2 - x1) == 0:
        k1 = None
        b1 = 0
    else:
        k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
        b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键

    if (x4 - x3) == 0:  # L2直线斜率不存在
        k2 = None
        b2 = 0
    else:
        k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在
        b2 = y3 * 1.0 - x3 * k2 * 1.0

    if k1 is None:
        if not k2 is None:
            x = x1
            y = k2 * x1 + b2
            point_is_exist = True
    elif k2 is None:
        x = x3
        y = k1 * x3 + b1
    elif not k2 == k1:
        x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        point_is_exist = True

    return point_is_exist, [x, y]

#终止手势判断
def fgesture(kp,thresh):
    '''
        输入人体关键点，判断是否终止手势
        参数:
           kp:[    [x0,y0], 鼻
                   [x1,y1], 左肘
                   [x2,y2], 左腕
                   [x3,y3], 右肘
                   [x4,y4], 右腕
           ]
           thresh:
               交叉点到鼻子的距离阈值
        返回：
           是否是终止手势
    '''
        # 左腕左肘 与 右腕右肘   是否交叉
    line1 = [kp[1][0],kp[1][1],kp[2][0],kp[2][1]]
    line2= [kp[3][0],kp[3][1],kp[4][0],kp[4][1]]
    nose = kp[0]
    point_is_exist, p = cross_point(line1, line2)
    ret = False
    if(point_is_exist):
        if(eu_2(nose, p)<thresh):
            ret = True
    return ret



def _iou(bb_test, bb_gt):
    """
    在两个box间计算IOU
    :param bb_test: box1 = [x1y1x2y2]
    :param bb_gt: box2 = [x1y1x2y2]
    :return: 交并比IOU
    """
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h
    o = wh / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1]) + (bb_gt[2] - bb_gt[0]) * (
            bb_gt[3] - bb_gt[1]) - wh)
    return o


def convert_bbox_to_z(bbox):
    """
    将[x1,y1,x2,y2]形式的检测框转为滤波器的状态表示形式[x,y,s,r]。其中x，y是框的中心坐标，s是面积，尺度，r是宽高比
    参数:
       bbox: [x1,y1,x2,y2] 分别是左上角坐标和右下角坐标
    返回：
       [x,y,s,r] 4行1列，其中x,y是box中心位置的坐标，s是面积，r是纵横比w/h
    """
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = bbox[0] + w / 2.
    y = bbox[1] + h / 2.
    s = w * h
    r = w / float(h)
    return np.array([x, y, s, r]).reshape((4, 1))


def convert_x_to_bbox(x, score=None):
    """
    将[cx，cy，s，r]的目标框表示转为[x_min，y_min，x_max，y_max]的形式
    参数:
        x:[ x, y, s, r ],其中x,y是box中心位置的坐标，s是面积，r
        score: 置信度
    返回:
        [x1,y1,x2,y2],左上角坐标和右下角坐标
    """
    w = np.sqrt(x[2] * x[3])
    h = x[2] / w
    if score is None:
        return np.array([x[0] - w / 2., x[1] - h / 2., x[0] + w / 2., x[1] + h / 2.]).reshape((1, 4))
    else:
        return np.array([x[0] - w / 2., x[1] - h / 2., x[0] + w / 2., x[1] + h / 2., score]).reshape((1, 5))


class KalmanBoxTracker(object):
    count = 0

    def __init__(self, bbox):
        """
        初始化边界框和跟踪器
        """
        # 定义等速模型
        # 内部使用KalmanFilter，7个状态变量和4个观测输入
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array(
            [[1, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
        self.kf.H = np.array(
            [[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]])
        self.kf.R[2:, 2:] *= 10.
        self.kf.P[4:, 4:] *= 1000.  # give high uncertainty to the unobservable initial velocities
        self.kf.P *= 10.
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[4:, 4:] *= 0.01
        self.kf.x[:4] = convert_bbox_to_z(bbox)
        self.time_since_update = 0  # 记录从上次更新到当前帧的预测次数，每次更新后清0(update函数中)
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0  # 记录跟踪上的次数，一旦一帧没有跟上直接清0(predict函数中)
        self.age = 0

    def update(self, bbox):
        """
        使用观察到的目标框更新状态向量。filterpy.kalman.KalmanFilter.update 会根据观测修改内部状态估计self.kf.x。
        重置self.time_since_update，清空self.history。
        参数:
           bbox:目标框
        """
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        self.kf.update(convert_bbox_to_z(bbox))

    def predict(self):
        """
        推进状态向量并返回预测的边界框估计。
        将预测结果追加到self.history。由于 get_state 直接访问 self.kf.x，所以self.history没有用到
        """
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0
        self.kf.predict()
        # 预测次数
        self.age += 1
        # 若跟踪过程中未进行更新，将hit_streak = 0
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        # 将预测结果追加到history
        self.history.append(convert_x_to_bbox(self.kf.x))
        return self.history[-1]

    def get_state(self):
        """
        返回当前边界框估计值
        """
        # print("x_speed:{}".format(self.kf.x))
        return convert_x_to_bbox(self.kf.x)


def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    """
    将检测框bbox与卡尔曼滤波器的跟踪框进行关联匹配
    参数:
         detections:检测框
         trackers:跟踪框，即跟踪目标
         iou_threshold:IOU阈值
    返回:  跟踪成功目标的矩阵：matchs
          新增目标的矩阵：unmatched_detections
          跟踪失败即离开画面的目标矩阵：unmatched_trackers
    """
    # 跟踪目标数量为0，直接构造结果
    if (len(trackers) == 0) or (len(detections) == 0):
        return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5), dtype=int)

    # iou 不支持数组计算。逐个计算两两间的交并比，调用 linear_assignment 进行匹配
    iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
    # 遍历目标检测的bbox集合，每个检测框的标识为d
    for d, det in enumerate(detections):
        # 遍历跟踪框（卡尔曼滤波器预测）bbox集合，每个跟踪框标识为t
        for t, trk in enumerate(trackers):
            iou_matrix[d, t] = _iou(det, trk)
    # 通过匈牙利算法将跟踪框和检测框以[[d,t]...]的二维矩阵的形式存储在match_indices中
    result = linear_sum_assignment(-iou_matrix)
    matched_indices = np.array(list(zip(*result)))

    # 记录未匹配的检测框及跟踪框
    # 未匹配的检测框放入unmatched_detections中，表示有新的目标进入画面，要新增跟踪器跟踪目标
    unmatched_detections = []
    for d, det in enumerate(detections):
        if d not in matched_indices[:, 0]:
            unmatched_detections.append(d)
    # 未匹配的跟踪框放入unmatched_trackers中，表示目标离开之前的画面，应删除对应的跟踪器
    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if t not in matched_indices[:, 1]:
            unmatched_trackers.append(t)
    # 将匹配成功的跟踪框放入matches中
    matches = []
    for m in matched_indices:
        # 过滤掉IOU低的匹配，将其放入到unmatched_detections和unmatched_trackers
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        # 满足条件的以[[d,t]...]的形式放入matches中
        else:
            matches.append(m.reshape(1, 2))
    # 初始化matches,以np.array的形式返回
    if len(matches) == 0:
        matches = np.empty((0, 2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)

    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)


class Sort(object):
    """
        多目标跟踪算法，通过卡尔曼滤波来传播目标物体到未来帧中，
        再通过IOU作为度量指标来建立关系，实现多目标追踪
    """

    def __init__(self, max_age=1, min_hits=3):
        # 最大检测数：目标未被检测到的帧数，超过之后会被删
        self.max_age = max_age
        # 目标命中的最小次数，小于该次数不返回
        self.min_hits = min_hits
        # 卡尔曼跟踪器
        self.trackers = []
        # 帧计数
        self.frame_count = 0

    def update(self, dets):
        self.frame_count += 1
        # 在当前帧逐个预测轨迹位置，记录状态异常的跟踪器索引
        # 根据当前所有的卡尔曼跟踪器个数（即上一帧中跟踪的目标个数）创建二维数组：行号为卡尔曼滤波器的标识索引，列向量为跟踪框的位置和ID
        trks = np.zeros((len(self.trackers), 5))  # 存储跟踪器的预测
        to_del = []  # 存储要删除的目标框
        ret = []  # 存储要返回的追踪目标框
        # 循环遍历卡尔曼跟踪器列表
        for t, trk in enumerate(trks):
            # 使用卡尔曼跟踪器t产生对应目标的跟踪框
            pos = self.trackers[t].predict()[0]
            # 遍历完成后，trk中存储了上一帧中跟踪的目标的预测跟踪框
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            # 如果跟踪框中包含空值则将该跟踪框添加到要删除的列表中
            if np.any(np.isnan(pos)):
                to_del.append(t)
        # numpy.ma.masked_invalid 屏蔽出现无效值的数组（NaN 或 inf）
        # numpy.ma.compress_rows 压缩包含掩码值的2-D 数组的整行，将包含掩码值的整行去除
        # trks中存储了上一帧中跟踪的目标并且在当前帧中的预测跟踪框
        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        # 逆向删除异常的跟踪器，防止破坏索引
        for t in reversed(to_del):
            self.trackers.pop(t)
        # 将目标检测框与卡尔曼滤波器预测的跟踪框关联获取跟踪成功的目标，新增的目标，离开画面的目标
        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(dets, trks)

        # 将跟踪成功的目标框更新到对应的卡尔曼滤波器
        for t, trk in enumerate(self.trackers):
            if t not in unmatched_trks:
                d = matched[np.where(matched[:, 1] == t)[0], 0]
                # 使用观测的边界框更新状态向量
                trk.update(dets[d, :][0])

        # 为新增的目标创建新的卡尔曼滤波器对象进行跟踪
        for i in unmatched_dets:
            trk = KalmanBoxTracker(dets[i, :])
            self.trackers.append(trk)

        # 自后向前遍历，仅返回在当前帧出现且命中周期大于self.min_hits（除非跟踪刚开始）的跟踪结果；如果未命中时间大于self.max_age则删除跟踪器。
        # hit_streak忽略目标初始的若干帧
        i = len(self.trackers)
        for trk in reversed(self.trackers):
            # 返回当前边界框的估计值
            d = trk.get_state()[0]
            # 跟踪成功目标的box与id放入ret列表中
            if (trk.time_since_update < 1) and (trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                ret.append(np.concatenate((d, [trk.id + 1])).reshape(1, -1))  # +1 as MOT benchmark requires positive
            i -= 1
            # 跟踪失败或离开画面的目标从卡尔曼跟踪器中删除
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)
        # 返回当前画面中所有目标的box与id,以二维矩阵形式返回
        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0, 5))

def track(tracker,dets):
    '''
        跟踪检测框
        参数：
            dets (list) : [[lx1,ly1,rx2,ry2,conf],...]     lx1,ly1,rx2,ry2,conf1分别为 检测框左上点(lx1,ly1)、右下点(rx2,ry2)和置信度conf
        返回：
            return list: [[lx1,ly1,rx2,ry2,track_id],...]   跟踪框坐标 左上点(lx1,ly1),右下点(rx2,ry2),跟踪编号(track_id)
    '''
    tracks = tracker.update(dets)
    return tracks


if __name__ == '__main__':
    # persons_coords = [[0.1, 0.2, 0.2, 0.4]]
    # areas = [[0, 0], [0.1920, 0], [1920, 1080], [0, 1080]]
    # resolution = [1920, 1080]
    # print(
    #     persons_in_areas(persons_coords=persons_coords,
    #                      areas=areas,
    #                      w_thresh=0.3))
    target_area = np.array([[0, 0], [100, 0], [100, 100], [0, 100]])
    coords = np.array([[[50, 50], [100, 100]], [[0, 0], [80, 80]],
                       [[0, 0], [5, 5]]])
    number, density = compute_density(target_area, coords)
    print(number, density, number * density)
    iou = get_IOU(np.array([50, 50, 100, 100]), np.array([0, 0, 100, 100]))
    print(iou)

    basis_x = [i for i in range(5)]
    basis_y = [0 for i in range(5)]
    cur_x = [i for i in range(5)]
    cur_y = [i for i in range(5)]
    res = get_scan_area(basis_x, basis_y, cur_x, cur_y, 2)
    print(res)