import os
import re
import shutil
import threading
import time

import numpy as np
import requests
import rpy2.robjects as robjects
from bs4 import BeautifulSoup
from rpy2.robjects import pandas2ri
from tensorflow.python.keras import backend as K
from tensorflow.python.keras import initializers, regularizers, constraints
from tensorflow.python.keras.layers import *

A_LIST = ('A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y')
TIME_SLEEP = 1

def get_feature_from_proteinrecon(name, sequence, is_non_redundancy=False):
    """
    从 protein recon中获取数据
    ! 网站可能无法访问
    :param name: 序列名称，e.g. ">P0001"
    :param sequence: 序列
    :param is_non_redundancy: 是否为 psi 准备
    :return: (属性名称, 属性)
    """

    if not name.startswith(">"):
        name = "> " + name
    url = "http://reccr.chem.rpi.edu/cgi-bin/recon.cgi"
    payload = {
        "TAE": "All",
        "format": "fasta",
        "fasta": "%s\n%s" % (name, sequence),
        "pdb": ""
    }
    try:
        response = requests.post(url, data=payload)
        time.sleep(TIME_SLEEP)
        data = str(response.text)
        soup = BeautifulSoup(data, "html.parser")
        context = soup.get_text().strip()

        context = context.split("\n")
        tmp = context[-1].split(",")
        if not name[1:].startswith(tmp[0]):
            raise RuntimeError("氨基酸名称不匹配, 目标 %s，实际 %s" % (name[1:], tmp[0]))
    except requests.exceptions.ConnectionError as e:
        tmp = [0]*141
    f_name = "AA,Population,VOLTAE,SurfArea,DRNA1,DRNA2,DRNA3,DRNA4,DRNA5,DRNA6,DRNA7,DRNA8,DRNA9,DRNA10,DKNA1,DKNA2,DKNA3,DKNA4,DKNA5,DKNA6,DKNA7,DKNA8,DKNA9,DKNA10,DGNA1,DGNA2,DGNA3,DGNA4,DGNA5,DGNA6,DGNA7,DGNA8,DGNA9,DGNA10,SIKA1,SIKA2,SIKA3,SIKA4,SIKA5,SIKA6,SIKA7,SIKA8,SIKA9,SIKA10,SIGA1,SIGA2,SIGA3,SIGA4,SIGA5,SIGA6,SIGA7,SIGA8,SIGA9,SIGA10,SIEPA1,SIEPA2,SIEPA3,SIEPA4,SIEPA5,SIEPA6,SIEPA7,SIEPA8,SIEPA9,SIEPA10,EP1,EP2,EP3,EP4,EP5,EP6,EP7,EP8,EP9,EP10,PIP1,PIP2,PIP3,PIP4,PIP5,PIP6,PIP7,PIP8,PIP9,PIP10,PIP11,PIP12,PIP13,PIP14,PIP15,PIP16,PIP17,PIP18,PIP19,PIP20,Fuk1,Fuk2,Fuk3,Fuk4,Fuk5,Fuk6,Fuk7,Fuk8,Fuk9,Fuk10,Lapl1,Lapl2,Lapl3,Lapl4,Lapl5,Lapl6,Lapl7,Lapl8,Lapl9,Lapl10,SIDRN,SIDKN,SIDGN,SIK,SIG,SIEP,Fuk,Lapl,DRNMin,DRNMax,DKMin,DKMax,DGNMin,DGNMax,SIKMin,SIKMax,SIGMin,SIGMax,SIEPMin,SIEPMax,PIPMin,PIPMax,PIPAvg,FukMin,FukMax,LaplMin,LaplMax".split(
        ",")[1:]
    f_data = tmp[1:]
    f_data = [float(i) for i in f_data]
    if not (len(f_name) == len(f_data) == 140):
        raise RuntimeError("获取到的特征数目不正确")
    return f_name, f_data

