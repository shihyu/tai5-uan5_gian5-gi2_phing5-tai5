from behave import when, then, step
from 臺灣言語平臺.項目模型 import 平臺項目表


@then('無建議的詞內底無物件')
def 無建議的詞內底無物件(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(len(無建議的詞), 0)


@step('有人求 豬 的講法')
def 有人求講法(context):
    回應 = context.test.client.post('/平臺項目/加外語', {'外語資料': '豬'})
    context.test.assertEqual(回應.status_code, 200)


@then('查 豬 無任何講法')
def 講法內無揣著物件(context):
    講法 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': '豬'}).json()['列表']
    context.test.assertEqual(len(講法), 0)


@then('無建議的詞內底有 豬')
def 無建議的詞內底有物件(context):
    無建議的詞 = context.test.client.get('/平臺項目列表/揣無建議的外語').json()['列表']
    context.test.assertEqual(無建議的詞[0]['外語資料'], '豬')


@step('有人答 豬仔 的講法')
def 有人答的講法(context):
    外語回應 = context.test.client.post('/平臺項目/加外語', {'外語資料': '豬'})
    回應 = context.test.client.post(
        '/平臺項目/加新詞文本', {
            '外語項目編號': 外語回應.json()['平臺項目編號'],  # 針對哪一個外語的母語文本
            '文本資料': '豬仔',  # 錄製的文本檔，檔案型態
        }
    )
    context.test.assertEqual(回應.status_code, 200)
    context.文本編號 = 回應.json()['平臺項目編號']


@when('有人校對 豬仔 的講法')
def 有人校對講法(context):
    平臺項目表.揣編號(context.文本編號).設為推薦用字()


@then('查 豬 會當揣著 豬仔')
def 會當揣著講法(context):
    講法 = context.test.client.get('/平臺項目列表/揣列表', {'關鍵字': '豬'}).json()['列表']
    context.test.assertEqual(講法[0]['新詞文本'][0]['文本資料'], '豬仔')
