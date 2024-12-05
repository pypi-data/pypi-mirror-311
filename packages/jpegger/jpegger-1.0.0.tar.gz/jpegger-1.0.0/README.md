![Logo](assets/banner.png)

![PyPI](https://img.shields.io/pypi/v/...)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ValentinKolb/jpeg_converter/ci.yml)

Img-Tool is a versatile CLI tool designed to convert standard (baseline) JPEG images into progressive JPEGs.
It streamlines the process of handling large batches of images, offering additional features like thumbnail creation, compression control, metadata management, and more.

## Installation

To install the tool, simply run the following command:

```bash
pip install todo
```

## Usage

After installation, you can start using JPEG Converter by executing:

```bash
jpeg-converter [OPTIONS] INPUT_PATH
```

## Features

JPEG Converter comes with a variety of features to manage and optimize your JPEG images efficiently:
- Convert Baseline to Progressive JPEG: Easily convert single images or entire directories from baseline to progressive JPEG format.
- Batch Processing: Handle multiple images at once, with support for recursive directory traversal.
- Thumbnail Generation: Create thumbnails with various specifications, including cropping and resizing.
- Compression Control: Adjust compression levels to balance image quality and file size.
- Metadata Management: Remove EXIF metadata to protect privacy or embed custom copyright information.

## Configuration

JPEG Converter can be configured using command-line options. Below is a table of available options:

| Option                           | Description                                                                                                      |
|----------------------------------|------------------------------------------------------------------------------------------------------------------|
| `--output-dir PATH`              | Directory to save the output images. If not specified, original images will be overwritten after confirmation.   |
| `--thumb TEXT`                   | Thumbnail specification. Formats: <br> - WxH (e.g., 100x300) - Crop to WxH from center <br> - WxHt (e.g., 100x300t) - Crop from top <br> - WxHb (e.g., 100x300b) - Crop from bottom <br> - WxHf (e.g., 100x300f) - Fit inside WxH without cropping <br> - 0xH (e.g., 0x300) - Resize to height H, preserving aspect ratio <br> - Wx0 (e.g., 100x0) - Resize to width W, preserving aspect ratio |
| `--thumb-dir PATH`               | Directory to save thumbnails. Required when --thumb is used.                                                     |
| `--compress [low, medium, high]` | Compression level for the output images.                                                               |
| `--verbose`                      | Enable verbose output during processing.                                                                        |
| `--recursive`                    | Process directories recursively, including subdirectories.                                                      |
| `--remove-metadata`              | Remove EXIF metadata from images.                                                                                |
| `--copyright-text TEXT`          | Add copyright text to the image metadata. Note: Ignored if --remove-metadata is used.                            |

## Examples

## Examples

### Basic Conversion

Convert a single image and overwrite the original after confirmation:

```bash
jpeg-converter path/to/image.jpg
```

### Convert All Images in a Directory

Convert all JPEG images in a directory and save the outputs to another directory:

```bash
jpeg-converter path/to/input_directory --output-dir path/to/output_directory
```

### Batch Conversion with Compression and Metadata Removal

Convert all images with high compression and remove EXIF metadata:

```bash
jpeg-converter path/to/input_directory --compress=high --remove-metadata
```

### Create Thumbnails

Create thumbnails with center cropping:

```bash
jpeg-converter path/to/input_directory --thumb=100x300 --thumb-dir path/to/thumbnails/
```

### Combine Multiple Options

Convert images, create thumbnails, set compression level, enable verbose output, process directories recursively, and add copyright:

```bash
jpeg-converter path/to/input_directory \
  --output-dir path/to/output_directory \
  --thumb=150x150f \
  --thumb-dir path/to/thumbnails/ \
  --compress=medium \
  --recursive \
  --verbose \
  --remove-metadata \
  --copyright-text="© 2024 Your Name"
```

## License

Distributed under the MIT License. See LICENSE for more information.