def get_feature_from_prodcal(name, sequence, is_non_redundancy=False):
    """
    使用 prodcal 工具计算出的属性
    :param name: 序列名称，e.g. ">P0001"
    :param sequence: 序列
    :param is_non_redundancy: 是否为 psi 准备
    :return: (属性名称, 属性)
    """
    if not name.startswith(">"):
        name = ">" + name
    name = name.replace(" ", "")
    # 修改工作目录为 prodcal 工作目录
    true_workspace = os.getcwd()
    print(true_workspace)
    dirname = os.path.dirname(__file__)  # 此文件所在目录
    prodcal_workspace = os.path.join(dirname, "ProtDCal")
    os.chdir(prodcal_workspace)

    # 可执行文件路径
    protdcal_path = os.path.join(prodcal_workspace, "ProtDCal.jar")
    if not os.path.isfile(protdcal_path):
        raise RuntimeError("ProtDcal.jar 文件不存在")

    # 输入目录, 如果已经存在则删除其中的文件，如果没有存在则创建
    input_dir_path = os.path.join(prodcal_workspace, "Inputs", time.strftime("psi-%Y%m%d"))
    if not os.path.exists(input_dir_path):
        os.makedirs(input_dir_path)
    else:
        _files = os.listdir(input_dir_path)
        for f in _files:
            f = os.path.join(input_dir_path, f)
            os.remove(f)

    # 创建 fasta 输入文件
    fasta_file_path = os.path.join(input_dir_path, "psi_predict.fasta")
    with open(fasta_file_path, "w") as f:
        f.write("%s\n%s" % (name, sequence))

    # 输出目录, 如果已经存在则删除其中的文件，如果没有存在则创建
    output_dir_path = os.path.join(prodcal_workspace, "Outputs", time.strftime("psi-%Y%m%d"))
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    else:
        _files = os.listdir(output_dir_path)
        for f in _files:
            f = os.path.join(output_dir_path, f)
            if os.path.isfile(f):
                os.remove(f)
            else:
                shutil.rmtree(f)

    # 创建工程文件
    proj_path = os.path.join(prodcal_workspace, "Projects", "psi_predict.proj")
    proj_file_context = """directory:
        {}
        indices:
Gw(U),Gs(U),W(U),Mw,HP,IP,ECI,L1-9,DHf,Z1,Z2,Z3,ISA,Xi,Ap,Pa,Pb,Pt,
cdk:
Energy,
groups:
PRT,
invariants:
N1,
parameters(t_cont,s_cont,A%,HydGroup,n,bins,K,SubG):
4.0,8.0,5.0,9.4,3.0,50,5,3
options(decimals,harmonicMeanType,geometricMeanType,windexID,datasetType,outputOrder):
3,0,0,-1,fasta,true
                """
    proj_file_context = proj_file_context.strip()  # 删除空格
    proj_file_context = proj_file_context.format(input_dir_path)  # 填写输入路径
    with open(proj_path, "w") as f:
        f.write(proj_file_context)

    # 执行命令
    # os.system('java -jar ProtDCal.jar -p abhishek_project_corrected.proj -o OutPuts/')
    commend = "java -Xmx1000m -jar {} -p {} -o {}".format(protdcal_path, proj_path, output_dir_path)
    os.system(commend)
    # 恢复工作目录
    os.chdir(true_workspace)

    # 读出结果
    output_file_path = os.path.join(output_dir_path, "psi_predict", "psi_predict_Prot.txt")
    # 这里可能会由于计算时间过长，并没有出现结果，需要添加重试次数
    for i in range(10):
        if os.path.exists(output_file_path):
            break
        time.sleep(1)
    if not os.path.exists(output_file_path):
        raise RuntimeError("结果文件不存在 %s" % output_file_path)

    with open(output_file_path) as f:
        # 第一行是名称，第二行是数据
        data = f.readline()
        f_name = data.strip().split("\t")[1:]
        data = f.readline()
        f_data = data.strip().split("\t")[1:]
        f_data = [float(i.replace(",", "")) for i in f_data]

    return f_name, f_data

