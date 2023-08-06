import os.path

from lm_datahandler.data_download.data_download import download_lm_data_from_server
from lm_datahandler.datahandler import DataHandler


def download_and_full_analyse(download_params):
    save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, save_path)
    for data in data_list:
        data_handler = DataHandler()

        data_name = data
        data_path = os.path.join(save_path, data_name)

        sleep_fig_save_path = os.path.join(data_path, "sleep_fig.png")
        slow_wave_stim_sham_plot = os.path.join(data_path, "sw_stim_sham_fig.png")

        slow_wave_excel_save_path = os.path.join(data_path, "sw.csv")
        spindle_excel_save_path = os.path.join(data_path, "sp.csv")

        # 数据加载
        data_handler.load_data(data_name=data_name, data_path=data_path)

        # 绘制慢波增强对比图，并保存
        data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess().sleep_staging().compute_sleep_variables().plot_sleep_data(savefig=sleep_fig_save_path)

        # spindle检测和慢波检测，并导出结果成excel
        data_handler.spindle_detect().export_sp_results(slow_wave_excel_save_path)
        data_handler.sw_detect().export_sw_results(spindle_excel_save_path)

        data_handler.show_plots()


if __name__ == '__main__':
    download_param = {
        # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
        'paradigms': [1, 2, 3, 4],
        # 用户手机号
        'phones': None,
        # 基座mac
        'macs': None,
        # 服务版本
        'serviceVersions': None,
        # 睡眠主观评分，1~5，-1表示未评分
        'sleepScores': None,
        # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
        'stopTypes': None,
        # 时间范围，以停止记录的时间为准
        'dateRange': ['20230620', '20230620'],
        # 数据时长范围
        'dataLengthRange': [60 * 1, 60 * 12],
        # 翻身次数范围
        'turnoverCountRange': None,
        # 刺激次数范围
        'stimulationCountRange': None,
        'save_path': 'E:/dataset/x7_new/matlab_data'
    }
    download_and_full_analyse(download_param)
