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
    httpheader = dict['httpHeader']
    browserinformation = dict['browserInformation']

    httpUserAgent = httpheader['httpUserAgent']
    httpRemoteAddr = httpheader['httpRemoteAddr']
    httpRomoteHost = httpheader['httpRemoteHost']
    httpAccept = httpheader['httpAccept']
    httpAcceptLanguage = httpheader['httpAcceptLanguage']
    httpAcceptEncoding = httpheader['httpAcceptEncoding']
    httpContentLength = httpheader['httpContentLength']
    httpContentType = httpheader['httpContentType']
    httpConnection = httpheader['httpConnection']
    httpCacheControl = httpheader['httpCacheControl']
    httpUpgradeInsecureRequests = ['httpUpgradeInsecureRequests']
    httpQueryString = ['httpQueryString']
    httpReferer = httpheader['httpReferer']
    isp = httpheader['isp']

    userAgent = str(browserinformation['userAgent'])
    languages = str(browserinformation['languages'])
    hardwareConcurrency = str(browserinformation['hardwareConcurrency'])
    appVersion = str(browserinformation['appVersion'])
    deviceMemory = str(browserinformation['deviceMemory'])
    doNotTrack = str(browserinformation['doNotTrack'])
    maxTouchPoints = str(browserinformation['maxTouchPoints'])
    product = str(browserinformation['product'])
    productSub = str(browserinformation['productSub'])
    vendor = str(browserinformation['vendor'])
    vendorSub = str(browserinformation['vendorSub'])
    oscpu = str(browserinformation['oscpu'])
    platform = str(browserinformation['platform'])
    colorDepth = str(browserinformation['colorDepth'])
    devicePixelRatio = str(browserinformation['devicePixelRatio'])
    screenResolution = str(browserinformation['screenResolution'])
    availScreenResolution = str(browserinformation['availScreenResolution'])
    windowResolution = str(browserinformation['windowResolution'])
    windowPosition = str(browserinformation['windowPosition'])
    cookieEnabled = str(browserinformation['cookieEnabled'])
    touchEnabled = str(browserinformation['touchEnabled'])
    pdfViewerEnabled = str(browserinformation['pdfViewerEnabled'])
    gpuVendor = str(browserinformation['gpuVendor'])
    gpuRenderer = str(browserinformation['gpuRenderer'])
    webgl = str(browserinformation['webgl'])
    referrer = str(browserinformation['referrer'])
    timezoneOffset = str(browserinformation['timezoneOffset'])
    networkInformation = str(browserinformation['networkInformation'])

    fingerprint = httpUserAgent + httpRemoteAddr + httpAcceptLanguage + userAgent + languages + appVersion + oscpu + platform + colorDepth + availScreenResolution + screenResolution + cookieEnabled + touchEnabled + pdfViewerEnabled + timezoneOffset
    #print(fingerprint)
    return fingerprint

#sql文
sql_all = 'SELECT fingerprint FROM fingerprint_fingerprint'

#フィンガープリントの用意
database_fingerprint = database(sql_all)
login_fingerptint = dataFormatting(json.loads((database_fingerprint[3])[0]))
distance_list = []

#評価するところ
for i in database_fingerprint:
    data = i[0]
    json_dict = json.loads(data)
    fingerprint = dataFormatting(json_dict)
    distance = Levenshtein.ratio(fingerprint, login_fingerptint)
    if distance >= 0.95:
        distance_list.append(distance)

len = len(distance_list)
print(len)
print(distance_list)
#print(distance_list[index])

#データベース接続終わり
cur.close()
connection.close()