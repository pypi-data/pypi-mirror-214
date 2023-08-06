import os.path
import pickle
import re
import zipfile

import numpy as np
import requests
from sklearn.externals import joblib

from ProTstab2.utils import A_LIST, get_all_features_from_protstab


class ProTstab2:
    def __init__(self):
        self.base_model_path = os.path.join(os.path.dirname(__file__), "models")
        self.features_model_name = 'selector_1028_200_with6935.pickle'
        self.my_model_name = 'LightGBM_200_with6935.pkl'

        self._check()

        # 乏了，就这么写吧，懒得改了
        self.get_model = None
        self.my_model = None
        self.load_models()

    def _check(self):
        assert os.path.exists(self.base_model_path), 'path does not exist'

    def load_models(self):
        with open(os.path.join(self.base_model_path, self.features_model_name), 'rb') as f:
            self.get_model = pickle.load(f)
        my_model = joblib.load(os.path.join(self.base_model_path, self.my_model_name))
        self.my_model = my_model

    def check_seq_input2(self, name, seq):
        names = re.findall(">([^>]*)", name.replace("\n", "").replace("\r", ""))
        if "|" in seq and names == []:
            seqs = []
            temp = re.findall(r">[^>]*?\|([\w]+)\|.*\n((?:\w|\n|\r)*)", seq, re.MULTILINE)
            if seq.count(">") != len(temp):
                raise TypeError("Data length is not same")
            for t in temp:
                if len(t) == 2:
                    if "x" in t[1].lower():
                        names.append(t[0])
                        # msg = "序列中不能包含X"
                        raise TypeError("sequence contains X. The tool used to calculate the features cannot handle sequence containing X.")
                    else:
                        t_seqs = t[1].replace("\r", "").replace("\n", "")
                        re_result = re.findall("([" + "".join(A_LIST) + r"]+)(.*)", t_seqs)

                        if re_result and len(re_result) == 1 and re_result[0][0] == t_seqs:
                            names.append(t[0])
                            seqs.append(t_seqs)
                        else:
                            names.append(t[0])
                            # seqs.append(WarningMsg(t[1], f"只能包含这{len(A_LIST)}个字符:{''.join(A_LIST)}, "
                            #                              f"但是发现奇异字符: {re_result[0][1][:1]}"))
                            raise TypeError("error input.")
                else:
                    raise TypeError("The length of regular matching is not 2")
        else:
            seqs = re.findall(">([^>]*)", seq.replace("\n", "").replace("\r", ""))

        print(seqs)
        if seqs:
            return names[0], seqs[0]
        else:
            return names[0], ''

    def predict(self, input_name, input_seq=None):
        name, seq = self.check_seq_input2(input_name, input_seq)
        if not seq:
            seq = self.get_seq_info(name)
        if not seq:
            raise TypeError("sequence is empty")
        print("name", name)
        print("seq", seq)
        support = self.get_model.get_support(True)
        res = get_all_features_from_protstab(name, seq)
        train_data = np.array([res[1]])[:, support]
        r = self.my_model.predict(train_data)
        return r[0]

    @staticmethod
    def get_seq_info(pr_id):
        if pr_id.startswith('>'):
            pr_id = pr_id[1:]
        if '\n' in pr_id:
            raise TypeError("The input name cannot contain line breaks")
        headers = {
            'authority': 'www.uniprot.org',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        pr_id = pr_id.split("_")[0] if "_" in pr_id else pr_id
        url = "https://www.uniprot.org/uniprot/" + pr_id
        res_fasta = requests.get(url + ".fasta", headers, verify=False)
        try:
            out_simple = "".join(res_fasta.text.split("\n")[1:])
        except IndexError:
            out_simple = ""
        if '<html' in out_simple or 'http:' in out_simple:
            # out_simple = ErrorMsg("爬虫网站挂了，别试了")
            raise Exception("There are some errors with input. Please have a check.(Maybe the website is down)")
        return out_simple


if __name__ == '__main__':
    # _name = ">P30177"
    _name = ""
    # _seq = ""
    _seq = """>sp|P30177|YBIB_ECOLI Uncharacterized protein YbiB OS=Escherichia coli (strain K12) OX=83333 GN=ybiB PE=1 SV=1
MDYRKIIKEIGRGKNHARDLDRDTARGLYAHMLNGEVPDLELGGVLIALRIKGEGEAEML
GFYEAMQNHTIKLTPPAGKPMPIVIPSYNGARKQANLTPLLAILLHKLGFPVVVHGVSED
PTRVLTETIFELMGITPTLHGGQAQAKLDEHQPVFMPVGAFCPPLEKQLAMRWRMGVRNS
AHTLAKLATPFAEGEALRLSSVSHPEYIGRVAKFFSDIGGRALLMHGTEGEVYANPQRCP
QINLIDREGMRVLYEKQDTAGSELLPQAKDPETTAQWIERCLAGSEPIPESLKIQMACCL
VATGEAATISDGLARVNQAF"""
    p = ProTstab2()
    r = p.predict(_name, _seq)
    print(r)
