import concurrent
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import numpy as np

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger
from pymongo import MongoClient

from sais.autotrain.dataservice.config.const import DEBUG
from sais.autotrain.dataservice.config.mongo_config import mongo_config
from sais.autotrain.dataservice.model.data_model import Coordinate
from sais.autotrain.dataservice.types.biz_exception import BizException
from bson.objectid import ObjectId

def query_nwp_mongo_biz(src: str, start_time: str, ndays: int, hours: int, coords: list[Coordinate], vars: list[str],
                        workers: int):
    nwp_meta = query_nwp_meta_info(src)
    # start_time = get_max_start_time(start_time, nwp_meta['start_time'])
    rule_start_time = get_rule_start_time(start_time)
    nearest_start_time = get_nearest_start_time(rule_start_time, nwp_meta['times'].split(','))
    real_start_time = get_real_start_time(nearest_start_time, nwp_meta.get('latest_time'), ndays)

    period_interval = 24
    period = ndays
    start_hour = calculate_hours_between(real_start_time, start_time)
    end_hour = (start_hour + hours) - 1
    # # 对于没有step0的属于源，需要特殊处理
    # if 'P0DT0H0M0S' not in json.loads(nwp_meta['steps']) and start_hour == 0:
    #     start_hour = 1
    #     end_hour = end_hour + 1
    forecast_interval = 1
    return query_nwp_mongo(src, real_start_time, period_interval, period, start_hour, end_hour,
                           forecast_interval, coords, vars, workers, nwp_meta)


def query_nwp_mongo(src: str, start_time: str, period_interval: int, period: int, start_hour: int, end_hour: int,
                    forecast_interval: int, coords: list[Coordinate], vars: list[str], workers: int,
                    nwp_meta: dict = None):
    if DEBUG:
        logger.debug(
            f'params: src: {src}, start_time: {start_time}, period_interval: {period_interval}, period: {period}, start_hour: {start_hour}, '
            f'end_hour: {end_hour}, forecast_interval: {forecast_interval}, coords: {coords}, vars: {vars}, workers: {workers}')
    # 记录查询开始时间
    query_start_time = time.time()
    # 查询气象源元信息
    if not nwp_meta:
        nwp_meta = query_nwp_meta_info(src)

    # 解析请求参数
    start_time_dt = datetime.strptime(start_time, "%y%m%d%H")
    # 所有起报时间点
    forcast_start_times = []
    # 所有预报时间点
    forcast_times = []
    # 预报步长
    steps = []
    # forcast_time 按月分组
    month_groups = {}
    # 发布时次
    for i in range(period):
        forcast_start_time = start_time_dt + timedelta(hours=i * period_interval)
        # logger.info(f'forcast_start_time: {forcast_start_time}')
        forcast_start_time_str = forcast_start_time.strftime("%Y-%m-%d %H:%M:%S")
        forcast_start_times.append(forcast_start_time_str)
        # 记录到月分组中
        month_key = forcast_start_time.strftime('%Y%m')
        if month_key not in month_groups:
            month_groups[month_key] = []
        month_groups[month_key].append(forcast_start_time_str)

        for hour in range(start_hour, end_hour + 1, forecast_interval):
            current_step = timedelta(hours=hour)
            forcast_time = forcast_start_time + current_step
            # logger.info(f'forcast_time: {forcast_time}')
            forcast_times.append(forcast_time.strftime("%Y-%m-%d %H:%M:%S"))

            # 格式化时间步长
            formatted_step = f"P{current_step.days}DT{current_step.seconds // 3600}H{(current_step.seconds // 60) % 60}M{current_step.seconds % 60}S"
            steps.append(formatted_step)
    # logger.info(f'forcast_times: {forcast_times}')
    # logger.info(f'forcast_start_times: {forcast_start_times}')

    # 获取实际查询的格点
    mapping_coords = approximate_coordinates(coords, nwp_meta['grid'])
    support_steps = json.loads(nwp_meta['steps'])
    valid_steps = [step for step in steps if step in support_steps]

    # 查询气象源数据
    result = query_mongo_multi_thread(workers, nwp_meta, month_groups, valid_steps, vars, mapping_coords)
    current = time.time()  # 记录查询结束时间
    query_time = current - query_start_time
    logger.info(f"查询耗时: {query_time:.2f} 秒")
    # 结果后处理
    result = handle_result(nwp_meta, forcast_start_times, valid_steps, src, start_time, period_interval, period, start_hour,
                           end_hour,
                           forecast_interval, mapping_coords, vars, result)
    all_end_time = time.time()  # 记录查询结束时间
    all_execution_time = all_end_time - query_start_time
    check_result(vars, forcast_start_times, valid_steps, result, nwp_meta)
    logger.info(f"总耗时: {all_execution_time:.2f} 秒")
    return result


