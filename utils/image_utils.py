from skimage.color import rgb2gray, rgba2rgb
from skimage.draw import set_color
from skimage.io import imsave
from skimage.draw import circle, circle_perimeter, rectangle_perimeter
from numpy import uint8
from skimage.filters import threshold_local, thresholding
import random
from numpy import array


def color_out_image(regions, image, multi=True, min=0, scale=2.5):
    for reg in regions:
        temp_set = {(1, 0)}
        y_ls = []
        x_ls = []

        for pt in reg.coords:
            y_ls.append(pt[0])
            x_ls.append(pt[1])
        if multi:
            r = random.randint(0, 200)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        else:
            r, g, b = 23, 162, 25
        scale = float(scale)
        if scale * scale * len(reg.coords) > (float(min)):
            set_color(image, (array(y_ls), array(x_ls)), color=(r, g, b))
    return image


def get_crop_image(image, boarder):
    """:returns crop image with"""
    y, x, z = image.shape
    bx, by = 800 - boarder, 600 - boarder
    startx = x // 2 - (bx // 2)
    starty = y // 2 - (by // 2)
    cropped = image[starty : starty + by, startx : startx + bx]
    return cropped


def get_thresh_image(image, constants):
    if constants["use_alt"]:
        print("USED ALT THRESH")
        img_seg = get_alt_thresh_image(
            image, constants["alt_thresh"], constants["fiber_type"]
        )
    else:
        print("start regular thresh")
        img_seg = get_reg_thresh_image(
            image, constants["thresh"], constants["fiber_type"]
        )
    return img_seg


def get_alt_thresh_image(
    image,
    alt_thresh,
    fiber,
):
    image = rgb2gray(image)
    tr = threshold_local(
        image, 601, "mean", mode="constant", cval=0, offset=-(alt_thresh / 255.0)
    )
    if fiber == "dark":
        print("went")
        img_seg = (image >= tr).astype(uint8)
    else:
        print("light fibers")
        img_seg = (image < tr).astype(uint8)

    window_size = 25
    return img_seg


def get_reg_thresh_image(image, threshold, fiber):
    """Performs constant image thresholding"""
    # image = tfImage.adjust_contrast(image,1.5)
    try:
        image = rgb2gray(rgba2rgb(image))
    except:
        image = rgb2gray(image)
    if fiber == "dark":
        img_seg = (image > threshold / 255).astype(uint8)
    else:
        img_seg = (image < threshold / 255).astype(uint8)
    return img_seg


def color_circle(c, r, image, scale):
    """colors circle with radius r centered at the point (c[0],c[1])
    circle is 3 px wide"""
    for i in range(3):
        x_ls, y_ls = circle_perimeter(int(c[0]), int(c[1]), int(r / scale) - i)
        set_color(image, (y_ls, x_ls), color=(245, 0, 0))


def color_holes2(hole_ls, image, scale):
    """colors circles in hole_ls onto image"""
    for hole in hole_ls:
        color_circle(hole[0], hole[1] / 2, image, scale)
    return image


def add_boarder(image, boarder):
    """
    draws red colored boarder that
    represents the area portion included in the calculations
    :returns numpy array representing image
    """
    y, x, z = image.shape
    for i in range(0, 5):
        coords = rectangle_perimeter(
            start=(boarder // 2 + i, boarder // 2 + i),
            end=(y - boarder // 2 + i, x - boarder // 2 + i),
        )
        set_color(image, coords, (255, 0, 0))

    return image


def save_out_image(image, out_path):
    """saves image  at outpath(normally ./job-name/frame/image"""
    save_name = out_path
    print("OUT_PATH:", save_name)
    imsave(save_name, image)
    print("saved image at", save_name)
