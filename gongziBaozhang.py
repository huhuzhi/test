#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import sys
import json
# reload(sys)
# sys.setdefaultencoding("utf-8")


def getgongziBaozhang():
    # 登录OA
    with open("D:\\code\\user.json", "r") as f:
        jsonconfig = json.load(f)
    _name = jsonconfig['name']
    _pass = jsonconfig['pass']
    print(_name, _pass)
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko'}
    payload = {'login-form-type': 'pwd', 'username': _name, 'password': _pass}
    r1 = s.post("http://portal.sx.cmcc/pkmslogin.form",
                headers=headers, data=payload)
    print("登录中.", end=""),
#    print(r1.text)
    r2 = s.get("http://portal.sx.cmcc/sxmcc_portal/dt?action=login&firstLogin=yes")
    print(".", end="")
    r3 = s.get("http://portal.sx.cmcc/sxmcc_portal/dt?portalmark=default")
    print(".", end="")
    r4 = s.get("http://portal.sx.cmcc/sxmcc_portal/tablex.jsp?portalmark=default")
    print(".", end="")
    r5 = s.get("http://portal.sx.cmcc/sxmcc_wcm/telcheck/tel_check.jsp")
    print(".", end="")
    r6 = s.get(
        "http://portal.sx.cmcc/sxmcc_wcm/portalchannelexample/daiban/daibai_new.jsp")
    print(".", end="")
    r7 = s.get(
        "http://portal.sx.cmcc/sxmcc_was/uploadResource/clientinforecord/getclientinfo.jsp?firstLogin=null")
    print(".", end="")
    r8 = s.get("http://portal.sx.cmcc/pend2/pend/dbzq/workitem/workitem_dbzq.jsp")
    print(".", end="")
    # 登录报账系统
#    r9 = s.get("http://portal.sx.cmcc/sxmcc_wcm/middelwebpage/app_recoder_log.jsp?app_flg=eFinance")
    r9 = s.get(
        "http://portal.sx.cmcc/pend1/pend/dbzq/workitem/app_recoder_log.jsp?app_flg=fmbz")
    print(".", end="")
#    print r9.text
    r10 = s.post("http://portal.sx.cmcc/eFinance/main.jsp")
    print(".")
#    print(r10.text)

    postURL = "http://portal.sx.cmcc/eFinance/rmbs/claimXML.do"

    postData = {'serviceBean': 'listAllClaimSavedService', 'isSys': 'y', 'sign': 'START', 'currPage': '1', 'pageSize': '1',
                'goPage': '', 'claimNo': '', 'itemId': '', 'applyUserName': '', 'applyStartDate': '', 'applyEndDate': '', 'contractNo': '',
                'contractName': '', 'vendorName': '', 'moneyFrom': '', 'moneyTo': '', 'item2Id': '163', 'polist': '', 'paymoneyFrom': '',
                'paymoneyTo': '', 'keyComp': '41000000', 'keyDept': '41560000', 'processState': '', 'permit ': '1'}
    resp = s.post(postURL, postData)
    claimUrl = "http://portal.sx.cmcc/eFinance/transferClaim.do?type=started&itemId=T002&motion=4003&claimId="
#    print(resp.text)
    # claimId = re.findall('Name="claimId.*?>(.*?)</Field>', resp.text, re.S)
    # date = re.findall('applyDate.*?>(.*?)</Field>', resp.text, re.S)
    # state = re.findall('processState.*?>(.*?)</Field>', resp.text, re.S)

    claimData = re.findall(
        'Name="claimId.*?>(.*?)</Field>.*?applyDate.*?>(.*?)</Field>.*?processState.*?>(.*?)</Field>', resp.text, re.S | re.M)
#    print claimData
    claimId = ''
    for item in claimData:
        print(item[1], item[2], claimUrl+item[0])
        claimId = item[0]

#    print date[0],'\t',state[0],'\t',claimUrl+claimId[0]

# 获取审批意见
    detailURL = claimUrl+claimId
#    print detailURL
    detailResp = s.get(detailURL)
    tableData = re.findall(u'/>审批意见</td>.*?<TABLE.*?>(.*?)</table>',
                           detailResp.text.lower(), re.S | re.M | re.IGNORECASE)
#    print tableData[0]
    try:
        trData = re.findall('<tr.*?>(.*?)</tr>', tableData[0], re.S | re.M)
    #    print trData
        for item in trData:
            #        print item
            data = re.findall('<td.*?>(.*?)</td>', item, re.S | re.M)
            print(data[0], '\t', data[1], '\t', data[2], '\t', data[3], '\t', data[5],
                  '\t', data[6].strip(), '\t', data[7], '\t', data[8], '\n', end=""),
    except:
        print("NULL")

    return


if __name__ == '__main__':
    getgongziBaozhang()
