from mosaic.mosaic import idw_mosaic
import rioxarray as rxr

DATA1 = "test/data/DOM_01_WaterDepth_Future2050_S1_Tr10_t33.tif"
DATA2 = "test/data/DOM_02_WaterDepth_Future2050_S1_Tr10_t33.tif"

def test_mosaic():
    ds1 = rxr.open_rasterio(DATA1).isel(band=0)
    ds2 = rxr.open_rasterio(DATA2).isel(band=0)
    
    idw_mosaic(ds1, ds2)
    
if __name__ == "__main__":
    test_mosaic()