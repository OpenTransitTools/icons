import os
from ott.utils import file_utils
from PIL import Image, ImageDraw, ImageFont


font_file = os.path.join(file_utils.get_file_dir(__file__), 'fonts', 'Transit-Bold.ttf')
transit_bold = ImageFont.truetype(font_file, 12)


def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='RGBA', color=(0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    offset, fill = (width / -2.0, '#6884ae')
    left, top = [(value + offset) * antialias for value in bounds[:2]]
    right, bottom = [(value - offset) * antialias for value in bounds[2:]]
    draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS (a high-quality downsampling filter)
    mask = mask.resize(image.size, Image.LANCZOS)

    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


def create_png(text, out_dir=".", font=transit_bold, outline_color="#6884ae", text_color="#FFF"):
    width, height = 20, 20
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    bbox = (1, 1, 19, 19)

    draw = ImageDraw.Draw(canvas)
    text_width, text_height = draw.textsize(text, font=font)

    # draw.ellipse(bbox, fill="#6884ae", outline="#6884ae")
    draw_ellipse(canvas, bbox, outline=outline_color, width=0, antialias=8)
    draw.text(((21 - text_width) / 2, (17 - text_height) / 2), text, text_color, font)

    # save the blank canvas to a file
    out_png = os.path.join(out_dir, str(text).zfill(3) + ".png")
    canvas.save(out_png, "PNG", dpi=(600, 600))


def from_gtfs_routes():
    import urllib2
    import csv
    import zipfile
    from StringIO import StringIO

    maps7_url = "http://maps7.trimet.org/pelias/"
    trimet_zip = maps7_url + "TRIMET.zip"
    out_dir = r"G:\PUBLIC\GIS\MOD\Map_Tiles\png"

    response = urllib2.urlopen(trimet_zip)
    zipfile_object = response.read()

    with zipfile.ZipFile(StringIO(zipfile_object), "r") as maps7_zip:
        with maps7_zip.open('routes.txt') as current_file:
            stops_string = current_file.read()

    routes_list = []

    reader = csv.reader(stops_string.split("\r\n"), delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for r in reader:
        if r:
            routes_list.append(r)

    del routes_list[0]


    for route in routes_list:
        if route[2]:
            create_png(route[0])


def main():
    create_png("31")
 
