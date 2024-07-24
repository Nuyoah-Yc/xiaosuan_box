import pandas as pd
from pyecharts.charts import Map, Pie, Bar
from pyecharts import options as opts

# 加载并清洗数据
def clean_data(file_path):
    data = pd.read_csv(file_path, encoding='gbk')

    # 删除无关列
    columns_to_drop = ['address_admin_area', 'address_country_code', 'address_locality', 'address_sublocality', 'address_latitude', 'address_longitude']
    data_cleaned = data.drop(columns=columns_to_drop)

    # 转换日期时间字段
    data_cleaned['timestamp'] = pd.to_datetime(data_cleaned['timestamp'], unit='s', errors='coerce')
    data_cleaned['create_time'] = pd.to_datetime(data_cleaned['create_time'], errors='coerce')

    # 标准化文本字段
    data_cleaned['device_key'] = data_cleaned['device_key'].str.lower()
    data_cleaned['cf_connecting_ip'] = data_cleaned['cf_connecting_ip'].str.lower()

    # 筛选出表示OAuth令牌的Cookie值为空和表示服务器返回403禁止访问错误的内容
    filter_conditions = data_cleaned['error_message'].str.contains("403", na=False) | data_cleaned['error_message'].str.contains("OAuth令牌的Cookie值为空", na=False)
    filtered_data = data_cleaned[filter_conditions]

    # 根据device_key字段去重
    filtered_data = filtered_data.drop_duplicates(subset='device_key')

    return filtered_data

# 地图可视化
def create_map(data_cleaned):
    province_data = data_cleaned['ip_city'].value_counts().reset_index().values.tolist()
    map_chart = (
        Map()
        .add("IP城市分布", province_data, "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="IP城市分布"),
            visualmap_opts=opts.VisualMapOpts(max_=150),
        )
    )
    map_chart.render('map_chart.html')

# 饼图可视化
def create_pie(data_cleaned):
    error_data = data_cleaned['error_message'].value_counts().reset_index().values.tolist()
    pie_chart = (
        Pie()
        .add("", error_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="错误类型用户数量"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # 下边添加一个时间标题
        .set_global_opts(
            title_opts=opts.TitleOpts(title="错误类型用户数量", subtitle="时间周期：2024/5/30 21:48:00-2024/6/11 15:47:00")
        )
    )
    pie_chart.render('pie_chart.html')

# 条形图可视化
def create_bar(data_cleaned):
    device_data = data_cleaned['model'].value_counts().reset_index().values.tolist()
    bar_chart = (
        Bar()
        .add_xaxis([x[0] for x in device_data])
        .add_yaxis("设备型号分布", [x[1] for x in device_data])
        .set_global_opts(title_opts=opts.TitleOpts(title="设备型号分布"))
    )
    bar_chart.render('bar_chart.html')

def main():
    file_path = 'oa_bury_event_202406111850.csv'
    data_cleaned = clean_data(file_path)
    print(data_cleaned.head())  # 显示清洗后的数据

    create_map(data_cleaned)
    create_pie(data_cleaned)
    create_bar(data_cleaned)

if __name__ == "__main__":
    main()
