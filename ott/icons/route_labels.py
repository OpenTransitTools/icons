import os
from ott.utils import file_utils
from ott.utils.parse.cmdline.base_cmdline import file_cmdline
from PIL import Image, ImageDraw, ImageFont


font_file = os.path.join(file_utils.get_file_dir(__file__), 'fonts', 'Transit-Bold.ttf')
transit_bold = ImageFont.truetype(font_file, 12)


def create_png(text, fill_color="#6884ae", outline_color=None, text_color="#FFF", width=20, height=20, out_dir=".", font=transit_bold):
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    bbox = (1, 1, width-1, height-1)
    draw = ImageDraw.Draw(canvas)
    text_width, text_height = draw.textsize(text, font=font)

    if outline_color is None:
        outline_color = fill_color

    # draw.ellipse(bbox, fill="#6884ae", outline="#6884ae")
    draw_ellipse(canvas, bbox, fill_color, outline=outline_color, width=0, antialias=8)
    draw.text(((width + 1 - text_width) / 2, (height - 2 - text_height) / 2), text, text_color, font)

    # save the blank canvas to a file
    out_png = os.path.join(out_dir, str(text).zfill(3) + ".png")
    canvas.save(out_png, "PNG", dpi=(600, 600))


def draw_ellipse(image, bounds, fill_color, width=1, outline='white', antialias=4):
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
    offset, fill = (width / -2.0, fill_color)
    left, top = [(value + offset) * antialias for value in bounds[:2]]
    right, bottom = [(value - offset) * antialias for value in bounds[2:]]
    draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS (a high-quality downsampling filter)
    mask = mask.resize(image.size, Image.LANCZOS)

    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


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
    fp = file_cmdline(do_parse=False)
    fp.add_argument(
        '--text',
        '-t',
        required=True,
        help="text content in the icon"
    )
    fp.add_argument(
        '--color',
        '-c',
        required=False,
        help="color of the icon ... starts with a # (e.g., #FFF or #c24d45)",
        default="#6884ae"
    )
    fp.add_argument(
        '--width',
        '-w',
        required=False,
        help="width of the icon",
        type=int,
        default=20
    )
    fp.add_argument(
        '--height',
        '-H',
        required=False,
        help="height of the icon",
        type=int,
        default=20
    )

    args = fp.parse_args()
    create_png(args.text, args.color, width=args.width, height=args.height)
