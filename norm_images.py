from collections import Counter
from math import sqrt
from os import listdir
from os.path import isfile, join
from sys import stdout

from skimage import io, color
import click

# The purpose of this script is to perform an analysis of images
# it returns the LAB values, including average and SD, as as well as the amount of white space in the image

def get_image_paths(directories):
    ''' Return JPG image paths from the given directories '''
    paths = []

    for directory in directories:
        for filename in listdir(directory):
            path = join(directory, filename)
            if isfile(path) and path.endswith('.jpg'):
                paths.append(path)

    return paths


def get_image(path):
    return io.imread(path)


def get_pixel_count(image):
    return len(image) * len(image[0])


def get_average_lab(image):
    ''' Return a tuple of the average L, A, B values of the given image,
        not including white pixels '''
    lab = color.rgb2lab(image)

    # Assume top-left pixel is always white
    white = tuple(lab[0][0])

    totals = [0] * 3
    pixel_count = 0
    for i, row in enumerate(lab):
        counter = Counter(map(tuple, row))
        if counter[white] == len(image):
            # Entire row is white pixels
            continue

        # Remove white pixels
        del counter[white]

        for pixel, count in counter.items():
            # 0 = L, 1 = A, 2 = B
            totals[0] += pixel[0] * count
            totals[1] += pixel[1] * count
            totals[2] += pixel[2] * count

            pixel_count += count

    return [total / pixel_count for total in totals]


def get_stddev(image, averages):
    ''' Return a tuple of the standard deviations of the L, A, B
        values of the given image '''
    lab = color.rgb2lab(image)

    # Assume top-left pixel is always white
    white = tuple(lab[0][0])

    deltas = [0] * 3
    pixel_count = 0
    for i, row in enumerate(lab):
        counter = Counter(map(tuple, row))
        if counter[white] == len(image):
            # Entire row is white pixels
            continue

        # Remove white pixels
        del counter[white]

        for pixel, count in counter.items():
            # 0 = L, 1 = A, 2 = B
            deltas[0] += count * (pixel[0] - averages[0])**2
            deltas[1] += count * (pixel[1] - averages[1])**2
            deltas[2] += count * (pixel[2] - averages[2])**2

            pixel_count += count

    return [sqrt(delta / pixel_count) for delta in deltas]


def get_whitespace_amount(image):
    ''' Return the amount of whitespace in the given image as a percentage '''
    count = 0
    for row in image:
        counter = Counter(map(tuple, row))
        count += counter[(255, 255, 255)]

    return count / get_pixel_count(image)


@click.command()
@click.option('--slice-index', default=0, help='Slice index in range [1, 4]')
def main(slice_index):
    # JPG images will be searched for in the following paths
    paths = get_image_paths([
        'New_addition_WIP',
    ])

    filename = 'output.csv'

    if slice

        ??_index > 0:
        paths.sort()

        slice_amount = int(len(paths) / 4)
        start = slice_amount * (slice_index - 1)
        end = start + slice_amount

        # Last slice may have a few more elements
        if slice_index == 4:
            end = len(paths)

        paths = paths[start:end]

        filename = f'data-{slice_index}.csv'

    config = {
        'average_lab': True,
        'stddev_lab': True,
        'whitespace': True,
    }

    with open(filename, mode='a', buffering=1) as f:
        f.write('"Filename"')

        if config['average_lab']:
            f.write(', "Avg L", "Avg A", "Avg B"')

        if config['stddev_lab'] and config['average_lab']:
            f.write(', "SD L", "SD A", "SD B"')

        if config['whitespace']:
            f.write(', "Whitespace"\n')

        for path in paths:
            print(path, end='')
            stdout.flush()

            image = get_image(path)

            f.write(f'"{path}"')

            if config['average_lab']:
                averages = get_average_lab(image)
                f.write(
                    f',{averages[0]:.6g},{averages[1]:.6g},{averages[2]:.6g}')

                print('.', end='')
                stdout.flush()

            if config['stddev_lab'] and config['average_lab']:
                # Need averages to get standard deviation
                stddev = get_stddev(image, averages)
                f.write(f',{stddev[0]:.6g},{stddev[1]:.6g},{stddev[2]:.6g}')

                print('.', end='')
                stdout.flush()

            if config['whitespace']:
                whitespace = get_whitespace_amount(image)
                f.write(f',{whitespace:.6g}')

                print('.', end='')
                stdout.flush()

            f.write('\n')
            print()


main()