def handle_result(nwp_meta: dict, forcast_start_times: list[str], valid_steps: list[str], src: str, start_time: str,
                  period_interval: int, period: int, start_hour: int, end_hour: int,
                  forecast_interval: int, mapping_coords: dict[tuple[float, float], Coordinate], vars: list[str],
                  result):
    if not result or len(result) == 0:
        return result
    df = pd.DataFrame(result)
    df = df.drop_duplicates()
    df = df.sort_values(by=['src', 'time', 'valid_time']).reset_index(drop=True)
    # 按经纬度分组
    grouped = df.groupby(['latitude', 'longitude'])
    # 构建结果列表
    result_list = []
    all_missing_forcast_times = set()
    for (lat, lon), group_df in grouped:
        group_df, missing_forcast_start_times =  find_missing_forcast_start_times(nwp_meta, lat, lon, group_df, forcast_start_times, valid_steps, vars)
        if missing_forcast_start_times:
            all_missing_forcast_times.update(missing_forcast_start_times)
        coor = mapping_coords.get((lat, lon))
        meta = {
            'src': src,
            'start_time': start_time,
            'period_interval': period_interval,
            'period': period,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'forecast_interval': forecast_interval,
            'latitude': lat,
            'longitude': lon,
            'req_lat': coor.req_lat,
            'req_lon': coor.req_lon
        }
        # 构建 data 字典
        var_list_dict = {var: group_df[var].tolist() for var in vars}
        data = {
            # 'step': group_df['step'].tolist(),
            **var_list_dict
        }
        result_list.append({
            'meta': meta,
            'data': data
        })
    if all_missing_forcast_times:
        save_lost_forecast_times(all_missing_forcast_times, nwp_meta)
    return result_list


