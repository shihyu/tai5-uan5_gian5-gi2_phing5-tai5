from django.http.response import JsonResponse
from 臺灣言語平臺.項目模型 import 平臺項目表

from dateutil import tz


def 外語請教條相關資料內容(request, 外語請教條項目編號):
	臺北 = tz.gettz('Asia/Taipei')
	時間格式 = '%Y-%m-%d %H:%M:%S'
	回應資料 = {'外語請教條項目編號':外語請教條項目編號}
	try:
		外語項目 = 平臺項目表.揣編號(外語請教條項目編號)
		外語 = 外語項目.外語
		回應資料['外語資料'] = 外語.外語資料
		回應資料['外語語言'] = 外語.外語語言.語言腔口
		回應資料['收錄者'] = 外語.收錄者.編號()
		回應資料['來源'] = 外語.來源.編號()
		回應資料['收錄時間'] = 外語.收錄時間\
				.astimezone(臺北).strftime(時間格式)
		回應資料['種類'] = 外語.種類.種類
		回應資料['語言腔口'] = 外語.語言腔口.語言腔口
	except:
		return JsonResponse({'錯誤': '這不是外語請教條的編號'})
	
	回應資料['新詞影音'] = []
	for 翻譯影音 in 外語.翻譯影音.all():
		影音 = 翻譯影音.影音
		回應影音 = {'新詞影音項目編號':str(影音.平臺項目.get().編號())}
		回應影音['收錄者'] = 影音.收錄者.編號()
		回應影音['來源'] = 影音.來源.編號()
		回應影音['收錄時間'] = 影音.收錄時間\
				.astimezone(臺北).strftime(時間格式)
		回應影音['影音資料網址'] = 影音.網頁影音資料.url
		回應影音['新詞文本'] = []
		for 影音文本 in 影音.影音文本.all():
			文本 = 影音文本.文本
			回應文本 = {'新詞文本項目編號':str(文本.平臺項目.get().編號())}
			回應文本['收錄者'] = 文本.收錄者.編號()
			回應文本['來源'] = 文本.來源.編號()
			回應文本['收錄時間'] = 文本.收錄時間\
					.astimezone(臺北).strftime(時間格式)
			回應文本['文本資料'] = 文本.文本資料
			回應影音['新詞文本'].append(回應文本)
		回應資料['新詞影音'].append(回應影音)
		
	回應資料['新詞文本'] = []
	for 翻譯文本 in 外語.翻譯文本.all():
		文本 = 翻譯文本.文本
		回應文本 = {'新詞文本項目編號':str(文本.平臺項目.get().編號())}
		回應文本['收錄者'] = 文本.收錄者.編號()
		回應文本['來源'] = 文本.來源.編號()
		回應文本['收錄時間'] = 文本.收錄時間\
				.astimezone(臺北).strftime(時間格式)
		回應文本['文本資料'] = 文本.文本資料
		回應資料['新詞文本'].append(回應文本)
	return JsonResponse(回應資料)
		
