import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy import skew
import math
# import tcp
# from sklearn.decomposition import PCA 
from numpy.linalg import eig

def Fit_the_plane(points):
    A = np.c_[points[:,0], points[:,1], points[:,2], np.ones(points.shape[0])]
    _, _, Vt = np.linalg.svd(A)
    plane = Vt[3, :]
    # (a, b, c) = compute_normal_vector(plane[0], plane[1], plane[2])
    # plane_tmp = np.array([a, b, c, plane[3]])
    # print(plane_tmp)
    # return plane_tmp
    return plane

def project_to_plane(points, plane):
    # 提取平面法向量和常数项
    normal = plane[:3]
    D = plane[3]
    # 归一化平面法向量和常数项
    dis = np.linalg.norm(normal)
    normal = normal / dis
    D = D / dis
    # 计算每个点到平面的距离
    distances = np.dot(points, normal) + D
    # 计算投影点
    projected_points = points - distances.reshape(-1, 1) * normal
    return projected_points

def fit_circle_3d(points):
    A = np.c_[2*points[:,0], 2*points[:,1], 2*points[:,2], np.ones(points.shape[0])]
    b = points[:,0]**2 + points[:,1]**2 + points[:,2]**2
    coeffs = np.linalg.lstsq(A, b, rcond=None)[0]
    x0, y0, z0 = coeffs[:3]
    radius = np.sqrt(coeffs[3] + x0**2 + y0**2 + z0**2)
    return (x0, y0, z0), radius

# def define_plane(point1, point2, point3):
#     # 三个天线确定的平面
#     AB = np.asmatrix(point2 - point1)
#     AC = np.asmatrix(point3 - point1)
#     N = np.cross(AB, AC)  # 向量叉乘，求法向量
#     Ax, By, Cz = N[0, 0], N[0, 1], N[0, 2]
#     D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
#     return Ax, By, Cz, D


def move_plane_to_point(plane_normal, point_A):
    # 根据法向量和新的起点确定新的平面
    dis = np.linalg.norm(plane_normal)
    plane_normal = plane_normal / dis
    a, b, c = plane_normal
    x_A, y_A, z_A = point_A
    d = -(a * x_A + b * y_A + c * z_A)
    return a, b, c, d

def point_to_plane_distance(point, plane_coefficients):
    # 计算点到平面的距离。
    Ax, By, Cz, D = plane_coefficients
    mod_d = Ax * point[0] + By * point[1] + Cz * point[2] + D
    mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
    distance = mod_d / mod_area
    return distance



# def calculate_intersection(point_A, point_B, plane_coefficients):
#     """
#     计算平面与AB连线的交点坐标。
#     :param point_A: 点A的坐标 (x_A, y_A, z_A)
#     :param point_B: 点B的坐标 (x_B, y_B, z_B)
#     :param plane_coefficients: 平面方程的系数 (a, b, c, d)
#     :return: 交点坐标 (x, y, z)
#     """
#     a, b, c, d = plane_coefficients
#     AB_vector = np.array(point_B) - np.array(point_A)
#     t = -(a * point_A[0] + b * point_A[1] + c * point_A[2] + d) / np.dot(AB_vector, [a, b, c])
#     intersection_point = np.array(point_A) + t * AB_vector
#     return intersection_point


# def get_lamda(point_A, point_B, point_D):
#     AB_vector = np.array(point_B) - np.array(point_A)
#     AD_vector = np.array(point_D) - np.array(point_A)
#     return np.linalg.norm(AD_vector) / np.linalg.norm(AB_vector)

# def get_lamda_point(point_A, point_B, lamda):
#     AB_vector = np.array(point_B) - np.array(point_A)
#     distance = lamda * np.linalg.norm(AB_vector)
#     D_prime = np.array(point_A) + distance * AB_vector / np.linalg.norm(AB_vector)
#     return D_prime

def compute_normal_vector(a, b, c):
    # 平面方程中的ax + by + cz + d = 0，用abc来求法向量
    magnitude = np.sqrt(a**2 + b**2 + c**2)
    normal_vector = (a / magnitude, b / magnitude, c / magnitude)
    return normal_vector

