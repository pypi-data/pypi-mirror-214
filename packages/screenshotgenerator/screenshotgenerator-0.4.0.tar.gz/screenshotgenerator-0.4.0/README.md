# screenshotgenerator
This project aims to automate the selection of video screenshots. It employs `ffmpeg` to generate a pool of screenshots (alternatively, you may supply the screenshots yourself) then calls on two `autogluon` machine learning models to score the screenshots in order to select the best of them. The first model attempts to determine whether a screenshot is focused while the second model attempts to determine whether the screenshot is a portrait (a close-up of one or more people). The focused model's score makes up 75% of the total score while the portrait model's score makes up 25% of the total score.

## Dependencies
The following must be installed on your system:
- [ffmpeg](https://ffmpeg.org/download.html)
- [MediaInfo](https://mediaarea.net/en/MediaInfo)
- [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) (if you're on Windows)

### CUDA
`autogluon` uses the CPU version of PyTorch, by default. If you have a CUDA-enabled GPU, installing the CUDA version of PyTorch may increase prediction speed:
```
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116
```

## Usage
### CLI
#### `screenshotgenerator`
Generates a pool of screenshots then selects the best N screenshots.

```
Usage: screenshotgenerator [OPTIONS]

Options:
  --end-time [%H:%M:%S]           The time at which to stop taking
                                  screenshots. Defaults to 95% of the video
                                  duration, to exclude credits.
  --ffmpeg-path TEXT              The path to ffmpeg. Defaults to 'ffmpeg', 
                                  which requires ffmpeg to be in your path.
  --models-directory TEXT         The path to the directory containing the
                                  autogluon models. If the directory doesn't
                                  exist, the pretrained models will be
                                  downloaded to this location. Defaults to a 
                                  subdirectory in the user data directory.
  --pool-directory TEXT           The directory in which to store the
                                  screenshot pool. Defaults to the temporary 
                                  directory.
  --pool-report-path TEXT         A JSON file detailing the screenshot pool,
                                  sorted by descending preference.
  --pool-size INTEGER             The size of the pool from which to select
                                  screenshots.  [default: 64]
  --portrait-preference [mixed|noportrait|portrait]
                                  Preference regarding portrait screenshots.
                                  [default: portrait]
  --screenshot-count INTEGER      The number of screenshots to select.
                                  [default: 4]
  --screenshot-directory TEXT     The directory into which to copy the
                                  selected screenshots.  [required]
  --silent                        Suppress ffmpeg and autogluon output.
  --start-time [%H:%M:%S]         The time at which to start taking
                                  screenshots.  [default: 00:00:00]
  --video-path TEXT               The path to the video for which to generate
                                  screenshots.  [required]
  --help                          Show this message and exit.
```

##### Example
```
screenshotgenerator --screenshot-directory "B:\Screenshots" --video-path "Z:\Encodes\A Great Movie (2023).mkv --portrait-preference mixed
```

#### `screenshotselector`
Selects the best N screenshots from an existing pool of screenshots.

```
Usage: screenshotselector [OPTIONS]

Options:
  --models-directory TEXT         The path to the directory containing the
                                  autogluon models. If the directory doesn't
                                  exist, the pretrained models will be
                                  downloaded to this location. Defaults to a 
                                  subdirectory in the user data directory.
  --pool-directory TEXT           The directory containing the existing pool
                                  of screenshots.  [required]
  --pool-file-filter TEXT         A "starts with" filter for files in the pool
                                  directory. Defaults to operating on all
                                  files in the pool directory.
  --pool-report-path TEXT         A JSON file detailing the screenshot pool,
                                  sorted by descending preference.
  --portrait-preference [mixed|noportrait|portrait]
                                  Preference regarding portrait screenshots.
                                  [default: portrait]
  --screenshot-count INTEGER      The number of screenshots to select.
                                  [default: 4]
  --screenshot-directory TEXT     The directory into which to copy the
                                  selected screenshots.  [required]
  --silent                        Suppress autogluon output.
  --help                          Show this message and exit.
```

##### Example
```
screenshotselector --pool-directory "B:\Pool" --screenshot-directory "B:\Screenshots" --portrait-preference mixed
```

### Library
#### `generate` function
Generates a pool of screenshots then selects the best N screenshots.

##### Parameters
- **`screenshot_directory: str`**  
The directory into which to copy the selected screenshots.
- **`video_path: str`**  
The path to the video for which to generate screenshots.
- _`end_time: datetime`_  
The time at which to stop taking screenshots. Defaults to 95% of the video duration, to exclude credits.
- _`ffmpeg_path: str`_  
The path to `ffmpeg`. Defaults to 'ffmpeg', which requires `ffmpeg` to be in your path.
- _`models_directory: str`_
The path to the directory containing the autogluon models. Defaults to a subdirectory in the user data directory.  
If the directory doesn't exist, the pretrained models will be downloaded to this location. 
- _`pool_directory: str`_  
The directory in which to store the screenshot pool. Defaults to the temporary directory.
- _`pool_size: int`_  
The size of the pool from which to select screenshots. Defaults to 64.
- _`portrait_preference: PortraitPreference`_  
Preference regarding portrait screenshots. Defaults to `PortraitPreference.PORTRAIT`.
- _`screenshot_count: int`_  
The number of screenshots to select. Defaults to 4.
- _`silent: bool`_  
True to suppress `ffmpeg` and `autogluon` output. Defaults to false.
- _`start_time: datetime`_  
The time at which to start taking screenshots. Defaults to 00:00:00.

##### Returns
`list[Screenshot]` The scored screenshot pool, sorted by descending preference.

##### Example
```
import screenshotgenerator

screenshots = screenshotgenerator.generate(
    screenshot_directory=r"B:\Screenshots",
    video_path=r"Z:\Encodes\A Great Movie (2023).mkv",
    portrait_preference = screenshotgenerator.PortraitPreference.MIXED)
```

#### `select` function
Selects the best N screenshots from an existing pool of screenshots.

##### Parameters
- **`pool_directory: str`**
The directory containing an existing pool of screenshots.
- **`screenshot_directory: str`**  
The directory into which to copy the selected screenshots.
- _`models_directory: str`_
The path to the directory containing the autogluon models. Defaults to a subdirectory in the user data directory.  
If the directory doesn't exist, the pretrained models will be downloaded to this location. 
- _`pool_file_filter: str`_  
A "starts with" filter for files in the pool directory. Defaults to operating on all files in the pool directory.
- _`portrait_preference: PortraitPreference`_  
Preference regarding portrait screenshots. Defaults to `PortraitPreference.PORTRAIT`.
- _`screenshot_count: int`_  
The number of screenshots to select. Defaults to 4.
- _`silent: bool`_  
True to suppress `autogluon` output. Defaults to false.

##### Returns
`list[Screenshot]` The scored screenshot pool, sorted by descending preference.

##### Example
```
import screenshotgenerator

screenshots = screenshotgenerator.select(
    pool_directory=r"B:\Pool",
    screenshot_directory=r"B:\Screenshots",
    portrait_preference = screenshotgenerator.PortraitPreference.MIXED)
```

#### `PortraitPreference` enum
##### Members
- `MIXED`  
- `NO_PORTRAIT`  
- `PORTRAIT`

#### `Screenshot` class
##### Attributes
- `focused_score: float`
- `path: str`
- `portrait_score: float`