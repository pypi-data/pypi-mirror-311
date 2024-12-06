import sys
import os

pythonPath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
if pythonPath not in sys.path:
    sys.path.insert(0, pythonPath)

from qr_codec.qr_code import *
import pandas as pd
from qr_codec.convert_json import map_a_to_b
from datetime import datetime


def save_excel(stat_list, file):
    import pandas as pd
    print('stat_list =', len(stat_list), file)
    df = pd.DataFrame(stat_list)
    
    with pd.ExcelWriter(file) as writer:
        df.to_excel(writer, sheet_name='sheet1')
        df.describe().to_excel(writer, sheet_name='describe') 
    # save to temp
    df2 = df.drop(columns=['file'])
    df2.to_csv(file.replace('.xlsx','_tmp.csv'))
    # save to db
    from  util.code2db import get_conn
    con = get_conn(recycle=True)
    df2.to_sql(name=os.path.basename(file).replace('.xlsx','_tmp'),con=con,if_exists='replace',index=True)


def perf_compare_asn1_avro(fdir):
    ''' 测试两种编码方式的效率
    '''
    import traceback
    stat_list = []
    conf_file = os.path.join(os.path.dirname(__file__), './example/qr.codec.vte.config.yml')
    qr1 = QR_Codec(conf_file, 'avro')
    qr2 = QR_Codec(conf_file, 'asn1')
    for fname in sorted(os.listdir(fdir))[:]:
        if not fname.endswith('.json'):
            continue
        try:
            file_name = os.path.join(fdir, fname)
            obj = load_json(file_name)
            B = map_a_to_b(obj)
            stat = {'file': os.path.basename(file_name)}
            start_date = obj['admissionTime']
            obj.pop('admissionTime', None)
            obj.pop('patientName', None)
            qr1.encode_body(deepcopy(obj), start_date, stat)
            qr2.encode_body(deepcopy(obj), start_date, stat)
            stat_list.append(stat)
        except Exception as e:
            print("Exception", type(e), fname, e)
            print(traceback.format_exc())
            exit()
    save_excel(stat_list, fdir + '.xlsx')


def stat_T1_detail(file):
    ''' 统计测试输入数据的基线情况
    '''
    obj = load_json(file)
    obj = map_a_to_b(obj)
    datetime_fields = {  # 相对于transaction_field字段的天数差
        "operate": "patientOperList",
        "image": "imageologys",
        "lab": "laboratoryList",
        "ass": "dischangeAss",
        "disease": "concomitantDiseases",
        "drug":"dischargeMedications"
    }
    stat = {'file': os.path.basename(file)}
    obj.pop('admissionTime',None)
    obj.pop('patientName',None)
    stat['total_field'] = count_fields(obj)
    stat['total_size'] = len(json.dumps(obj, ensure_ascii=False).encode('utf-8'))
    # stat['total_v_size'] = count_fields_payload(obj)
    stat['base_field'] = stat['total_field']
    stat['base_size'] = stat['total_size']
    # stat['base_v_size'] = stat['total_v_size']
    for k, f in datetime_fields.items():
        child = {f: obj[f]}
        stat[f'{k}_field'] = count_fields(child)
        stat[f'{k}_size'] = len(json.dumps(child, ensure_ascii=False).encode('utf-8'))
        # stat[f'{k}_v_size'] = count_fields_payload(child)
        stat['base_field'] -= stat[f'{k}_field']
        stat['base_size'] -= stat[f'{k}_size']
        # stat['base_v_size'] -= stat[f'{k}_v_size']
    return stat