def angle_with(plane1, plane2):
    # 计算两个平面之间的夹角
    n1 = compute_normal_vector(plane1[0], plane1[1], plane1[2])
    n2 = compute_normal_vector(plane2[0], plane2[1], plane2[2])
    dot_product = sum(x * y for x, y in zip(n1, n2))
    angle_rad = math.acos(dot_product)
    return angle_rad

# def vector_angle(a, b):  
#     # 计算点积  
#     dot_product = sum(x*y for x, y in zip(a, b))  
      
#     # 计算模长  
#     norm_a = math.sqrt(sum(x**2 for x in a))  
#     norm_b = math.sqrt(sum(x**2 for x in b))  
      
#     # 计算夹角（以弧度为单位）  
#     cos_theta = dot_product / (norm_a * norm_b)  
#     theta = math.acos(cos_theta)    
#     return theta

# def line_equation_3d(p1, p2):
#     # 提取 p1 和 p2 的坐标
#     x1, y1, z1 = p1
#     x2, y2, z2 = p2
    
#     # 计算方向向量
#     dx = x2 - x1
#     dy = y2 - y1
#     dz = z2 - z1
    
#     # 返回参数方程的系数
#     return (x1, y1, z1), (dx, dy, dz)

# def find_plane_b(a, b, c, d, x0, y0, z0, theta):
#     # 根据已知平面ax + by + cz + d = 0，已知的点p（x0,y0,z0），已知平面间夹角theta，求目标平面表达
#     # 平面a的法向量
#     n_a = np.array([a, b, c])
    
#     # 计算平面a的法向量的模
#     norm_a = np.linalg.norm(n_a)
    
#     # 计算平面a的法向量的单位向量
#     u = n_a / norm_a
    
#     # 选择一个与u垂直的向量v
#     if u[0] != 0 or u[1] != 0:
#         v = np.array([-u[1], u[0], 0])
#     else:
#         v = np.array([0, -u[2], u[1]])
    
#     # 计算v的单位向量
#     v = v / np.linalg.norm(v)
    
#     # 计算旋转后的法向量n_b
#     cos_theta = np.cos(theta)
#     sin_theta = np.sin(theta)
#     n_b = cos_theta * u + sin_theta * v

#     # 验证夹角
#     # cos_angle = np.dot(n_a, n_b) / (norm_a * np.linalg.norm(n_b))
#     # cos_angle = np.clip(cos_angle, -1, 1)  # 修正cos_angle的值
#     # angle = np.arccos(cos_angle)
#     # angle_deg = math.degrees(angle)
#     # print(f"计算的夹角: {angle_deg}")
    
#     # 计算平面b的常数项
#     constant_b = -np.dot(n_b, np.array([x0, y0, z0]))
    
#     return n_b, constant_b

# def rodrigues_rotation_matrix(k, theta):
#     """
#     k (numpy array): 旋转轴的单位向量，形状为 (3,)
#     theta (float): 旋转角度（弧度）
#     返回:
#     R=I+(sinθ)K+(1−cosθ)K2 
#     numpy array: 旋转矩阵，形状为 (3, 3)
#     """
    
#     # 单位矩阵
#     I = np.eye(3)
#     K = skew(k)

#     return I + math.sin(theta) * K + (1 - math.cos(theta)) * np.dot(K ,K)

def rotate_point_around_axis(point, axis_point, axis_direction, theta):
    # Translate point to the origin
    p = np.array(point) - np.array(axis_point)

    # Normalize the axis direction vector
    u = np.array(axis_direction)
    u = u / np.linalg.norm(u)

    ux, uy, uz = u
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    # Rotation matrix around the origin
    R_origin = np.array([
        [cos_theta + one_minus_cos*ux**2, one_minus_cos*ux*uy - sin_theta*uz, one_minus_cos*ux*uz + sin_theta*uy],
        [one_minus_cos*ux*uy + sin_theta*uz, cos_theta + one_minus_cos*uy**2, one_minus_cos*uy*uz - sin_theta*ux],
        [one_minus_cos*ux*uz - sin_theta*uy, one_minus_cos*uy*uz + sin_theta*ux, cos_theta + one_minus_cos*uz**2]
    ])

    # Rotate point
    p_rotated = np.dot(R_origin, p)

    # Translate point back
    p_final = p_rotated + np.array(axis_point)

    return p_final

