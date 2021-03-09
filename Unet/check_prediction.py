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
                points.append((j, i))
                break

    for i in range(0, Image.size[1]):
        for j in range(0, Image.size[0]):
            if pix[Image.size[0]-j-1, Image.size[1]-i-1] > 25:
                points.append((Image.size[0]-j-1, Image.size[1]-i-1))
                break
    return points



if __name__ == '__main__':
    predict_mask_folder = "data/predicted_masks/"
    mask_folder = "data/masks/"

    predict_mask_points = []
    mask_points = []

    for i in os.listdir(predict_mask_folder):
        print(predict_mask_folder + i)
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

    for i in os.listdir("data/imgs/"):
        os.system("python predict.py -i data/imgs/" + i + " -o data/predicted_masks/" + i)