def stat_t1(xlsx_file):
    '''统计表1的信息，并把t1的结果作为sheet追加写入到excel中
    '''
    df = pd.read_excel(xlsx_file)

    def tl_with_postfix(df, postfix='_field', decimals=1):
        '''根据后缀，统计某些字段的Table one信息
        '''
        import tableone
        field_columns = [c for c in df.columns if postfix in c]
        rename = dict(zip(field_columns, [i.replace(postfix, '') for i in field_columns]))
        t1 = tableone.TableOne(df, missing=False, categorical=[], rename=rename, columns=field_columns,
                               decimals=decimals, overall=True, min_max=field_columns)
        return t1

    # 统计一些字段
    t1_field = tl_with_postfix(df, postfix='_field')
    t1_size = tl_with_postfix(df, postfix='_size', decimals=0)
    t1_ = t1_field.tableone.rename(columns={"Overall": "Field(num)"})
    t2_ = t1_size.tableone.rename(columns={"Overall": "Size(bytes)"})

    def cal_percent(df, cal_column='Field(num)', target='Field(%)'):
        # 获取总数
        total = 0
        for row in df.itertuples():
            if 'total' in row.Index[0]:
                v = df.at[row.Index, cal_column]
                total = float(v.split(' ')[0])
                break
        if total == 0:
            raise Exception('not fount Total for ({cal_column})')
        for row in df.itertuples():
            if " " not in row.Index[0] or 'total' in row.Index[0]:
                df.at[row.Index, target] = ''
                continue
            v = df.at[row.Index, cal_column]
            v = float(v.split(' ')[0])
            df.at[row.Index, target] = f'{v / total * 100:.1f}'

    # 计算百分比
    cal_percent(t1_, cal_column='Field(num)', target='Field(%)')
    cal_percent(t2_, cal_column='Size(bytes)', target='Size(%)')
    t1 = pd.concat([t1_, t2_], axis=1, join="inner")
    # 结果打印
    pd.options.display.max_columns = 5
    # 结果保存在excel中
    with pd.ExcelWriter(xlsx_file, mode="a", engine="openpyxl") as writer:
        t1.to_excel(writer, index=True, sheet_name='t1')


def perf_stat_t1(fdir):
    '''批量任务，统计表1的信息
    '''
    stat_list = []
    for fname in sorted(os.listdir(fdir))[:]:
        if not fname.endswith('.json'):
            continue
        file_name = os.path.join(fdir, fname)
        stat = stat_T1_detail(file_name)
        stat_list.append(stat)
    xlsx_file = fdir + '_t1.xlsx'
    save_excel(stat_list, xlsx_file)
    # stat_t1(xlsx_file)


def xlsx_2_qr_list(xlsx_file, start=0, end=1000, max_qr=1171):
    df = pd.read_excel(xlsx_file)[start:end]
    # 判断是否为数值
    columns = []
    data = []
    for t in df.columns:
        if 'Unnamed' in t:
            continue
        if 'int' not in str(df[t].dtype):
            continue
        columns.append(t)
        data.append(df[t].to_list())
    obj = {
        "data": data, "columns": columns,
        'fileName': os.path.basename(xlsx_file).replace('.xlsx', ''),
        'createTime': datetime.now().strftime('%Y-%m-%d')
    }
    conf_file = os.path.join(os.path.dirname(__file__), './example/qr.codec.excel.config.yml')
    qr = QR_Codec(conf_file, 'avro')
    qr.max_qr_len = max_qr
    stat = {}
    qr_list = qr.encode(obj, stat)
    print(xlsx_file, len(qr_list), stat)
    return qr_list


def convert_xlsx2bytes(xlsx_file):
    '''把xlsx转换为qr的数据
    '''
    # 转换为
    df = pd.read_excel(xlsx_file)
    # 判断是否为数值
    columns = []
    data = []
    for t in df.columns:
        if 'Unnamed' in t:
            continue
        if 'int' not in str(df[t].dtype):
            continue
        columns.append(t)
        data.append(df[t].to_list())
    obj = {"data": data, "columns": columns}
    print(len(df), len(json.dumps(obj, indent=2).encode()))
    # 参考： https://avro.apache.org/docs/++version++/specification/
    json_scheme = {
        #  "namespace": "example.avro",
        "type": "record",
        "name": "User",
        "fields": [
            {"name": "columns",
             "type":
                 {"type": "array",
                  "items": "string"}
             },
            {"name": "data",
             "type":
                 {"type": "array",
                  "items":
                      {"type": "array",
                       "items": "int"}
                  }
             }
        ]
    }
    import avro
    schema = avro.schema.parse(json.dumps(json_scheme))
    encoded_bytes = encode_by_json_serial(obj, schema)
    z_bytes = zlib.compress(encoded_bytes)
    print(xlsx_file, len(df), len(columns), len(json.dumps(obj, indent=2).encode()), len(encoded_bytes), len(z_bytes))