def is_point_in_plane(point, plane):
    A, B, C, D = plane
    x, y, z = point
    return np.isclose(A*x + B*y + C*z + D, 0, atol=1e-2)

def is_point_in_plane2(point, plane):
    A, B, C, D = plane
    x, y, z = point
    return np.isclose(A*x + B*y + C*z + D, 0, atol=1e-1)

def check_front(point_a, point_b, origin_a, origin_b):
    AB = np.array(point_b) - np.array(point_a)
    AC = np.array(origin_b) - np.array(origin_a)
    AB = np.array([AB[0], AB[1], 0.0])
    AC = np.array([AC[0], AC[1], 0.0])
    angle = angle_with(AB, AC)
    # print("angle:", angle)
    print(abs(angle))
    if abs(angle) > 1.8:
        return True
    return False

# def find_theta(plane, point, axis_point, axis_direction, initial_theta=0.0, step=0.001, tolerance=1e-6):
#     theta = initial_theta
#     while theta < 2 * np.pi:
#         tmp_theta = theta
#         rotated_point = rotate_point_around_axis(point, axis_point, axis_direction, tmp_theta)
#         if is_point_in_plane(rotated_point, plane):
#             return tmp_theta, rotated_point
#         theta += step
#     return None, None  # No solution found within 0 to 2*pi

def find_theta(plane, cur_point_a, cur_point_b, ori_point_a, ori_point_b, axis_point, axis_direction, initial_theta=0.0, step=0.01, tolerance=1e-4):
    theta = initial_theta
    while theta < 2 * np.pi:
        tmp_theta = theta
        rotated_point_1 = rotate_point_around_axis(cur_point_b, axis_point, axis_direction, tmp_theta)
        if is_point_in_plane2(rotated_point_1, plane):
            rotated_point_2 = rotate_point_around_axis(cur_point_a, axis_point, axis_direction, tmp_theta)
            if check_front(rotated_point_2, rotated_point_1, ori_point_a, ori_point_b):
                theta += step
                continue
            # return tmp_theta, rotated_point_1
            return find_theta2(plane, cur_point_a, cur_point_b, ori_point_a, ori_point_b, axis_point, axis_direction, tmp_theta)
        theta += step
    return None, None  # No solution found within 0 to 2*pi

def find_theta2(plane, cur_point_a, cur_point_b, ori_point_a, ori_point_b, axis_point, axis_direction, tmp_theta, initial_theta=0.0, step=0.001, tolerance=1e-6):
    over = False
    if tmp_theta < 0.1:
        tmp_theta = 0.0 
        # tmp = 2.0 * math.pi
        over = True
    else:
        tmp_theta = tmp_theta - 0.1
    tmp = tmp_theta + 0.2
    theta = tmp_theta
    while theta < tmp:
        tmp_theta = theta
        rotated_point_1 = rotate_point_around_axis(cur_point_b, axis_point, axis_direction, tmp_theta)
        if is_point_in_plane(rotated_point_1, plane):
            rotated_point_2 = rotate_point_around_axis(cur_point_a, axis_point, axis_direction, tmp_theta)
            if check_front(rotated_point_2, rotated_point_1, ori_point_a, ori_point_b):
                theta += step
                continue
            return tmp_theta, rotated_point_1
        theta += step
    if over:
        theta = 2.0 * math.pi - 0.1
        while theta < 2.0 * math.pi:
            tmp_theta = theta
            rotated_point_1 = rotate_point_around_axis(cur_point_b, axis_point, axis_direction, tmp_theta)
            if is_point_in_plane(rotated_point_1, plane):
                rotated_point_2 = rotate_point_around_axis(cur_point_a, axis_point, axis_direction, tmp_theta)
                if check_front(rotated_point_2, rotated_point_1, ori_point_a, ori_point_b):
                    theta += step
                    continue
                return tmp_theta, rotated_point_1
            theta += step
    return None, None  # No solution found within 0 to 2*pi

