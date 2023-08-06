import json
import logging
import math
import os

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, validator, root_validator, Field

import geopandas as gpd
import numpy as np

try:
    import ogr
except:
    from osgeo import ogr

log = logging.getLogger(__name__)



@dataclass
class Tile:
    name: str
    epsg: int
    count: int

@dataclass
class Services:
    sub: List[str] = field(default_factory=list)
    dst: List[str] = field(default_factory=list)
    parcel_id: str = field(default_factory=str)
    FOI: List[str] = field(default_factory=list)


@dataclass
class DataObject:
    tiles: List[Tile]
    services: Dict[str, Services]
    pixel: Dict[str, int]
    kult_conversion_table_name: Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel : int

    def get_service_info(self, service_name):
        for serivce_item_name, serive_attribute in self.services.items():
            if serivce_item_name == service_name:
                return serive_attribute

    def get_tile_info(self, tile_name):
        if self.tiles is not None:
            for tile_name_item in self.tiles:
                if tile_name_item.name == tile_name:
                    return tile_name_item
        else:
            return None

class DataObjectModel(BaseModel):
    tiles: Optional[List[Tile]]
    services: Dict[str, Services]
    pixel: Dict[str, int] =  Field({})
    kult_conversion_table_name : Optional[str]
    conversion_table_original_column: Optional[str]
    conversion_table_target_column: Optional[str]
    classification_support_data: Optional[Path]
    min_parcel: int = Field(2000)

    @validator('services', pre=True)
    def convert_to_services_objects(cls, value):
        return {k: Services(**v) for k, v in value.items()}

def open_json(path: Union[Path, str]):
    with open(path, 'r') as file:
        return json.load(file)

class Config(BaseModel):
    tiles: Optional[List]
    services: dict

def create_object(config_path):
    # Parsing the JSON data and creating the object
    parsed_object = DataObjectModel.parse_obj(open_json(config_path))
    data_object = DataObject(**parsed_object.dict())
    return data_object



#############################################################

def return_eodata_tilename(tilename):
    if "-" in tilename:
        eodata_tilename = tilename.split("-")[0]
        return eodata_tilename
    else:
        return tilename

def get_tile_list(tile_gpkgfilepath):
    master_df = gpd.read_file(str(tile_gpkgfilepath))
    return master_df.sitecode.to_list()

def compile_service_project_env_time_sub_folder_relpath(parent_folder, service, project, environment, analysis_time, subfolder_type= None):
    if subfolder_type is not None:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time), str(subfolder_type).upper())
    else:
        service_folder = parent_folder.joinpath(str(service).lower(), str(project).upper(), str(environment).upper(),
                                            str(analysis_time))
    return service_folder


def compile_output_dir(parent_folder, service_name, environment, project, analysis_time, tilename, sub_dir=None):
    parent_output_folder = Path(parent_folder).joinpath("output")
    output_dir = compile_service_project_env_time_sub_folder_relpath(parent_output_folder, service_name, project, environment, analysis_time, sub_dir)
    output_dir_tile = output_dir.joinpath(tilename)
    return output_dir_tile

###############################################################################
def get_gpkg_epsg(gpkg_path):
    source = ogr.Open(str(gpkg_path), update=False)
    layer = source.GetLayer()
    epsg = layer.GetSpatialRef().GetAuthorityCode(None)
    source = None
    layer = None
    return epsg



def split_geodataframe(gdf, subtiles_count, min_rows = 2000):
    total_rows = len(gdf)
    if min_rows is None:
        min_rows = total_rows/subtiles_count
    max_rows_per_split = math.ceil(max(min_rows, total_rows/subtiles_count))
    splits = []
    for i in range(subtiles_count):
        start_idx = i * max_rows_per_split
        end_idx = min((i + 1) * max_rows_per_split, total_rows)
        split_gdf = gdf.iloc[start_idx:end_idx]
        splits.append(split_gdf)
    return splits