def get_feature_from_protparam(name, sequence, is_non_redundancy=False):
    """
    从 protparam(web) 中获取数据
    :param name: 序列名称，e.g. ">P0001"
    :param sequence: 序列
    :param is_non_redundancy: 是否为 psi 准备
    :return: (属性名称, 属性)
    """
    if not name.startswith(">"):
        name = "> " + name
    url = 'https://web.expasy.org/cgi-bin/protparam/protparam'
    payload = {
        "sequence": sequence
    }
    response = requests.post(url, data=payload)
    data = str(response.text)
    soup = BeautifulSoup(data, "html.parser")
    context = soup.get_text()

    amino_list = ['Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu', 'Gly', 'His', 'Ile', 'Leu', 'Lys', 'Met', 'Phe',
                  'Pro',
                  'Ser', 'Thr', 'Trp', 'Tyr', 'Val']
    c_h_n_o_s_list = ['Carbon', 'Hydrogen', 'Nitrogen', 'Oxygen', 'Sulfur']

    num_of_aa = re.search("Number of amino acids:.*?(\d+)", context).group(1)
    molecular_weight = re.search("Molecular weight:.*?([0-9.]+)", context).group(1)
    theoretical_pi = re.search("Theoretical pI:.*?([0-9.]+)", context).group(1)
    aa_composition = re.findall("(\w+)\s+\((.)\)\s+(\d+)\s+([0-9.]+)%", context)
    aa_composition = [i for i in aa_composition if i[0] in amino_list]
    atomic_composition = re.findall("(\w+)\s+(\w)\s+(\d+)", context)
    atomic_composition = [i for i in atomic_composition if i[0] in c_h_n_o_s_list]

    # 保存结果
    f_name = [
                 "Number of amino acids",
                 "Molecular weight",
                 "Theoretical pI",
             ] + [
                 "count(%s)" % i[1] for i in aa_composition
             ] + [
                 "Atomic composition for %s(%s)" % (i[0], i[1]) for i in atomic_composition
             ]
    f_data = [
                 int(num_of_aa),
                 float(molecular_weight),
                 float(theoretical_pi)
             ] + [
                 int(i[2]) for i in aa_composition
             ] + [
                 int(i[2]) for i in atomic_composition
             ]

    if not (len(f_name) == len(f_data) == 28):
        raise RuntimeError("获取到的特征数目不正确")
    return f_name, f_data
def get_feature_by_self(name, sequence, is_non_redundancy=False):
    """
    手动计算的一些属性
    :param name: 序列名称，e.g. ">P0001"
    :param sequence: 序列
    :param is_non_redundancy: 是否为 psi 准备
    :return: (属性名称, 属性)
    """
    if not name.startswith(">"):
        name = "> " + name
    f_name = []
    f_data = []
    # 针对不同的分组，进行计算 CTD
    group1 = ['V', 'I', 'L', 'F', 'M', 'W', 'Y', 'C']
    group1_count = 0
    group2 = ['D', 'E']
    group2_count = 0
    group3 = ['R', 'K', 'H']
    group3_count = 0
    group4 = ['G', 'P']
    group4_count = 0
    group5 = ['N', 'Q', 'S']
    group5_count = 0
    group6 = ['A', 'T']
    group6_count = 0

    animo_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X',
                  'Y']
    concate_list = []  # 相邻的氨基酸
    for i in animo_list:
        for j in animo_list:
            concate_list.append(i + j)
    count_dict = {}
    for i in concate_list:
        count_dict[i] = 0

    # 计算相邻氨基酸对的数目
    for j in range(len(sequence) - 1):
        count_dict[sequence[j] + sequence[j + 1]] += 1
    # 计算不同组别氨基酸的数目
    for j in range(len(sequence)):
        if sequence[j] in group1:
            group1_count += 1
        if sequence[j] in group2:
            group2_count += 1
        if sequence[j] in group3:
            group3_count += 1
        if sequence[j] in group4:
            group4_count += 1
        if sequence[j] in group5:
            group5_count += 1
        if sequence[j] in group6:
            group6_count += 1
    # group count all 相当于就是序列的长度
    # 需要数目和频率
    group_count_all = group1_count + group2_count + group3_count + group4_count + group5_count + group6_count

    f_name += ["fre(G6_%s)" % i for i in range(1, 7)]
    f_name += ["count(G6_%s)" % i for i in range(1, 7)]
    f_data += [group1_count * 1.0 / group_count_all,
               group2_count * 1.0 / group_count_all,
               group3_count * 1.0 / group_count_all,
               group4_count * 1.0 / group_count_all,
               group5_count * 1.0 / group_count_all,
               group6_count * 1.0 / group_count_all,
               ]
    f_data += [group1_count, group2_count, group3_count, group4_count, group5_count, group6_count, ]

    f_name += ["count(%s to %s)" % (i[0], i[1]) for i in concate_list]
    f_data += [count_dict[i] for i in concate_list]

    '''
    20210912 添加二肽频率
    '''
    # f_name += ["fre_count(%s to %s)" % (i[0], i[1]) for i in concate_list]
    # f_data += [(count_dict[i] / len(sequence))*100 for i in concate_list]
    '''
    '''

    if not (len(f_name) == len(f_data) == 453):
        raise RuntimeError("获取到的特征数目不正确")
    return f_name, f_data


