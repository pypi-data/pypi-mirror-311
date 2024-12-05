import os
import re
import sys

import click
import piexif
from PIL import Image
from click import progressbar

Image.MAX_IMAGE_PIXELS = None

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output-dir', type=click.Path(),
              help='Directory to save the output images. If not specified, original images will be overwritten after confirmation.')
@click.option('--thumb', type=str, help="""\b
Thumbnail specification in the format WxH[tfb]. The specification can be one of the following:
 - WxH  crop to WxH from center (e.g., 100x300)
 - WxHt crop to WxH from top (e.g., 100x300t)
 - WxHb crop to WxH from bottom (e.g., 100x300b)
 - WxHf fit inside WxH without cropping (e.g., 100x300f)
 - 0xH  resize to height H, preserving aspect ratio (e.g., 0x300)
 - Wx0  resize to width W, preserving aspect ratio (e.g., 100x0)
""")
@click.option('--thumb-dir', type=click.Path(), help='Directory to save thumbnails. Required when --thumb is used.')
@click.option('--compress', type=click.Choice(['low', 'medium', 'high'], case_sensitive=False),
              help='Compression level for the output images. Default is no compression.')
@click.option('--verbose', is_flag=True, help='Enable verbose output during processing.')
@click.option('--recursive', is_flag=True, help='Process directories recursively, including subdirectories.')
@click.option('--remove-metadata', is_flag=True, help='Remove EXIF metadata from images.')
@click.option('--copyright-text', type=str, help='Add copyright text to the image metadata.')
def convert(input_path, output_dir, thumb, thumb_dir, compress, verbose, recursive, remove_metadata, copyright_text):
    """
    CLI tool to optimize jpeg images for websites

    INPUT_PATH: Path to a single JPEG file or a directory containing JPEG files.
    """
    # Gather list of JPEG files to process
    jpeg_files = []
    if os.path.isdir(input_path):
        if recursive:
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg')):
                        jpeg_files.append(os.path.join(root, file))
        else:
            jpeg_files = [os.path.join(input_path, f) for f in os.listdir(input_path)
                          if f.lower().endswith(('.jpg', '.jpeg'))]
        if not jpeg_files:
            click.echo(f"No JPEG images found in directory {input_path}.")
            sys.exit(1)
    else:
        if input_path.lower().endswith(('.jpg', '.jpeg')):
            jpeg_files = [input_path]
        else:
            click.echo(f"Error: {input_path} is not a JPEG image.")
            sys.exit(1)

    # Confirmation for overwriting original images if no output directory is specified
    if not output_dir:
        if not click.confirm('No output directory specified. Do you want to overwrite the original images?',
                             default=False):
            click.echo("Operation cancelled.")
            sys.exit(0)

    # Validate thumbnail options
    if thumb and not thumb_dir:
        click.echo("Error: --thumb-dir is required when --thumb is used.")
        sys.exit(1)

    # Conflict handling between removing metadata and adding copyright
    if remove_metadata and copyright_text:
        click.echo("Warning: --remove-metadata is set. Skipping adding copyright text.")
        # Optionally, you can decide to exit or proceed without adding the text
        # Here, we'll proceed without adding the text
        copyright_text = None

    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        (verbose and click.echo(f"Output directory set to: {output_dir}"))

    # Create thumbnail directory if needed
    if thumb and thumb_dir:
        os.makedirs(thumb_dir, exist_ok=True)
        (verbose and click.echo(f"Thumbnail directory set to: {thumb_dir}"))

    # Set quality level based on compression option
    match compress:
        case 'low':
            quality = 95
        case 'medium':
            quality = 85
        case 'high':
            quality = 75
        case _:
            quality = 100
    (verbose and click.echo(f"Compression quality set to: {quality}"))

    # Process each JPEG file with a progress bar
    with progressbar(jpeg_files, label='Processing Images', show_eta=True) as bar:
        for input_file in bar:
            process_image(input_file, output_dir, thumb, thumb_dir, quality, remove_metadata, verbose, copyright_text)


def process_image(input_file, output_dir, thumb, thumb_dir, quality, remove_metadata, verbose, copyright_text):
    """
    Processes a single JPEG image according to the specified options.

    Parameters:
    - input_file: Path to the input JPEG file.
    - output_dir: Directory to save the output images.
    - thumb: Thumbnail specification.
    - thumb_dir: Directory to save thumbnails.
    - quality: Compression quality for the output images.
    - remove_metadata: Remove EXIF metadata from images.
    - verbose: Enable verbose output during processing.
    - copyright_text: Add copyright text to the image metadata.
    """
    try:
        with Image.open(input_file) as img:
            # Ensure the image is in JPEG format
            if img.format != 'JPEG':
                (verbose and click.echo(f"Skipping {input_file}: Not a JPEG image."))
                return

            # Remove metadata if specified
            if remove_metadata:
                data = list(img.getdata())
                img_without_exif = Image.new(img.mode, img.size)
                img_without_exif.putdata(data)
                img = img_without_exif
                (verbose and click.echo(f"EXIF metadata removed from {input_file}."))

            # Set output path
            if output_dir:
                output_file = os.path.join(output_dir, os.path.basename(input_file))
            else:
                output_file = input_file  # Overwrite original file

            # Handle copyright
            exif_dict = {}
            if copyright_text:
                try:
                    exif_dict = piexif.load(img.info.get('exif', b''))
                    # Set the copyright tag (ExifIFD.Copyright)
                    # Tag ID 0x8298
                    exif_dict['0th'][piexif.ImageIFD.Copyright] = copyright_text.encode('utf-8')
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(output_file, 'JPEG', progressive=True, quality=quality, exif=exif_bytes)
                    (verbose and click.echo(f"Converted to progressive JPEG with copyright: {output_file}"))
                except Exception as e:
                    click.echo(f"Error adding copyright to {input_file}: {e}")
                    # Save without copyright
                    img.save(output_file, 'JPEG', progressive=True, quality=quality)
                    (verbose and click.echo(f"Converted to progressive JPEG without copyright: {output_file}"))
            else:
                # Save the progressive JPEG with compression
                img.save(output_file, 'JPEG', progressive=True, quality=quality)
                (verbose and click.echo(f"Converted to progressive JPEG: {output_file}"))

            # Create thumbnail if specified
            if thumb:
                thumb_file = os.path.join(thumb_dir, os.path.basename(input_file))
                create_thumbnail(img, thumb, thumb_file, verbose)
    except Exception as e:
        click.echo(f"Error processing {input_file}: {e}")