def project_to_plane2(point, plane_normal, plane_d):  
    # 计算点到平面的距离  
    dist = -(np.dot(plane_normal, point) + plane_d) / np.linalg.norm(plane_normal)  
    # 计算投影点  
    projected_point = point + dist * (plane_normal / np.linalg.norm(plane_normal))  
    return projected_point

def get_R(axis_direction, theta):
    u = np.array(axis_direction)
    u = u / np.linalg.norm(u)

    ux, uy, uz = u
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    # Rotation matrix around the origin
    R_origin = np.array([
        [cos_theta + one_minus_cos*ux**2, one_minus_cos*ux*uy - sin_theta*uz, one_minus_cos*ux*uz + sin_theta*uy],
        [one_minus_cos*ux*uy + sin_theta*uz, cos_theta + one_minus_cos*uy**2, one_minus_cos*uy*uz - sin_theta*ux],
        [one_minus_cos*ux*uz - sin_theta*uy, one_minus_cos*uy*uz + sin_theta*ux, cos_theta + one_minus_cos*uz**2]
    ])
    return R_origin

# points = np.random.rand(10, 3)
# print(points)
# points[:,2] = 0
# 将第一列作为x，第二列作为y，第三列作为z
####################################################################################################################################
def not_all_in_plane(a, b, c):
    x = np.random.uniform(-10, 10, size=10)
    y = np.random.uniform(-10, 10, size=10)
    z = (a * x + b * y + c) + np.random.normal(0.0, 0.1, size=10)
    return x, y, z
# x, y, z = not_all_in_plane(2, 5, 6)
# points = []
# for i in range(len(x)):
#     points.append([x[i], y[i], z[i]])
# points = np.array(points)
# # print(points)
# x0 = np.mean(x)
# y0 = np.mean(y)
# z0 = np.mean(z)
# coefficients = Fit_the_plane(points)
# print(len(coefficients))
# a, b, c, d = move_plane_to_point(coefficients[:3], [x0, y0, z0])
# print("%fx + %fy + %fz + %f = 0" %(a, b, c, d))
# d = point_to_plane_distance([x0, y0 + 2.0, z0 + 10.0], [a, b, c, d])
# print(d)

# c = (coefficients[0] * x0 + coefficients[1] * y0 + coefficients[2] * z0) / coefficients[2]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(points[:, 0], points[:, 1], points[:, 2])
# ax.scatter(coefficients[0], coefficients[1], coefficients[2])

# xx, yy = np.meshgrid(np.linspace(0, 1), np.linspace(0, 1))

# zz = (-coefficients[0] / coefficients[2]) * xx + (-coefficients[1] / coefficients[2]) * yy + c
# ax.plot_surface(xx, yy, zz)

# plt.show()
####################################################################################################################################

# def correct2(c_trajectory_points, point_a, point_b, point_c):
#     # 大幅度变幅，获取变幅轴和变幅平面
#     plane_c = Fit_the_plane(c_trajectory_points)
#     BC_mid_point = get_lamda_point(point_b, point_c, 0.5)
#     plane_normal = plane_c[:3]
#     new_plane = move_plane_to_point(plane_normal, BC_mid_point)
#     crosspoint_planeC_AC = calculate_intersection(point_a, point_c, new_plane)
#     vector = np.array(crosspoint_planeC_AC) - np.array(BC_mid_point)
#     normal_vector_BC_lamda_point = vector / np.linalg.norm(vector)
#     lamda_AC = (point_a, point_c, crosspoint_planeC_AC)
#     plane_ABC = define_plane(point_a, point_b, point_c)
#     normal_vector_plane_ABC = compute_normal_vector(plane_ABC[0], plane_ABC[1], plane_ABC[2])
#     angle = angle_with(new_plane, plane_ABC)
#     tmp_vec = np.dot(rodrigues_rotation_matrix(normal_vector_BC_lamda_point, angle), normal_vector_plane_ABC)
#     dot_product = np.dot(plane_normal, tmp_vec)
#     tmp_angle = math.acos(dot_product)
#     if math.abs(dot_product - 1.0) > 0.01:
#         angle = -angle
#     return lamda_AC, angle