def r2py(text):
    s = r"""
library('protr')
library('DT')
extractCTD = function (x) c(extractCTDC(x), extractCTDT(x), extractCTDD(x))

funcdict   = c(
'aac'    = 'extractAAC',
'dc'     = 'extractDC',
'tc'     = 'extractTC',
'mb'     = 'extractMoreauBroto',
'moran'  = 'extractMoran',
'geary'  = 'extractGeary',
'ctd'    = 'extractCTD',
'ctriad' = 'extractCTriad',
'socn'   = 'extractSOCN',
'qso'    = 'extractQSO',
'paac'   = 'extractPAAC',
'apaac'  = 'extractAPAAC',
'ets' = 'extractScales'
)


fs = function(path){

 seq <- scan(textConnection(path), what = 'complex', blank.lines.skip = TRUE)

 aaa <- c("aac","dc","mb","moran","geary","ctd","ctriad","socn","qso","paac","apaac")

 exec = paste0('t(sapply(seq, ', funcdict[as.character(aaa)], '))')
 outlist = vector('list', length(exec))
 n = length(exec)
 for (i in 1L:n) {
   outlist[[i]] = eval(parse(text = exec[i]))
 }

 out = do.call(cbind, outlist)
 return(out)
}
"""
    robjects.r(s)

    r = robjects.r["fs"](text)

    # print(r)
    # print(type(r))
    rr = pandas2ri.rpy2py_floatvector(r)
    # print(type(rr))
    return rr

def extract_descales(text):
    s = r"""
    library('protr')
    fs = function(text, p){
    x <- scan(textConnection(text), what = 'complex', blank.lines.skip = TRUE)
    descscales <- extractDescScales(
      x,
      propmat = p,
      # index = c(1:5, 1:5),
      # index = c(37:41, 43:47),
      pc = 5, lag = 7, silent = FALSE
    )
    return(descscales)
    }
    """

    robjects.r(s)
    var_list = [
        'AAMOE2D', 'AAMOE3D', 'AACPSA', 'AADescAll', 'AA2DACOR', 'AA3DMoRSE', 'AAACF', 'AABurden', 'AAConn', 'AAConst', 'AAEdgeAdj',
        'AAEigIdx', 'AAFGC', 'AAGeom', 'AAGETAWAY', 'AAInfo', 'AAMolProp', 'AARandic', 'AARDF', 'AATopo', 'AATopoChg', 'AAWalk',
        'AAWHIM'
    ]
    # result = {}
    err_list = []
    mer = None
    for index, p in enumerate(var_list):
        print(f"now = {p}")
        try:
            ret = robjects.r["fs"](text, p)
            # print("=== 上面自动打印，下面ret内容 ===")
            rr = pandas2ri.rpy2py_floatvector(ret)
            rr_len = len(rr)

            if rr_len < 175:
                num = np.average(rr)
                print("num=", num)
                rr = np.append(rr, [num] * (175 - rr_len))
            else:
                rr = rr[:175]

            if mer is None:
                mer = rr
            else:
                mer = np.append(mer, rr)
            # result[p] = rr
            # print(ret)
        except UnicodeDecodeError:
            err_list.append(p)
    if err_list:
        print(f"err_list={err_list}")
        print("len=", len(err_list))
    # print(mer)
    # print(len(mer))
    return mer

