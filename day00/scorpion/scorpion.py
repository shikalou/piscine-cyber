from PIL import Image, ExifTags
import sys
import os
from datetime import datetime


def timeConvert(atime):
  dt = atime
  newtime = datetime.fromtimestamp(dt)
  return newtime.date()


def main():
    try:
        for i in range(1, len(sys.argv)):
            print("\n")
            img = Image.open(sys.argv[i])
            info_dict = {
                "Filename": img.filename,
                "Creation Date": timeConvert(os.path.getctime(sys.argv[1])),
                "Image Size": img.size,
                "Image Height": img.height,
                "Image Width": img.width,
                "Image Format": img.format,
                "Image Mode": img.mode,
                "Image is Animated": getattr(img, "is_animated", False),
                "Frames in Image": getattr(img, "n_frames", 1)
            }
            for label,value in info_dict.items():
                print(f"{label:25}: {value}")
            img_exif = img.getexif()
            for tid in img_exif:
                tag = ExifTags.TAGS.get(tid, tid)
                data = img_exif.get(tid)
                if isinstance(data, bytes):
                    data = data.decode()
                print(f"{tag:25}: {data}")
    except Exception as msg:
        print(msg)

if __name__ == "__main__":
    main()