# def detection(point_a, point_b, point_c, lamda_AC, angle):
#     plane_ABC = define_plane(point_a, point_b, point_c)
#     BC_mid_point = get_lamda_point(point_b, point_c, 0.5)
#     lamda_point = get_lamda_point(point_a, point_c, lamda_AC)
#     normal_vector_plane_ABC = compute_normal_vector(plane_ABC[0], plane_ABC[1], plane_ABC[2])
#     vector = np.array(lamda_point) - np.array(BC_mid_point)
#     normal_vector_BC_lamda_point = vector / np.linalg.norm(vector)
#     new_vector = np.dot(rodrigues_rotation_matrix(normal_vector_BC_lamda_point, angle), normal_vector_plane_ABC)
#     new_plane = move_plane_to_point(new_vector.tolist(), point_c)
#     # (x1, y1, z1), (dx, dy, dz) = line_equation_3d(BC_mid_point, lamda_point)

#     return new_plane

def correct1(b_trajectory_points):
    # 旋转一圈，获取旋转轴

    # Fit plane
    plane = Fit_the_plane(b_trajectory_points)
    plane_normal = plane[:3]
    a, b, c = plane_normal
    plane_normal_ = compute_normal_vector(a, b, c)
    # Project points to plane
    projected_points = project_to_plane(b_trajectory_points, plane)

    # Fit circle
    fitted_center, fitted_radius = fit_circle_3d(projected_points)

    fitted_center_p = project_to_plane([fitted_center], plane)[0]
    # 返回旋转轴的轴心和轴的方向
    return fitted_center_p, plane_normal_

def correct2(c_trajectory_points, point_a, point_b, point_c):
    # 大幅度变幅，获取变幅轴,变幅平面和基准旁弯距离
    plane_c = Fit_the_plane(c_trajectory_points)
    plane_normal = plane_c[:3]
    a, b, c = plane_normal
    plane_normal_ = compute_normal_vector(a, b, c)
    ############################# 基准变幅平面从b改a
    new_plane = move_plane_to_point(plane_normal_, point_a)
    basic_pangwang_dis = point_to_plane_distance(point_c, new_plane)

    # Project points to plane
    projected_points = project_to_plane(c_trajectory_points, plane_c)

    # Fit circle
    fitted_center, fitted_radius = fit_circle_3d(projected_points)

    fitted_center_p = project_to_plane([fitted_center], plane_c)[0]
    # 返回基础旁弯距离，过b点的变幅平面，变幅轴的轴心，变幅轴的方向就是变幅平面的法向量，并记录原始形态下的b的坐标
    return basic_pangwang_dis, new_plane, fitted_center_p, point_b

def correct3(c_trajectory_points, new_plane):
    # 伸长吊臂，拟合理想直线
    # 将点投影到平面上
    plane_normal = new_plane[:3]
    plane_d = new_plane[3]
    projected_points = np.array([project_to_plane2(point, plane_normal, plane_d) for point in c_trajectory_points])
    # 拟合投影后的点来找到直线的方向向量  
    centroid = np.mean(projected_points, axis=0)  
    centered_points = projected_points - centroid  
    covariance_matrix = np.cov(centered_points.T)  
    eigenvalues, eigenvectors = eig(covariance_matrix)  
    max_eigenvalue_index = np.argmax(eigenvalues)  
    line_direction = eigenvectors[:, max_eigenvalue_index] 
    unit_line_direction = line_direction / np.linalg.norm(line_direction)
    return unit_line_direction, centroid



