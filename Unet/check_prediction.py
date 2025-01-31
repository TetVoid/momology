import os
from PIL import Image, ImageDraw
import math


def barycenter(Image):
    X_sum = 0
    Y_sum = 0
    point_count = 0
    pix = Image.load()
    for i in range(0, Image.size[1]):
        for j in range(0, Image.size[0]):
            if pix[j, i] > 25:
                X_sum += j
                Y_sum += i
                point_count += 1

    if point_count != 0:
        return Y_sum / point_count, X_sum / point_count
    else:
        return "error"

def get_polyline(Image):
    pix = Image.load()
    points = []
    for i in range(0, Image.size[1]):
        for j in range(0, Image.size[0]):
            if pix[j, i] > 25:
                points.append((i, j))
                break

    for i in range(0, Image.size[1]):
        for j in range(0, Image.size[0]):
            if pix[Image.size[0]-j-1, Image.size[1]-i-1] > 25:
                points.append((Image.size[1]-i-1, Image.size[0]-j-1))
                break
    return points


def calculate_error():
    predict_mask_folder = "Unet/data/predicted_masks/"
    mask_folder = "Unet/data/masks/"

    predict_mask_points = []
    mask_points = []

    for i in os.listdir(predict_mask_folder):
        image1 = Image.open(predict_mask_folder + i)
        image2 = Image.open(mask_folder + i)

        result = barycenter(image1)
        if result != "error":
            predict_mask_points.append(result)
            mask_points.append(barycenter(image2))

    sum = 0
    for i in range(len(mask_points)):
        y = math.pow(mask_points[i][0] - predict_mask_points[i][0], 2)
        x = math.pow(mask_points[i][1] - predict_mask_points[i][1], 2)
        sum += math.sqrt(x + y)

    print(sum / len(mask_points))


def new_predict():
    for i in os.listdir("Unet/data/imgs/"):
        os.system("python Unet/predict.py -i Unet/data/imgs/" + i + " -o Unet/data/predicted_masks/" + i)

    predict_mask_folder = "Unet/data/predicted_masks/"

    log = open("logs.txt", "r")
    information_for_cords = []
    for line in log:
        line = line.replace('\n', '')
        line = line.split(" ")
        information_for_cords.append(line)

    info = None
    for i in os.listdir(predict_mask_folder):
        for j in information_for_cords:
            if j[0] == i:
                info = j
        image1 = Image.open(predict_mask_folder + i)
        result = barycenter(image1)
        if result != "error":
            Y = (result[0]*float(info[5])+int(info[3]))/(
                    image1.size[1]*float(info[5])+int(info[3])+int(info[4]))
            X = (result[1]*float(info[5])+int(info[1]))/(
                    image1.size[0]*float(info[5])+int(info[1])+int(info[2]))

            result = (Y, X)
            poly_line = get_polyline(image1)
            new_poly_line = []
            for j in poly_line:
                Y = (j[0] * float(info[5]) + int(info[3])) / (
                            image1.size[1]*float(info[5]) + int(info[3]) + int(info[4]))
                X = (j[1] * float(info[5]) + int(info[1])) / (
                            image1.size[0]*float(info[5]) + int(info[1]) + int(info[2]))

                new_poly_line.append((Y, X))
            if os.path.exists("Unet/data/barry_center_poly_line.txt") is False:
                result_file = open("Unet/data/barry_center_poly_line.txt", "w")
            else:
                result_file = open("Unet/data/barry_center_poly_line.txt", "a")
            result_file.write(str(i)+" "+str(result[0])+" "+str(result[1]))

            for j in new_poly_line:
                result_file.write(str(j[0])+" "+str(j[1])+" ")
            result_file.write('\n')
            result_file.close()
