import sqlite3
import json
import Levenshtein

#データベース接続
db = "db.sqlite3"
connection = sqlite3.connect(db)
cur = connection.cursor()

#データベースからsqlで中身取り出す関数
def database(sql):
    cur.execute(sql)
    return cur.fetchall()

#フィンガープリントから必要な特徴点取り出す関数
def dataFormatting(dict):
    fingerprint_list = []

    httpheader = dict['httpHeader']
    browserinformation = dict['browserInformation']

    httpUserAgent = fingerprint_list.append(httpheader['httpUserAgent'])
    httpRemoteAddr = fingerprint_list.append(httpheader['httpRemoteAddr'])
    httpRomoteHost = fingerprint_list.append(httpheader['httpRemoteHost'])
    httpAccept = fingerprint_list.append(httpheader['httpAccept'])
    httpAcceptLanguage = fingerprint_list.append(httpheader['httpAcceptLanguage'])
    httpAcceptEncoding = fingerprint_list.append(httpheader['httpAcceptEncoding'])
    httpContentLength = fingerprint_list.append(httpheader['httpContentLength'])
    httpContentType = fingerprint_list.append(httpheader['httpContentType'])
    httpConnection = fingerprint_list.append(httpheader['httpConnection'])
    httpCacheControl = fingerprint_list.append(httpheader['httpCacheControl'])
    httpUpgradeInsecureRequests = fingerprint_list.append(httpheader['httpUpgradeInsecureRequests'])
    httpQueryString = fingerprint_list.append(httpheader['httpQueryString'])
    httpReferer = fingerprint_list.append(httpheader['httpReferer'])
    isp = fingerprint_list.append(str(httpheader['isp']))

    userAgent = fingerprint_list.append(str(browserinformation['userAgent']))
    languages = fingerprint_list.append(str(browserinformation['languages']))
    hardwareConcurrency = fingerprint_list.append(str(browserinformation['hardwareConcurrency']))
    appVersion = fingerprint_list.append(str(browserinformation['appVersion']))
    deviceMemory = fingerprint_list.append(str(browserinformation['deviceMemory']))
    doNotTrack = fingerprint_list.append(str(browserinformation['doNotTrack']))
    maxTouchPoints = fingerprint_list.append(str(browserinformation['maxTouchPoints']))
    product = fingerprint_list.append(str(browserinformation['product']))
    productSub = fingerprint_list.append(str(browserinformation['productSub']))
    vendor = fingerprint_list.append(str(browserinformation['vendor']))
    vendorSub = fingerprint_list.append(str(browserinformation['vendorSub']))
    oscpu = fingerprint_list.append(str(browserinformation['oscpu']))
    platform = fingerprint_list.append(str(browserinformation['platform']))
    colorDepth = fingerprint_list.append(str(browserinformation['colorDepth']))
    devicePixelRatio = fingerprint_list.append(str(browserinformation['devicePixelRatio']))
    screenResolution = fingerprint_list.append(str(browserinformation['screenResolution']))
    availScreenResolution = fingerprint_list.append(str(browserinformation['availScreenResolution']))
    windowResolution = fingerprint_list.append(str(browserinformation['windowResolution']))
    windowPosition = fingerprint_list.append(str(browserinformation['windowPosition']))
    cookieEnabled = fingerprint_list.append(str(browserinformation['cookieEnabled']))
    touchEnabled = fingerprint_list.append(str(browserinformation['touchEnabled']))
    pdfViewerEnabled = fingerprint_list.append(str(browserinformation['pdfViewerEnabled']))
    gpuVendor = fingerprint_list.append(str(browserinformation['gpuVendor']))
    gpuRenderer = fingerprint_list.append(str(browserinformation['gpuRenderer']))
    webgl = fingerprint_list.append(str(browserinformation['webgl']))
    referrer = fingerprint_list.append(str(browserinformation['referrer']))
    timezoneOffset = fingerprint_list.append(str(browserinformation['timezoneOffset']))
    networkInformation = fingerprint_list.append(str(browserinformation['networkInformation']))

    #fingerprint = httpUserAgent + httpRemoteAddr + httpAcceptLanguage + userAgent + languages + appVersion + oscpu + platform + colorDepth + availScreenResolution + screenResolution + cookieEnabled + touchEnabled + pdfViewerEnabled + timezoneOffset
    #print(fingerprint_list)
    return fingerprint_list

#sql文
sql_all = 'SELECT fingerprint FROM fingerprint_fingerprint'

#フィンガープリントの用意
database_fingerprint = database(sql_all)
login_fingerptint = dataFormatting(json.loads((database_fingerprint[3])[0]))
distance_list = []

#評価するところ
for i in database_fingerprint:
    distance = 0
    data = i[0]
    json_dict = json.loads(data)
    fingerprint = dataFormatting(json_dict)
    #print(fingerprint)
    for j,k in zip(fingerprint, login_fingerptint):
        distance = Levenshtein.ratio(j, k) + distance
    distance = distance / len(login_fingerptint)
    if distance >= 0.95:
        distance_list.append(distance)

# len = len(distance_list)
# per = (len / 78) * 100
# print(per)
# print(len)
# print(distance_list)

#データベース接続終わり
cur.close()
connection.close()