def check_result(vars, forcast_start_times, steps, result, nwp_meta):
    """
    :param vars: 所有气候变量
    :param forcast_start_times: 所有预报开始时间点
    :param steps 所有steps未去重
    :param result: 预报结果
    :param nwp_meta: 气象源元信息
    :return:
    """
    start_time = datetime.strptime(nwp_meta['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(nwp_meta['end_time'], "%Y-%m-%d %H:%M:%S")

    # 筛选出在指定时间范围内的所有起报时间
    # filtered_fc_start_times = [
    #     ft for ft in forcast_start_times
    #     if start_time <= datetime.strptime(ft, "%Y-%m-%d %H:%M:%S") <= end_time
    # ]
    # 去重步长
    unique_steps = list(set(steps))
    if not result or len(result) == 0:
        raise BizException(code=1, msg="查询结果为空")
    for index, item_result in enumerate(result):
        if not item_result['data']:
            raise BizException(code=2, msg="预报数据为空")
        for var in vars:
            # 检查是否存在该变量的预报数据
            if var not in result[index]['data']:
                raise BizException(code=3, msg=f"预报数据不存在于查询结果中")
            # 检查是否存在该预报时间点的预报数据
            expect_len = len(forcast_start_times) * len(unique_steps)
            real_len = len(result[index]['data'][var])
            if expect_len != real_len:
                raise BizException(code=4,
                                   msg=f"{var} 预报数据长度与预报时间点长度不一致, expect_len: {str(expect_len)}, real_len:{str(real_len)}")


def run_query(db: MongoClient, nwp_meta: dict, month_item: dict, forcast_times: list[str], steps: list[str],
              vars: list[str],
              mapping_coords: dict[tuple[float, float], Coordinate]):
    query_conditions = []

    # 获取近似经纬度
    rounded_coords = [
        {"req_lat": key[0], "req_lon": key[1]}
        for key in mapping_coords.keys()
    ]
    query_conditions.append({
        "src": nwp_meta['src'],
        "time": {"$in": forcast_times},
        "$or": [
            {"$and": [{"latitude": loc['req_lat']}, {"longitude": loc['req_lon']}]} for loc in rounded_coords
        ],
        "step": {"$in": steps},
        "$and": [{var: {"$exists": True}} for var in vars]
    })
    collection = get_collection(db, nwp_meta["prefix"], month_item)
    vars_dict = {key: 1 for key in vars}
    query = {"$and": query_conditions}
    if DEBUG:
        logger.info(f'query: {query_conditions}')
    # logger.info(f'query: {query_conditions}')
    query_results = collection.find(query, {
        "_id": 0,
        "src": 1,
        "time": 1,
        "valid_time": 1,
        "step": 1,
        "latitude": 1,
        "longitude": 1,
        **vars_dict
    }).sort({
        "time": 1,
        "step": 1
    })
    return list(query_results)


def query_mongo_multi_thread(workers, nwp_meta: dict, month_group: dict, steps: list[str], vars: list[str],
                             mapping_coords: dict[tuple[float, float], Coordinate]):
    # 并发查询
    all_results = []
    client = mongo_config.get_client()
    db = client[os.getenv("MONGO_DB", "auto_train")]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_month = {
            executor.submit(run_query, db, nwp_meta, month_key, month_group[month_key], steps, vars,
                            mapping_coords): month_key
            for month_key in month_group
        }
        for future in concurrent.futures.as_completed(future_to_month):
            month_key = future_to_month[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as exc:
                print(f'Error for month {month_key}: {exc}')
    return all_results


def query_nwp_meta_info(src):
    """
    查询气象源元数据
    :param src: 气象源
    :return:
    """
    client = mongo_config.get_client()
    db = client[os.getenv("MONGO_DB", "auto_train")]
    meta_info = db["nwp_infos"].find_one({"src": src})
    if not meta_info:
        raise BizException(code=6, msg=f"未查询到{src}气象源元信息")
    meta_info['_id'] = str(meta_info['_id'])
    return meta_info


def get_collection(db, prefix, year_month):
    cname = f"{prefix}_{year_month}"
    if DEBUG:
        logger.info(f'collection name: {cname}')
    return db[cname]


def get_year_month(dt):
    year_month = dt.strftime("%Y%m")
    return year_month


def get_nearest_start_time(input_time_str, supported_hours):
    """
    获取与给定时刻最近（向前）的起报时间。

    参数:
    input_time_str (str): 输入的时间字符串，格式为 "YYMMDDHH"。
    supported_hours (list): 支持的小时时刻列表，如 ["00", "12"]。

    返回:
    str: 最近的起报时间字符串，格式为 "YYMMDDHH"。
    """
    # 解析输入的时间字符串
    input_time = datetime.strptime(input_time_str, "%y%m%d%H")

    # 找到最近的支持时刻
    nearest_hour = None
    min_diff = None
    for hour in supported_hours:
        # 构建当前支持时刻的时间
        test_time = datetime.strptime(input_time_str[:-2] + hour, "%y%m%d%H")

        # 计算差异
        diff = (input_time - test_time).total_seconds()

        # 只考虑过去的时间
        if diff >= 0 and (min_diff is None or diff < min_diff):
            nearest_hour = hour
            min_diff = diff

    if nearest_hour is None:
        raise ValueError("无法找到最近的支持时刻")

    # 返回最近的起报时间
    return input_time_str[:-2] + nearest_hour


def calculate_hours_between(start_time_str, end_time_str):
    """
    计算两个时间点之间的小时数。

    参数:
    start_time_str (str): 开始时间字符串，格式为 "YYMMDDHH"。
    end_time_str (str): 结束时间字符串，格式为 "YYMMDDHH"。

    返回:
    int: 两个时间点之间的小时数。
    """
    # 解析时间字符串为 datetime 对象
    start_time = datetime.strptime(start_time_str, "%y%m%d%H")
    end_time = datetime.strptime(end_time_str, "%y%m%d%H")

    # 计算时间差
    delta = end_time - start_time

    # 将时间差转换为小时数
    hours = int(delta.total_seconds() / 3600)

    return hours


def approximate_coordinates(coords, grid):
    """
    根据传入的分辨率对经纬度列表进行取舍，并存储在字典中。

    :param coords: 经纬度对象列表，每个对象包含 req_lat 和 req_lon 属性
    :param grid: 分辨率，单位为度
    :return: 存储近似后坐标的字典
    """
    if grid <= 0:
        raise ValueError("分辨率必须大于0")

    factor = 1 / grid
    mapping_coords = {}

    for coord in coords:
        approx_lon = round(coord.req_lon * factor) / factor
        approx_lat = round(coord.req_lat * factor) / factor
        key = (approx_lat, approx_lon)
        if key not in mapping_coords:
            mapping_coords[key] = coord

    return mapping_coords


from datetime import datetime


def get_real_start_time(nearest_start_time: str, latest_time: list, ndays: int) -> str:
    if not latest_time or len(latest_time) == 0:
        return nearest_start_time
    # 将nearest_start_time转换为datetime对象
    nearest_dt = datetime.strptime(nearest_start_time, '%y%m%d%H')
    # 将latest_time列表中的字符串转换为datetime对象
    latest_dts = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S') for t in latest_time]
    # 找到latest_time中最接近nearest_start_time的时间
    closest_dt = min(latest_dts, key=lambda x: abs(x - nearest_dt))
    # 如果nearest_start_time比latest_time中的任何一个都靠前，返回nearest_start_time
    if all(nearest_dt < t for t in latest_dts):
        return nearest_start_time
    # 否则，将最接近的时间转换回yymmddhh格式
    closest_time_str = closest_dt.strftime('%y%m%d%H')
    return closest_time_str


def get_max_start_time(start_time: str, data_start_time: str) -> str:
    # 将start_time转换为datetime对象
    start_dt = datetime.strptime(start_time, '%y%m%d%H')
    # 将data_start_time转换为datetime对象
    data_start_dt = datetime.strptime(data_start_time, '%Y-%m-%d %H:%M:%S')
    # 比较两个时间，返回较大的时间
    max_dt = max(start_dt, data_start_dt)
    # 将较大的时间转换回yymmddhh格式
    max_time_str = max_dt.strftime('%y%m%d%H')
    return max_time_str

def get_max_start_time(start_time: str, data_start_time: str) -> str:
    # 将start_time转换为datetime对象
    start_dt = datetime.strptime(start_time, '%y%m%d%H')
    # 将data_start_time转换为datetime对象
    data_start_dt = datetime.strptime(data_start_time, '%Y-%m-%d %H:%M:%S')
    # 比较两个时间，返回较大的时间
    max_dt = max(start_dt, data_start_dt)
    # 将较大的时间转换回yymmddhh格式
    max_time_str = max_dt.strftime('%y%m%d%H')
    return max_time_str

def get_rule_start_time(start_time: str) -> str:
    # 将start_time转换为datetime对象
    start_dt = datetime.strptime(start_time, '%y%m%d%H')

    new_start_dt = start_dt - timedelta(hours=8)
    new_start_str = new_start_dt.strftime('%y%m%d%H')
    return new_start_str

def find_missing_forcast_start_times(nwp_meta: dict, latitude: float, longitude: float, df: pd.DataFrame,
                                     forcast_start_times: list[str], valid_steps: list[str],
                                     vars: list[str]) -> pd.DataFrame:
    missing_forcast_start_times = set()
    missing_data = []

    for time in forcast_start_times:
        # 过滤出对应时间的数据
        filtered_df = df[df['time'] == time]
        # 获取当前时间的所有step
        current_steps = set(filtered_df['step'])
        # 找到缺失的step
        missing_steps_for_time = set(valid_steps) - current_steps

        # 如果有缺失的step，记录下来
        if missing_steps_for_time:
            missing_forcast_start_times.add(time)

            # 生成缺失数据的行
            for step in missing_steps_for_time:
                row = {
                    'time': time,
                    'step': step,
                    'valid_time': calculate_valid_time(time, step),
                    'src': nwp_meta['src'],
                    'latitude': latitude,
                    'longitude': longitude
                }
                for var in vars:
                    row[var] = np.nan
                missing_data.append(row)

    # 将缺失数据添加到 DataFrame 中
    if missing_data:
        missing_df = pd.DataFrame(missing_data)
        df = pd.concat([df, missing_df], ignore_index=True)
        df = df.sort_values(by=['src', 'time', 'valid_time']).reset_index(drop=True)
    return df, missing_forcast_start_times


def save_lost_forecast_times(missing_forcast_start_times: set, nwp_meta: dict):
    """
    更新缺失的预报时间次
    """
    client = mongo_config.get_client()
    db = client[os.getenv("MONGO_DB", "auto_train")]
    lost_forecast_times = nwp_meta.get('lost_forecast_times', [])
    merged_forecast_times = list(set(lost_forecast_times + list(missing_forcast_start_times)))
    result = db["nwp_infos"].update_one(
        {'_id': ObjectId(nwp_meta['_id'])},
        {'$set': {'lost_forecast_times': merged_forecast_times}}
    )



def parse_step(step: str) -> relativedelta:
    """
    解析step字符串，返回一个relativedelta对象。
    step格式为PnDTnHnMnS，例如P2DT2H0M0S。
    """
    # 去掉开头的P
    step = step[1:]

    # 定义正则表达式来匹配各个部分
    pattern = r'(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, step)

    if not match:
        raise ValueError(f"Invalid step format: {step}")

    groups = match.groups()

    # 解析各部分
    days = int(groups[0]) if groups[0] else 0
    hours = int(groups[1]) if groups[1] else 0
    minutes = int(groups[2]) if groups[2] else 0
    seconds = int(groups[3]) if groups[3] else 0

    return relativedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def calculate_valid_time(time: str, step: str) -> str:
    """
    计算valid_time，给定time和step。
    time格式为YYYY-MM-DD HH:MM:SS，例如2024-08-01 00:00:00。
    step格式为PnDTnHnMnS，例如P2DT2H0M0S。
    返回valid_time，格式为YYYY-MM-DD HH:MM:SS。
    """
    time_dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    step_delta = parse_step(step)
    valid_time_dt = time_dt + step_delta
    return valid_time_dt.strftime('%Y-%m-%d %H:%M:%S')