def extract_fascales(text):
    s = r"""
    library('protr')
    fs = function(text, p){
    x <- scan(textConnection(text), what = 'complex', blank.lines.skip = TRUE)
    data(AATopo)
    tprops <- AATopo[, c(37:41, 43:47)] 
    a <- extractFAScales(x, propmat = tprops, factors = 5, lag = 7, silent = FALSE)
    return(a)
    }
    """
    robjects.r(s)
    r = robjects.r["fs"](text)
    rr = pandas2ri.rpy2py_floatvector(r)
    return rr

def extract_mdsscales(text):
    s = r"""
    library('protr')
    fs = function(text, p){
    x <- scan(textConnection(text), what = 'complex', blank.lines.skip = TRUE)
    data(AATopo)
    # tprops <- AATopo[, c(37:41, 43:47)] 
    tprops <- AATopo
    mds <- extractMDSScales(x, propmat = tprops, k = 5, lag = 7, silent = FALSE)
    return(mds)
    }
    """
    robjects.r(s)
    r = robjects.r["fs"](text)
    rr = pandas2ri.rpy2py_floatvector(r)
    return rr


def merge_all(text):
    ret = r2py(text)
    ret1 = extract_descales(text)
    # print(ret1)
    # print("shape=", ret1.shape)
    ret2 = extract_fascales(text)
    # print(ret2)
    # print("shape=", ret2.shape)
    ret3 = extract_mdsscales(text)
    # print(ret3)
    # print("shape=", ret3.shape)
    return np.append(np.append(np.append(ret, ret1), ret3), ret2)
    # return np.append(np.append(ret1, ret3), ret2)
def get_feature_from_profeat_replace(name, sequence, is_non_redundancy=False):
    result = merge_all(sequence)
    result = result.tolist()
    # print("result", result)
    return list(range(len(result))), result

def get_all_features_from_protstab(name, seq, is_non_redundancy=False, is_mutil_thread=True):
    """
    返回所有的相关的属性
    :param name: 序列名称，e.g. ">P0001"
    :param seq: 氨基酸序列
    :param is_non_redundancy: 是否为 psi 准备
    :param is_mutil_thread: 是否使用多线程，速度可以快一倍左右
    :return: (属性名称, 属性数据)
    """
    result_profeat_replace = []
    result_proteinrecon = []
    result_prodcal = []
    result_protparam = []
    result_by_self = []

    # 是否使用多线程
    if is_mutil_thread:
        def run(store, fun, *args):
            """线程辅助函数"""
            _res = fun(*args)
            store.append(_res[0])
            store.append(_res[1])

        # 创建线程
        threads = [
            # threading.Thread(target=run, args=(result_profeat, get_feature_from_profeat, name, seq, is_non_redundancy)),
            threading.Thread(target=run,
                             args=(result_proteinrecon, get_feature_from_proteinrecon, name, seq, is_non_redundancy)),
            threading.Thread(target=run, args=(result_prodcal, get_feature_from_prodcal, name, seq, is_non_redundancy)),
            threading.Thread(target=run,
                             args=(result_protparam, get_feature_from_protparam, name, seq, is_non_redundancy)),
            threading.Thread(target=run, args=(result_by_self, get_feature_by_self, name, seq, is_non_redundancy)),
            threading.Thread(target=run,
                             args=(result_profeat_replace, get_feature_from_profeat_replace, name, seq, is_non_redundancy)),
        ]
        # 开启线程
        for t in threads:
            t.setDaemon(True)
            t.start()

        # 同步
        for t in threads:
            t.join()
    else:
        result_proteinrecon = get_feature_from_proteinrecon(name, seq)
        result_prodcal = get_feature_from_prodcal(name, seq)
        result_protparam = get_feature_from_protparam(name, seq)
        result_by_self = get_feature_by_self(name, seq)
        result_profeat_replace = get_feature_from_profeat_replace(name, seq, is_non_redundancy)
    # 汇总结果
    full_result = [
        result_proteinrecon,
        result_prodcal,
        result_protparam,
        result_by_self,
        result_profeat_replace
    ]
    f_names = []
    f_datas = []
    for i in full_result:
        # 这里开始改
        try:
            f_names += i[0]
            f_datas += i[1]
        except:
            continue
        # 结束，下面是原本代码
        # f_names += i[0]
        # f_datas += i[1]
    return f_names, f_datas