# 写2个api，一个是触发性能分析，一个是获取性能分析文件
# API  /api/v1/qr/perfrun
# 参数?type=avro&&fdir=广西桂东 ===> 后台执行函数perf_compare_asn1_avro(fdir)
# 参数?type=t1&&fdir=广西桂东 ===> 后台执行函数perf_stat_t1(fdir)
# API  /api/v1/qr/perfdata?file=xx.xlsx ===> 读取xx.xlsx，在页面上显示二维码列表
def write_qr2png(qr_list,dir_path,error_correction=1,prefix=""):
    '''
    error_correction的定义跟常识不一致，L为1
    ERROR_CORRECT_L = 1
    ERROR_CORRECT_M = 0
    ERROR_CORRECT_Q = 3
    ERROR_CORRECT_H = 2
    '''
    import qrcode
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for filename in os.listdir(dir_path):
        if filename.endswith('.png'):
          os.unlink(os.path.join(dir_path, filename))
    # 首先清楚fdir目录下的文件
    img_paths =[]
    for i, qr_code in enumerate(qr_list):
        # border = 4 if len(qr_code) < 500 else int(4*len(qr_code)/400)
        # box_size = 10 if len(qr_code) < 500 else int(10*len(qr_code)/400)
        # 转换为 Base64
        # import base64
        # base64_encoded = base64.b64encode(qr_code)
        # # 转换为字符串以便查看
        # base64_string = base64_encoded.decode('utf-8')
        # print(f"{i}Base64 编码：", base64_string)
        border = 0
        box_size = 40 # 图片大一点，这样放大时不会模糊
        qr = qrcode.QRCode(border=border, box_size=box_size, error_correction=error_correction)
        qr.add_data(qr_code, optimize=0)
        qr.make()
        img = qr.make_image()
        print('字符长度', len(qr_code), 'version', qr.version, qr.border, qr.box_size) # 二维码版本对应https://www.qrcode.com/zh/about/version.html
        filename = os.path.join(dir_path,f'{prefix}{len(qr_list):02d}_{i:02d}_{qr.version}.png')
        # 保存图像
        img.save(filename)
        img_paths.append(filename)
    return img_paths


def read_and_recover_json(dir_path, conf_file, prefix=""):
    '''由于python的几个第三方（pyzbar、zxing）解析二维码时，对输出结果为二进制格式的支持不好
    调用了nodejs的库，通过nodejs解析出二进制数值，保卫为临时json
    '''
    file_list = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path) if filename.endswith('.json') and (not prefix or filename.startswith(prefix))]

    qr  = QR_Codec(conf_file)
    for file in file_list:
        # 遍历读png，转换为qr_list
        # 遍历qr_list,判断flag== finished, return r
        v_list = load_json(file)
        _bytes = bytes(v_list)
        print(file,len(_bytes),_bytes)
        flag, r = qr.decode(_bytes,"",True)
        if flag == 'finished':
          print('解码成功',r)
          return r
        else:
          print(f'{file}:{len(_bytes)},flag = {flag}')
    print('解码失败')
    return None

def read_and_recover_xlsx(dir_path, conf_file, prefix=""):
    '''
    '''
    obj = read_and_recover_json(dir_path, conf_file, prefix)
    columns = obj['columns']
    data = obj['data']
    df = pd.DataFrame(data=dict(zip(obj['columns'],obj['data'])))
    file = os.path.join(dir_path,prefix+"_"+datetime.now().strftime('%Y%m%d%H%M%S')+'.xlsx')
    print(file)
    with pd.ExcelWriter(file) as writer:
        df.to_excel(writer, sheet_name='sheet1')


if __name__ == "__main__":
    fdir = '/Users/lcz/git/d/vte_qr/test/codec/广西桂东'
    # fdir = '/Users/lcz/git/d/vte_qr/test/codec/宁波中医院'
    # fdir = '/Users/lcz/git/d/vte_qr/test/codec/浙江中山医院'
    # fdir = '/Users/lcz/git/d/vte_qr/test/codec/新医'
    fdir = './logs/homecare'
    perf_compare_asn1_avro(fdir)
    perf_stat_t1(fdir)
    json_file = os.path.join(os.path.dirname(__file__),'sample.json')
    # stat= stat_T1_detail(json_file)
    # print('stat',stat)
    # perf_stat_t1_detail(fdir)
    xlsx_file  = '/Users/lcz/git/d/vte_qr/test/codec/广西桂东_t1_1019.xlsx'
    # convert_xlsx2bytes(xlsx_file)
    # stat_t1("/Users/lcz/git/d/vte_qr/test/qr_codec_test/六中心_20241025143015_t1.xlsx")
    xlsx_file  = '/Users/lcz/git/d/vte_qr/test/codec/广西桂东_1019.xlsx'
    dir_path  = '/Users/jxu/Desktop/test_900/'
    conf_file = os.path.join(os.path.dirname(__file__), './example/qr.codec.excel.config.yml')
    # qr_list = xlsx_2_qr_list(xlsx_file,173)
    # write_qr2png(qr_list,dir_path)
    read_and_recover_xlsx(dir_path, conf_file, prefix="")