import os
import shutil
from glob import glob
from enum import Enum
import rasterio
from rasterio.transform import Affine
from rasterio.enums import Resampling
import numpy as np

def copy_dir(src, dst, *, follow_sym=True):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    if os.path.isdir(src):
        shutil.copytree(src, dst, symlinks=follow_sym)
        shutil.copystat(src, dst, follow_symlinks=follow_sym)
    return dst

class Upscale(Enum):
    B01 = 6
    B02 = 1
    B03 = 1
    B04 = 1
    B05 = 2
    B06 = 2
    B07 = 2
    B08 = 1
    B8A = 2
    B09 = 6
    B10 = 6
    B11 = 2
    B12 = 2
    SCL = 2

def upscale(filename, outputf):
    head, tail = os.path.split(str(filename))
    band = (tail[-11:-8]).replace('_', '')
    upscale_factor = Upscale[band].value
    if upscale_factor == 2:
        with rasterio.open(filename) as dataset:
            data = dataset.read(
                out_shape=(
                    dataset.count,
                    int(dataset.height * upscale_factor),
                    int(dataset.width * upscale_factor)
                ),
                resampling=Resampling.bilinear
            )
            transform = dataset.transform * dataset.transform.scale(
                (dataset.width / data.shape[-1]),
                (dataset.height / data.shape[-2])
            )
            profile = dataset.profile
            profile.update(
                transform=dataset.transform * Affine.scale(1 / upscale_factor),
                height=data.shape[-2],
                width=data.shape[-1]
            )
            with rasterio.open(outputf, "w", **profile) as resampled:
                resampled.write(data)
# Replace these with your actual source and destination paths
# source = "D:/AgR/SEN2/DATA"
# resample = "D:/AgR/SEN2/outs"
def process_sen2(source, resample):
        
    # Create destination directory if it doesn't exist
    os.makedirs(resample, exist_ok=True)

    # Copy directory structure
    shutil.copytree(source, resample, copy_function=copy_dir, dirs_exist_ok=True)

    # List of jp2 files
    listOfiles = glob(source + '/**', recursive=True)
    FileList = [num for num in listOfiles if ('10m.jp2' in num or '20m.jp2' in num) and 
                ('_B' in num or '_SCL_' in num) and 'B01' not in num]

    print(f"Total files: {len(FileList)}")

    heads, tails = os.path.split(str(source))
    headr, tailr = os.path.split(str(resample))
    tailss = os.sep + tails
    tailrr = os.sep + tailr

    # Process files
    for filename in FileList:
        print('Converting to tif: ', filename)
        
        input_file = filename
        output_file = filename.replace(source, resample).replace('.jp2', '.tif')
        
        with rasterio.open(input_file) as src:
            profile = src.profile.copy()
            profile.update(
                driver='GTiff',
                count=1
            )
            with rasterio.open(output_file, 'w', **profile) as dst:
                for i in range(1, src.count + 1):
                    data = src.read(i)
                    dst.write(data, i)
                    
        output_resample = output_file.replace(os.path.join("/", tails), 
                                            os.path.join("/", tailr)).replace('20m.tif', '10m.tif')
        upscale(output_file, output_resample)
        print(f"Processed: {output_file}")

    # Process folders
    Folderlist = [folder for folder in os.listdir(resample) if folder.endswith(".SAFE")]

    for folder in Folderlist:
        listOfiles = glob(os.path.join(resample, folder + '/**'), recursive=True)
        FileList = [num for num in listOfiles if '10m.tif' in num and '_B' in num]
        
        # Sort bands
        FileList.sort(key=lambda x: x[-10:-8])
        last_element = FileList.pop()
        FileList.insert(7, last_element)
        
        head, tail = os.path.split(FileList[0])
        filename = tail[:-11]
        
        # Stack bands
        with rasterio.open(FileList[0]) as src0:
            meta = src0.meta
        
        meta.update(count=len(FileList))
        outstack = os.path.join(head, filename + 'ALL10m.tif')
        
        with rasterio.open(outstack, 'w', **meta) as dst:
            for id, layer in enumerate(FileList, start=1):
                with rasterio.open(layer) as src1:
                    dst.write_band(id, src1.read(1))
        print(f"{outstack}: Stacking successfully!")
        
        # Cloud removal
        with rasterio.open(outstack) as src:
            if src.count < 10:
                print(f"Not all bands present ABORTING: {filename}")
                continue
                
            bands = [src.read(i) for i in range(1, 11)]
        
        scl = FileList[-1].replace('B12', 'SCL')
        print('scl', scl)
        
        with rasterio.open(scl) as src:
            r_mask = src.read(1)
            
        mask_all = np.isin(r_mask, [4, 7])
        masked_bands = [band * mask_all for band in bands]
        
        outstackmask = os.path.join(head, filename + 'CloudFree.tif')
        meta.update(count=len(masked_bands))
        
        with rasterio.open(outstackmask, 'w', **meta) as dst:
            for id, layer in enumerate(masked_bands, start=1):
                dst.write_band(id, layer)
        print(f"{outstackmask}: Stacking successfully!")
        
        # Copy to output folder
        fdn, fln = os.path.split(outstackmask)
        shutil.copy2(outstackmask, os.path.join(resample, fln))
    return 1
