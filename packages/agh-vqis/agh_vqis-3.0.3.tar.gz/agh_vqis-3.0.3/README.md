# agh-vqis
A Python package computing a set of image quality indicators (IQIs) for a given input video.

Following IQIs are included in the package:

- A set of 15 Video Quality Indicators (VQIs) developed by the team from AGH. See the following website for more information: https://qoe.agh.edu.pl/indicators/.
- Our Python reimplementation of the Colourfulness IQI. See [this](http://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf) paper for more information regarding this IQI.
- Blur Amount IQI. See [package's Python Package Index web page](https://pypi.org/project/cpbd/) for more information.
- UGC IQI (User-generated content).

**Authors**: Jakub Nawała <[jakub.nawala@agh.edu.pl](mailto:jnawala@agh.edu.pl)>, Filip Korus <[fkorus@student.agh.edu.pl](mailto:fkorus@studnt.agh.edu.pl)>

## Requirements
- ffmpeg - version >= 4.4.2
- Python - version >= 3.9

## Installation
```shell
pip install agh_vqis
```

### Usage
1. Single multimedia file:
    ```python
    from agh_vqis import process_single_mm_file, VQIs
    from pathlib import Path
    
    if __name__ == '__main__':
        process_single_mm_file(Path('/path/to/single/video.mp4'))
    ```


2. Folder with multimedia files:
    ```python
    from agh_vqis import process_folder_w_mm_files, VQIs
    from pathlib import Path
    
    if __name__ == '__main__':
        process_folder_w_mm_files(Path('/path/to/multimedia/folder/'))
   ```


3. Options parameter - in either `process_single_mm_file` and `process_folder_w_mm_files` function options could be provided as an optional argument. It is being passed to function as a dictionary like below.
    ```python
     process_single_mm_file(Path('/path/to/single/video.mp4'), options={
          VQIs.contrast: False,  # disable contrast indicator
          VQIs.colourfulness: False,  # disable colourfulness indicator
     })
    ```
   

4. How to disable/enable indicators to count? Every indicator is **enabled by default except `blue_amount`** due to long computing time. To disable one of following indicators `(blockiness, SA, letterbox, pillarbox, blockloss, blur, TA, blackout, freezing, exposure, contrast, interlace, noise, slice, flickering, colourfulness, ugc)` pass 
   ```python
   VQIs.indicator_name: False
   ```
   to options dictionary. Whereas to **enable** `blur_amount` indicator pass `True` value.


5. agh-vqis package could be used from command line interface as well. For example:
   ```shell
   python3 -m agh_vqis /path/to/single/movie.mp4 # will run VQIS for single file
   ```
   or
   ```shell
   python3 -m agh_vqis /path/to/multimedia/folder/ # will run VQIS for folder
   ```
   Whereas this command will display help:
   ```shell
   $ python3 -m agh_vqis -h
   ```
6. Supported multimedia files: `mp4`, `y4m`, `mov`, `mkv`, `avi`, `ts`, `jpg`, `jpeg`, `png`, `gif`, `bmp`.


7. First row of the output CSV file contains header with image quality indicators (IQIs) names, whereas each row below the header represents single video frame from the input video file. Each column provides a numerical result as returned by a given IQI when applied to the respective frame.


8. Cast chosen indicators for different resolutions (**experimental**). For example: to cast Blur to 1440p and Blockiness to 2160p you should pass two additional lines in `options` dictionary like below.
```python
    from agh_vqis import process_single_mm_file, CastVQI, DestResolution
    from pathlib import Path
    
    if __name__ == '__main__':
        process_single_mm_file(Path('/path/to/single/video.mp4'), options={
           CastVQI.blur: DestResolution.p1440,
           CastVQI.blockiness: DestResolution.p2160
        })
   ```

   ### Available casts
   ##### Blockiness:
   - 1080p -> 1440p
   - 1080p -> 2160p
   - 1440p -> 2160p
   - 2160p -> 1440p

   ##### Blur:
   - 1080p -> 1440p
   - 1080p -> 2160p
   - 1440p -> 1080p
   - 1440p -> 2160p
   - 2160p -> 1080p
   - 2160p -> 1440p
   - 240p -> 360p
   - 240p -> 480p
   - 360p -> 240p
   - 360p -> 480p
   - 360p -> 720p
   - 480p -> 240p
   - 480p -> 360p
   - 480p -> 720p
   - 720p -> 1080p
   - 720p -> 360p
   - 720p -> 480p

   ##### Contrast:
   - 1080p -> 1440p
   - 1080p -> 2160p
   - 1080p -> 240p
   - 1080p -> 360p
   - 1080p -> 480p
   - 1080p -> 720p
   - 1440p -> 1080p
   - 1440p -> 2160p
   - 1440p -> 240p
   - 1440p -> 360p
   - 1440p -> 480p
   - 1440p -> 720p
   - 2160p -> 1080p
   - 2160p -> 1440p
   - 2160p -> 240p
   - 2160p -> 360p
   - 2160p -> 480p
   - 2160p -> 720p
   - 240p -> 1080p
   - 240p -> 1440p
   - 240p -> 2160p
   - 240p -> 360p
   - 240p -> 480p
   - 240p -> 720p
   - 360p -> 1080p
   - 360p -> 1440p
   - 360p -> 2160p
   - 360p -> 240p
   - 360p -> 480p
   - 360p -> 720p
   - 480p -> 1080p
   - 480p -> 1440p
   - 480p -> 2160p
   - 480p -> 240p
   - 480p -> 360p
   - 480p -> 720p
   - 720p -> 1080p
   - 720p -> 1440p
   - 720p -> 2160p
   - 720p -> 240p
   - 720p -> 360p
   - 720p -> 480p
   
   ##### Exposure(bri):
   - 1080p -> 1440p
   - 1080p -> 2160p
   - 1080p -> 360p
   - 1080p -> 480p
   - 1080p -> 720p
   - 1440p -> 1080p
   - 1440p -> 2160p
   - 1440p -> 480p
   - 1440p -> 720p
   - 2160p -> 1080p
   - 2160p -> 1440p
   - 2160p -> 720p
   - 240p -> 360p
   - 240p -> 480p
   - 240p -> 720p
   - 360p -> 1080p
   - 360p -> 240p
   - 360p -> 480p
   - 360p -> 720p
   - 480p -> 1080p
   - 480p -> 1440p
   - 480p -> 240p
   - 480p -> 360p
   - 480p -> 720p
   - 720p -> 1080p
   - 720p -> 1440p
   - 720p -> 2160p
   - 720p -> 240p
   - 720p -> 360p
   - 720p -> 480p
   
   ##### Interlace:
   - 1080p -> 1440p
   - 240p -> 360p
   - 360p -> 240p
   - 360p -> 480p
   - 480p -> 360p
   - 480p -> 720p
   - 720p -> 1080p
   - 720p -> 480p
   
   ##### Noise:
   - 1080p -> 1440p
   - 1080p -> 2160p
   - 1440p -> 1080p
   - 1440p -> 2160p
   - 2160p -> 1440p
   - 240p -> 360p
   - 360p -> 240p
   - 360p -> 480p
   - 480p -> 360p
   - 480p -> 720p
   - 720p -> 480p

### License
The `agh-vqis` Python package is provided via the [Evaluation License Agreement](https://app.qoe.agh.edu.pl/public/agh-vqis/license.txt).
