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

    userAgent = browserinformation['userAgent']
    languages = browserinformation['languages']
    hardwareConcurrency = browserinformation['hardwareConcurrency']
    appVersion = browserinformation['appVersion']
    deviceMemory = browserinformation['deviceMemory']
    doNotTrack = browserinformation['doNotTrack']
    maxTouchPoints = browserinformation['maxTouchPoints']
    product = browserinformation['product']
    productSub = browserinformation['productSub']
    vendor = browserinformation['vendor']
    vendorSub = browserinformation['vendorSub']
    oscpu = browserinformation['oscpu']
    platform = browserinformation['platform']
    colorDepth = browserinformation['colorDepth']
    devicePixelRatio = browserinformation['devicePixelRatio']
    screenResolution = browserinformation['screenResolution']
    availScreenResolution = browserinformation['availScreenResolution']
    windowResolution = browserinformation['windowResolution']
    windowPosition = browserinformation['windowPosition']
    cookieEnabled = str(browserinformation['cookieEnabled'])
    touchEnabled = str(browserinformation['touchEnabled'])
    pdfViewerEnabled = str(browserinformation['pdfViewerEnabled'])
    gpuVendor = browserinformation['gpuVendor']
    gpuRenderer = browserinformation['gpuRenderer']
    webgl = browserinformation['webgl']
    referrer = browserinformation['referrer']
    timezoneOffset = browserinformation['timezoneOffset']
    networkInformation = browserinformation['networkInformation']

    fingerprint = httpUserAgent
    #print(fingerprint)
    return fingerprint

#sql文
sql_all = 'SELECT tracking FROM fingerprint_tracking'

#フィンガープリントの用意
database_fingerprint = database(sql_all)
login_fingerptint = dataFormatting(json.loads((database_fingerprint["""ここに比較したいフィンガ―プリントのid-1(インデックス番号)の数字を入れる"""])[0]))
distance_list = []

#評価するところ
for i in database_fingerprint:
    data = i[0]
    json_dict = json.loads(data)
    fingerprint = dataFormatting(json_dict)
    distance = Levenshtein.ratio(fingerprint, login_fingerptint)
    distance_list.append(distance)

print(distance_list.index(max(distance_list)))
    

#データベース接続終わり
cur.close()
connection.close()