def detection(point_a, point_b, point_c, origin_a, origin_b, origin_c, luf_origin_b,basic_pangwang_dis, plane_k, axis_point, axis_direction, Luffing_axis_point, line_vec, line_point, angle_diff):
    # point_a, point_b, point_c是当前的三个天线的位置
    # origin_b是初始化时天线a的位置
    # plane_k是基准变幅平面过origin_b的新的平面
    # axis_point, axis_direction 是旋转轴的轴心和轴向
    # Luffing_axis_point是初始变幅轴的轴心，他的轴向和基准变幅平面的法向量相等
    # line_vec, line_point是拟合直线的表达，为一个直线上的点和单位方向向量

    # 计算出当前b点到初始变幅平面的旋转角度

    # print("new plane: ", plane_k, "\n", "point: ", point_b, "\n", "axis_point: ", axis_point, "\n", "axis_direction: ", axis_direction, "\n", "origin_b: ", origin_b, "\n")
    # origin_a = [np.float64(636003.0553794308), np.float64(3116429.790478268), 77.5266] 
    # origin_b = [np.float64(636004.2920980707), np.float64(3116431.141854721), 78.8462] 
    # # [np.float64(636004.2899430173), np.float64(3116431.141386878), 78.8518] -0.8772615029010922 
    # plane_k = (np.float64(-0.7060195304873985), np.float64(0.7081922995949879), np.float64(0.00029893931865738283), np.float64(-1758001.108754708)) 
    # axis_point = [6.36003226e+05, 3.11642940e+06, 8.87759426e+01] 
    # axis_direction = (np.float64(0.0016527758496396679), np.float64(-0.02284051729301591), np.float64(-0.9997377551647123)) 
    axis_direction = [0.0, 0.0, -1.0]
    # basic_pangwang_dis = -0.8772615029010922
    # print("point_a: ", point_a, point_b)

    # theta, rotated_point = find_theta(plane_k, point_a, point_b, origin_a, origin_b, axis_point, axis_direction)
    theta, rotated_point = find_theta(plane_k, point_b, point_a, origin_b, origin_a, axis_point, axis_direction)

    print("param: ",origin_a,origin_b, luf_origin_b,basic_pangwang_dis, plane_k, axis_point, axis_direction, Luffing_axis_point, line_vec, line_point)
    print("theta: ",theta)
    if not theta:
        theta = 0.0
    print("theta: ",theta)
    if 0.003 < theta < (2 * math.pi - 0.003):
        theta = theta + 0.003
    R = get_R(axis_direction, -theta)
    # 旧b点一定在初始变幅平面上，反向旋转旧b点到新变幅上
    # new_origin_b = rotate_point_around_axis(origin_b, axis_point, axis_direction, -theta)
    new_origin_a = rotate_point_around_axis(origin_a, axis_point, axis_direction, -theta)
    # # 验证旋转是否正确
    # AB = np.array(point_b) - np.array(point_a)
    # AC = np.array(new_origin_b) - np.array(point_a)
    # AB = np.array([AB[0], AB[1], 0.0])
    # AC = np.array([AC[0], AC[1], 0.0])
    # angle = angle_with(AB, AC)
    # # print("angle:", angle)
    # if abs(angle) > math.pi / 2.0:
    #     theta = -theta
    # new_origin_b = rotate_point_around_axis(origin_b, axis_point, axis_direction, -theta)
    # print(theta)
    
    # 计算新的变幅平面
    plane_coefficients = np.array([plane_k[0], plane_k[1], plane_k[2]])
    transformed_plane_coefficients = np.dot(R, plane_coefficients)
    # new_plane_k = move_plane_to_point(transformed_plane_coefficients, new_origin_b)
    new_plane_k = move_plane_to_point(transformed_plane_coefficients, new_origin_a)

    print("new_plane_k: ", new_plane_k)

    # 计算点c在平面的左右
    c_projected_point = project_to_plane2(origin_c, plane_k[:3], plane_k[3])
    vec_plane = [float(c_projected_point[0] - origin_a[0]), float(c_projected_point[1] - origin_a[1])]
    vec_cur = [float(origin_c[0] - origin_a[0]), float(origin_c[1] - origin_a[1])]
    cross_product = vec_plane[0] * vec_cur[1] - vec_cur[0] * vec_plane[1]

    # 叉积大于0在左边, 此时旁弯也该大于0
    revert = False
    if cross_product * basic_pangwang_dis < 0:
        revert = True
    # if (cross_product > 0 and basic_pangwang_dis < 0) or (cross_product < 0 and basic_pangwang_dis > 0):
    #     revert = True


    # 计算旁弯值
    test_a_dis  = point_to_plane_distance(point_a, new_plane_k)
    test_b_dis  = point_to_plane_distance(point_b, new_plane_k)
    print("test_a_dis: ",test_a_dis, "   test_b_dis: ",test_b_dis)
    pangwang_dis = point_to_plane_distance(point_c, new_plane_k) - basic_pangwang_dis
    print("point_c: ", point_c)
    print("ori_pangwang_dis: ", pangwang_dis + basic_pangwang_dis)
    luffing_angle = angle_diff
    if revert:
        pangwang_dis = - pangwang_dis
        luffing_angle = -luffing_angle

    # 计算新的变幅轴心，连接轴心到新b点和旧b点转过来的点，他们在同一平面上，计算变幅角度
    new_Luffing_axis_point = rotate_point_around_axis(Luffing_axis_point, axis_point, axis_direction, -theta)
    # now_l = np.array(point_b) - np.array(new_Luffing_axis_point)
    # t_l = np.array(luf_origin_b) - np.array(new_Luffing_axis_point)
    
    # luffing_angle = angle_with(now_l, t_l)
    # print("luffing_angle: ",luffing_angle)

    # # 验证角度是否正确
    # now_cross_product = np.cross(now_l, t_l)
    # new_plane_k_coefficients = np.array([new_plane_k[0], new_plane_k[1], new_plane_k[2]])
    # norm_a = np.linalg.norm(now_cross_product)
    # norm_b = np.linalg.norm(new_plane_k_coefficients)
    # dot_product = np.dot(now_cross_product, new_plane_k_coefficients)
    # if dot_product > 0 and np.isclose(np.abs(dot_product), norm_a * norm_b):
    #     luffing_angle = -luffing_angle


    # 将伸长的直线转过来
    R2 = get_R(new_plane_k[:3], -luffing_angle)
    new_line_point_tmp = rotate_point_around_axis(line_point, axis_point, axis_direction, -theta)
    new_line_point = rotate_point_around_axis(new_line_point_tmp, new_Luffing_axis_point, new_plane_k[:3], -luffing_angle)
    transformed_line_vec_tmp = np.dot(R, line_vec)
    transformed_line_vec = np.dot(R2, transformed_line_vec_tmp)
    # xy平面的法向量  
    xy_plane_normal = np.array([0, 0, 1])  
    
    # 计算平面j的法向量（直线方向向量与xy平面法向量的叉积）  
    plane_j_normal = np.cross(transformed_line_vec, xy_plane_normal)  
    # plane_j_normal = np.cross(transformed_line_vec_tmp, xy_plane_normal)
    plane_j_normal = plane_j_normal / np.linalg.norm(plane_j_normal)  # 归一化  
    
    # 计算平面k的法向量（直线方向向量与平面j法向量的叉积）  
    plane_k_normal = np.cross(transformed_line_vec, plane_j_normal)  
    # plane_k_normal = np.cross(transformed_line_vec_tmp, plane_j_normal)  
    plane_k_normal = plane_k_normal / np.linalg.norm(plane_k_normal)

    # 计算k平面的方程
    a, b, c = plane_k_normal  
    d = -np.dot(plane_k_normal, new_line_point)
    # d = -np.dot(plane_k_normal, new_line_point_tmp)

    # 计算c点的x，y在平面k上的z值，这个就是理想的扰度值
    x = point_c[0]
    y = point_c[1]
    z = point_c[2]
    
    # deflection = -(a * x + b * y + d) / c - z
    new_z = -(a * x + b * y + d) / c
    dis_ac = math.sqrt((x - new_line_point_tmp[0])**2 + (y - new_line_point_tmp[1])**2 + (z - new_line_point_tmp[2])**2)
    dis_an = math.sqrt((x - new_line_point_tmp[0])**2 + (y - new_line_point_tmp[1])**2 + (new_z - new_line_point_tmp[2])**2)
    vector_normalized = transformed_line_vec_tmp / np.linalg.norm(transformed_line_vec_tmp)
    end_point = new_line_point_tmp + (dis_ac + dis_an) / 2.0 * vector_normalized
    deflection = (end_point[2] - z) * 0.6

    return pangwang_dis, deflection, theta

    # return pangwang_dis, new_plane_k, new_origin_b, theta


    
