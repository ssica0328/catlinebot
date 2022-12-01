from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.

from linebot import WebhookParser
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError

#其他
import time
import datetime as dt
from django.utils import timezone
import pytz
pretime = dt.datetime(2018, 6, 14, 21, 17, 8, 132263).isoformat(' ')

import random
import emoji as em
stars = em.emojize(":glowing_star:")

from cat_linebot.models import *

line_api = LineBotApi(channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(channel_secret=settings.LINE_CHANNEL_SECRET)

#主程式
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if event.type == 'message':
                handle_message(event)
            if event.type == 'postback':
                handle_postback(event)
    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def handle_postback(event):
    #得到user資訊
    display_name = line_api.get_profile(event.source.user_id).display_name
    user_id = line_api.get_profile(event.source.user_id).user_id
    picture_url = line_api.get_profile(event.source.user_id).picture_url
    now = timezone.now()
    #now += dt.timedelta(hours = 8)
    
    data = event.postback.data
    print(f'(postback){display_name}:{data}\n{now}')
    message = []

    if 'game' in data:
        data = str(data).split('+')[1]
        if User_Info.objects.filter(uid=user_id).exists()==True:
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                points = int(user.points)
                ans_time = user.ansdt
            ans_time = str(ans_time).split(' ')[0]
            today_time = str(now).split(' ')[0]
            if ans_time == today_time:
                message.append(TextMessage(text=f'您今日已做過每日問答，請明日再來'))
            else:
                if data == '0':
                    points += 10
                    User_Info.objects.filter(uid=user_id).update(points=points)
                    message.append(TextMessage(text=f'答對了！獲得積分10分\n您的分數提升至：{points}分\n請明日再來'))
                else:
                    message.append(TextMessage(text=f'答錯了！您的分數將維持在：{points}分'))
        else:
            message.append(TextMessage(text=f'您尚未建立會員，請點選下方選單並加入會員'))
    elif '心' in data:
        num = int(str(data).split('+')[1])
        food = 心靈雞湯.objects.filter(num = num)
        for items in food:
            scores = items.score
            times = items.times
        
        new_score = int(str(data).split('+')[2])
        scores += new_score
        times += 1
        心靈雞湯.objects.filter(num = num).update(score = scores)
        心靈雞湯.objects.filter(num = num).update(times = times)
        message.append(TextMessage(text='感謝您為此商品完成評分！'))
    else:
        message.append(TextMessage(text='測試中'))
            
    line_api.reply_message(event.reply_token, message)


def handle_message(event):
    #得到user資訊
    display_name = line_api.get_profile(event.source.user_id).display_name
    user_id = line_api.get_profile(event.source.user_id).user_id
    picture_url = line_api.get_profile(event.source.user_id).picture_url
    now = timezone.now()

    #分辨型別為text
    if event.message.type == "text":
        text = event.message.text
    else:
        typeofmessage = event.message.type
        print(f'({typeofmessage}){display_name}:\n{now}')
        line_api.reply_message(event.reply_token,TextMessage(text="I can't reply this."))
        return 200
    print(f'(text){display_name}:{text}\n{now}')

    #訊息
    message = []

    if '會員資料' in text:
        message.append(TemplateSendMessage(
        alt_text='會員資料',
        template=ButtonsTemplate(
            title='會員資料',
            text='請點選下方按鈕',
            thumbnail_image_url='https://i.imgur.com/D4a3Ale.jpg',
            actions=[
                    MessageTemplateAction(label='加入會員',text='加入會員'),
                    MessageTemplateAction(label='積分查詢',text='積分查詢'),])))
        line_api.reply_message(event.reply_token, message)
    elif '加入會員' in text:
        if User_Info.objects.filter(uid=user_id).exists()==False:
            User_Info.objects.create(uid=user_id, name=display_name, pic_url=picture_url, mtext=text, mdt=now, points=0)
            message.append(TextMessage(text='註冊成功'))
        elif User_Info.objects.filter(uid=user_id).exists()==True:
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                sign_time = user.mdt
            sign_time += dt.timedelta(hours = 8)
            sign_time = str(sign_time).split('.')[0]
            message.append(TextMessage(text=f'已於{sign_time}\n註冊成功'))
        line_api.reply_message(event.reply_token, message)
    elif '積分查詢' in text:
        if User_Info.objects.filter(uid=user_id).exists()==True:
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                points = int(user.points)
            message.append(TextMessage(text=f'您的分數是：{points}分'))
        else:
            message.append(TextMessage(text=f'您尚未建立會員，請點選下方選單並加入會員'))
        line_api.reply_message(event.reply_token, message)
        
    elif '每日問答' in text:
        if User_Info.objects.filter(uid=user_id).exists()==True:
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                ans_time = user.ansdt
            ans_time = str(ans_time).split(' ')[0]
            today_time = str(now).split(' ')[0]
            print(f'ans_time:{ans_time}, today_time:{today_time}')
            if ans_time == today_time:
                message.append(TextMessage(text=f'您今日已做過每日問答，請明日再來'))
            else:
                i = random.randint(0, 4)
                random_question = random_exam.objects.filter(num = i)
                for Q1 in random_question:
                    num = Q1.num
                    question = Q1.question
                    op1 = Q1.op1
                    op2 = Q1.op2
                    op3 = Q1.op3
                    ans = int(Q1.ans)
                message.append(TemplateSendMessage(
                    alt_text='每日問答',
                    template=ButtonsTemplate(
                    title='每日問答',
                    text=f'回答以下問題並獲得積分:\n{question}',
                    thumbnail_image_url='https://i.imgur.com/D4a3Ale.jpg',
                    actions=[
                            PostbackTemplateAction(label=f'{op1}',data=f"game+{1-ans}"),
                            PostbackTemplateAction(label=f'{op2}',data=f"game+{2-ans}"),
                            PostbackTemplateAction(label=f'{op3}',data=f"game+{3-ans}"),])))
                User_Info.objects.filter(uid=user_id).update(ansdt=now)
        else:
            message.append(TextMessage(text=f'您尚未建立會員，請點選下方選單並加入會員'))
        
        line_api.reply_message(event.reply_token, message)
    elif '商品查詢' in text:
        message.append(TemplateSendMessage(
            alt_text='商品查詢',
            template=ButtonsTemplate(
                title='商品查詢',
                text='點選下方按鈕查看商品資訊',
                thumbnail_image_url='https://i.imgur.com/Z3QWYlE.jpg',
                actions=[
                        MessageTemplateAction(label='主食罐',text="主食罐"),
                        MessageTemplateAction(label='飼料',text="飼料"),
                        MessageTemplateAction(label='貓砂',text="貓砂"),
                        MessageTemplateAction(label='玩具',text="玩具"),
                        ])))
        line_api.reply_message(event.reply_token, message)
    elif '乖乖吃飯' in text:
        if text == '乖乖吃飯':
            message.append(TemplateSendMessage(
            alt_text='乖乖吃飯',
            template=ButtonsTemplate(
                title='乖乖吃飯',
                text='乖乖吃飯',
                thumbnail_image_url='https://i.imgur.com/Z3QWYlE.jpg',
                actions=[
                        MessageTemplateAction(label='香煨嫩雞',text="乖乖吃飯_香煨嫩雞"),
                        MessageTemplateAction(label='青魽凝鮨',text="乖乖吃飯_青魽凝鮨"),
                        MessageTemplateAction(label='極品精鯛',text="乖乖吃飯_極品精鯛"),
                        MessageTemplateAction(label='烈焰火雞',text="乖乖吃飯_烈焰火雞"),
                        ])))
        else:
            dict1 = {'香煨嫩雞':0, '青魽凝鮨':1, '極品精鯛':2, '烈焰火雞':3, '鮮燉鴕鳥':4, '老甕珍牛':5}
            text1 = text.split('_')[1]
            i = dict1[text1]
            food = 乖乖吃飯.objects.filter(num = i)
            for items in food:
                name = items.name
                price = items.price
                grams = items.grams
                protein = items.protein
                fat = items.fat
                carbo = items.carbo
                phos = items.phos
                kcal = items.kcal
                score = items.score
            message.append(TextSendMessage(text=f'{name}\n\n價格：{price}\n重量：{grams}\n蛋白質：{protein}\n脂肪：{fat}\n碳水化合物：{carbo}\n磷含量：{phos}\n熱量：{kcal}\n推薦指數：{score}\n為這個商品評分吧',
                        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label=f"{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}{stars}", data="nothing")),
                        ])))
        line_api.reply_message(event.reply_token, message)
    elif 'pidan' in text or 'Pidan' in text:
        if text == 'pidan' or text == 'Pidan':
            message.append(TemplateSendMessage(
            alt_text='pidan',
            template=ButtonsTemplate(
                title='pidan',
                text='點選下方按鈕查看商品資訊',
                thumbnail_image_url='https://i.imgur.com/Z3QWYlE.jpg',
                actions=[
                        MessageTemplateAction(label='混合貓砂經典版',text="pidan_混合貓砂 經典版"),
                        MessageTemplateAction(label='混合貓砂活性碳低塵版',text="pidan_混合貓砂 活性碳低塵版"),
                        MessageTemplateAction(label='豆腐貓砂原味款',text="pidan_豆腐貓砂 原味款"),
                        MessageTemplateAction(label='豆腐貓砂隱血測試款',text="pidan_豆腐貓砂 隱血測試款"),
                        ])))
        else:
            dict1 = {'混合貓砂 經典版':0, '混合貓砂 活性碳低塵版':1, '豆腐貓砂 原味款':2, '豆腐貓砂 隱血測試款':3}
            text1 = text.split('_')[1]
            i = dict1[text1]
            food = pidan.objects.filter(num = i)
            for items in food:
                name = items.name
                price = items.price
                grams = items.grams
                material = items.material
                ratio = items.ratio
                score = items.score
            message.append(TextSendMessage(text=f'{name}\n\n價格：{price}\n重量：{grams}\n成分：{material}\n產品配比：{ratio}\n推薦指數：{score}\n為這個商品評分吧',
                        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label=f"{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}{stars}", data="nothing")),
                        ])))
        line_api.reply_message(event.reply_token, message)
    elif '心靈雞湯' in text:
        if text == '心靈雞湯':
            message.append(TemplateSendMessage(
            alt_text='心靈雞湯',
            template=ButtonsTemplate(
                title='心靈雞湯',
                text='點選下方按鈕查看商品資訊',
                thumbnail_image_url='https://i.imgur.com/Z3QWYlE.jpg',
                actions=[
                        MessageTemplateAction(label='經典系列-雞肉佐火雞肉成貓',text="心靈雞湯_經典雞肉成貓"),
                        MessageTemplateAction(label='經典系列-雞肉佐火雞肉幼母貓',text="心靈雞湯_經典雞肉幼貓"),
                        MessageTemplateAction(label='經典系列-鮭魚佐雞肉成貓',text="心靈雞湯_經典鮭魚"),
                        ])))
        else:
            dict1 = {'經典雞肉成貓':0, '經典雞肉幼貓':1, '經典鮭魚':2}
            text1 = text.split('_')[1]
            i = dict1[text1]
            food = 心靈雞湯.objects.filter(num = i)
            for items in food:
                num = items.num
                name = items.name
                price = items.price
                grams = items.grams
                protein = items.protein
                fat = items.fat
                carbo = items.carbo
                phos = items.phos
                score = items.score
            message.append(TextSendMessage(text=f'{name}\n\n價格：{price}\n重量：{grams}\n蛋白質：{protein}\n脂肪：{fat}\n碳水化合物：{carbo}\n磷含量：{phos}\n推薦指數：{score}\n為這個商品評分吧',
                        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label=f"{stars}", data=f"心+{num}+1")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}", data=f"心+{num}+2")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}", data=f"心+{num}+3")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}", data=f"心+{num}+4")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}{stars}", data=f"心+{num}+5")),
                        ])))
        line_api.reply_message(event.reply_token, message)
    elif '主食罐' in text:
        message.append(TextMessage(text='請輸入你要查詢的品牌(ex.乖乖吃飯)'))
        line_api.reply_message(event.reply_token, message)
    elif '飼料' in text:
        message.append(TextMessage(text='請輸入你要查詢的品牌(ex.心靈雞湯)'))
        line_api.reply_message(event.reply_token, message)
    elif '貓砂' in text:
        message.append(TextMessage(text='請輸入你要查詢的品牌(ex.pidan)'))
        line_api.reply_message(event.reply_token, message)
    elif '玩具' in text:
        message.append(TextMessage(text='請輸入你要查詢的品牌'))
        line_api.reply_message(event.reply_token, message)
    else:
        line_api.reply_message(event.reply_token,TextMessage(text=text))