def create_thumbnail(img, spec, thumb_file, verbose):
    """
    Creates a thumbnail for the given image based on the specified thumbnail specification.

    Parameters:
    - img: The original image.
    - spec: Thumbnail specification in the format WxH[tfb].
    - thumb_file: Path to save the thumbnail.
    - verbose: Enable verbose output during processing.
    """
    try:
        width, height, mode = parse_thumb_spec(spec)
        original_width, original_height = img.size

        match mode:
            case 'crop_center' | 'crop_top' | 'crop_bottom':
                # Ensure target dimensions are not larger than the original
                target_width = min(width, original_width)
                target_height = min(height, original_height)
                match mode:
                    case 'crop_center':
                        img_thumb = crop_center(img, target_width, target_height)
                    case 'crop_top':
                        img_thumb = crop_top(img, target_width, target_height)
                    case 'crop_bottom':
                        img_thumb = crop_bottom(img, target_width, target_height)
            case 'fit':
                img_thumb = img.copy()
                img_thumb.thumbnail((width, height), Image.Resampling.LANCZOS)
            case 'resize_width':
                ratio = width / float(original_width)
                height_new = int(float(original_height) * ratio)
                img_thumb = img.resize((width, height_new), Image.Resampling.LANCZOS)
            case 'resize_height':
                ratio = height / float(original_height)
                width_new = int(float(original_width) * ratio)
                img_thumb = img.resize((width_new, height), Image.Resampling.LANCZOS)
            case _:
                raise ValueError(f"Unknown mode: {mode}")

        # Remove metadata from thumbnail if desired
        img_thumb_no_exif = img_thumb.copy()
        if hasattr(img_thumb, 'info'):
            img_thumb_no_exif.info = {}

        img_thumb_no_exif.save(thumb_file, 'JPEG')
        (verbose and click.echo(f"Thumbnail saved: {thumb_file}"))
    except Exception as e:
        click.echo(f"Error creating thumbnail for {thumb_file}: {e}")


def parse_thumb_spec(spec):
    """
    Parses the thumbnail specification and returns width, height, and mode.

    Parameters:
    - spec: Thumbnail specification in the format WxH[tfb].

    Returns:
    - width: Width of the thumbnail.
    - height: Height of the thumbnail.
    - mode: Mode of the thumbnail (e.g., crop_center, crop_top, crop_bottom, fit, resize_width, resize_height).
    """
    pattern = r'^(\d*)x(\d*)([tfb]?|f?)$'
    match = re.match(pattern, spec)
    if not match:
        raise ValueError(f"Invalid thumbnail specification: {spec}")

    width_str, height_str, mode_flag = match.groups()
    width = int(width_str) if width_str else 0
    height = int(height_str) if height_str else 0

    if mode_flag == 't':
        mode = 'crop_top'
    elif mode_flag == 'b':
        mode = 'crop_bottom'
    elif mode_flag == 'f':
        mode = 'fit'
    else:
        mode = 'crop_center'

    # Handle cases where width or height is zero
    if width == 0 and height == 0:
        raise ValueError("At least one of width or height must be non-zero in the thumbnail specification.")

    if width == 0:
        mode = 'resize_height'
    elif height == 0:
        mode = 'resize_width'

    return width, height, mode


def crop_center(img, target_width, target_height):
    """
    Crops the image centered.

    Parameters:
    - img: The original image.
    - target_width: Target width of the cropped image.
    - target_height: Target height of the cropped image.

    Returns:
    - Cropped image.
    """
    width, height = img.size
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    return img.crop((left, top, right, bottom))


def crop_top(img, target_width, target_height):
    """
    Crops the image from the top.

    Parameters:
    - img: The original image.
    - target_width: Target width of the cropped image.
    - target_height: Target height of the cropped image.

    Returns:
    - Cropped image.
    """
    width, height = img.size
    left = (width - target_width) // 2
    top = 0
    right = left + target_width
    bottom = target_height
    return img.crop((left, top, right, bottom))


def crop_bottom(img, target_width, target_height):
    """
    Crops the image from the bottom.

    Parameters:
    - img: The original image.
    - target_width: Target width of the cropped image.
    - target_height: Target height of the cropped image.

    Returns:
    - Cropped image.
    """
    width, height = img.size
    left = (width - target_width) // 2
    bottom = height
    top = bottom - target_height
    right = left + target_width
    return img.crop((left, top, right, bottom))


if __name__ == "__main__":
    convert()