def do_split_save_gpkg(input_gpkg, output_gpkg_basename, output_dir,
                       subtiles_count=14, min_parcels = None):

    logfilepath = output_dir.joinpath("tiling_log.txt")
    logfile = open(logfilepath, "w")
    logfile.write("--------------------------------\n")
    logfile.write("-SUBTILE PARCEL COUNT-\n")
    logfile.write("--------------------------------\n")

    gpkg_filename = Path(input_gpkg).name
    gpkg_ds = ogr.Open(str(input_gpkg))

    # Get the number of parcels
    layer_name = gpkg_ds.GetLayer().GetName()
    feature_count = gpkg_ds.GetLayer().GetFeatureCount()

    # Load the GeoPackage file into a GeoDataFrame
    gdf = gpd.read_file(input_gpkg, layer=layer_name)

    if min_parcels is None:
        # Divide the GeoDataFrame into n equal parts
        gdfs = np.array_split(gdf, subtiles_count)
    else:
        gdfs = split_geodataframe(gdf, subtiles_count, min_parcels)
    gpgk_paths = []
    # Write each subset of data to a new GeoPackage file
    parcel_count = 0
    for gdf_index, gdf_subset in enumerate(gdfs):

        number_of_parcels = len(gdf_subset)
        parcel_count += number_of_parcels

        if number_of_parcels !=0:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}.gpkg"))
            output_file.unlink(missing_ok=True)
            layer_name = gpkg_filename.replace(".gpkg", f"_{gdf_index+1}.gpkg")
            gdf_subset.to_file(output_file, layer=layer_name, driver='GPKG')
            gpgk_paths.append(output_file)
        else:
            output_file = output_dir.joinpath(output_gpkg_basename.replace(".gpkg", f"-{gdf_index + 1}_NODATA.txt"))
            output_file.unlink(missing_ok=True)
            output_file.write_text("No parcel")
            gpgk_paths.append(output_file)
        logfile.write(f"{output_file} -- {number_of_parcels} \n")
    logfile.write("--------------------------------\n")
    logfile.write(f"PARCEL COUNT = {parcel_count}\n")
    logfile.close()
    return gpgk_paths

class Merge():
    def __init__(self, project, environemt, yearmonth, service, bioregion, classification_support_data=None, sar_type= None):
        self.project = str(project).upper()
        self.environemt = str(environemt).upper()
        self.yearmonth = str(yearmonth)
        self.service = str(service).upper()
        self.sar_type = str(sar_type).upper()
        self.bioregion = str(bioregion).upper()
        self.year = self.yearmonth[0:4]
        self.classification_support_data = classification_support_data

    def get_config_path(self, parent_folder):
        config_path = parent_folder.joinpath("project_info", self.project, f"{self.bioregion}_config.json")
        if config_path.exists():
            log.info(f"{config_path} exists.")
            return config_path
        else:
            raise Exception(f"{config_path} doesnt exists.")

    def set_bioregion_path(self, parent_folder):
        gpkg_filepath = parent_folder.joinpath("tiles", self.project, f"{self.bioregion}_tiles.gpkg")
        if gpkg_filepath.exists():
            log.info(f"{gpkg_filepath} exists.")
            self.region_gpkg = gpkg_filepath
            return gpkg_filepath
        else:
            raise Exception(f"{gpkg_filepath} doesnt exists.")

    def set_epsg(self, template_gpkg):
        epsg = get_gpkg_epsg(template_gpkg)
        self.epsg = epsg


def create_submit_tile_instance(project, environment, yearmonth, service, bioregion, parent_folder, tile_name = None, tool_service = None):
    mi = Merge(project=project, environemt=environment, yearmonth=yearmonth, service=service, bioregion=bioregion, classification_support_data=None)
    mi.set_bioregion_path(parent_folder)

    config_path = mi.get_config_path(parent_folder)
    config = create_object(config_path)

    service_attributes = config.get_service_info(service)
    service_gpkg_dst = service_attributes.dst

    if len(service_gpkg_dst) == 1:
        dst_tool = service_gpkg_dst[0]
    else:
        if tool_service is None:
            raise Exception(f"tool_service is none")
        else:
            if tool_service in service_gpkg_dst:
                dst_tool = tool_service
            else:
                raise Exception(f"{tool_service} not in dst list")

    if tile_name is None:
        tilename_list = []
        tile_list = get_tile_list(mi.region_gpkg)
        for tile_name in tile_list:
            eodata_tilename = return_eodata_tilename(tile_name)
            for service_gpkg_dst_item in service_gpkg_dst:
                if not service_gpkg_dst_item == tool_service:
                    continue
                output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                                mi.yearmonth,
                                                eodata_tilename, sub_dir=None)
            output_dir_filelist = os.listdir(output_dir)
            output_dir_filelist = [i for i in output_dir_filelist if i.endswith('.gpkg')]
            output_dir_filelist_len = len(output_dir_filelist)

            for subtile_count in range(output_dir_filelist_len):
                tilename_list.append(f"{eodata_tilename}-{subtile_count + 1}")

    else:
        eodata_tilename = return_eodata_tilename(tile_name)
        for service_gpkg_dst_item in service_gpkg_dst:
            if not service_gpkg_dst_item == tool_service:
                continue
            output_dir = compile_output_dir(parent_folder, service_gpkg_dst_item, mi.environemt, mi.project,
                                            mi.yearmonth,
                                            eodata_tilename, sub_dir=None)
        output_dir_filelist =  os.listdir(output_dir)
        output_dir_filelist  = [i for i in output_dir_filelist if i.endswith('.gpkg')]
        output_dir_filelist_len = len(output_dir_filelist)

        tilename_list = []
        for subtile_count in range(output_dir_filelist_len):
            tilename_list.append(f"{eodata_tilename}-{subtile_count+1}")

    return tilename_list