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
    now = time.ctime()
    
    data = int(event.postback.data)
    print(f'(postback){display_name}:{data}\n{now}')
    message = []

    
    if User_Info.objects.filter(uid=user_id).exists()==True:
        user_info = User_Info.objects.filter(uid=user_id)
        for user in user_info:
            points = int(user.points)
        if data == 0:
            points += 10
            User_Info.objects.filter(uid=user_id).update(points=points)
            message.append(TextMessage(text=f'答對了!加10分，您的分數提升至：{points}分'))
        elif data == 'nothing':
            message.append(TextMessage(text='測試成功'))
        else:
            message.append(TextMessage(text=f'答錯了!您的分數維持在：{points}分'))
    else:
        message.append(TextMessage(text=f'您尚未建立會員，請輸入"開始"加入會員'))
    line_api.reply_message(event.reply_token, message)


def handle_message(event):
    #得到user資訊
    display_name = line_api.get_profile(event.source.user_id).display_name
    user_id = line_api.get_profile(event.source.user_id).user_id
    picture_url = line_api.get_profile(event.source.user_id).picture_url
    now = time.ctime()

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

    if '新增會員資料' in text:
        if User_Info.objects.filter(uid=user_id).exists()==False:
            User_Info.objects.create(uid=user_id, name=display_name, pic_url=picture_url, mtext=text, mdt=now, points=0)
            message.append(TextMessage(text='註冊成功'))
        elif User_Info.objects.filter(uid=user_id).exists()==True:
            message.append(TextMessage(text='已註冊成功'))
        line_api.reply_message(event.reply_token, message)

    elif '會員資料註冊' in text:
        if User_Info.objects.filter(uid=user_id).exists()==False:
            message.append(TemplateSendMessage(
            alt_text='加入會員',
            template=ButtonsTemplate(
                title='加入會員',
                text='點選下方按鈕以建立會員資料',
                thumbnail_image_url='https://i.imgur.com/D4a3Ale.jpg',
                actions=[MessageTemplateAction(label='加入會員',text='新增會員資料')])))
        elif User_Info.objects.filter(uid=user_id).exists()==True:
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                sign_time = user.mdt
            message.append(TextMessage(text=f'已於{sign_time}註冊成功'))
        line_api.reply_message(event.reply_token, message)

    elif '積分' in text:
        if '查詢' in text:
            if User_Info.objects.filter(uid=user_id).exists()==True:
                user_info = User_Info.objects.filter(uid=user_id)
                for user in user_info:
                    points = int(user.points)
                message.append(TextMessage(text=f'您的分數是：{points}分'))
            else:
                message.append(TextMessage(text=f'您尚未建立會員，請輸入"開始"加入會員'))
            line_api.reply_message(event.reply_token, message)
        elif '歸零' in text:
            if User_Info.objects.filter(uid=user_id).exists()==True:
                User_Info.objects.filter(uid=user_id).update(points=int(0))
                message.append(TextMessage(text=f'您已成功將分數歸零'))
            else:
                message.append(TextMessage(text=f'您尚未建立會員，請輸入"開始"加入會員'))
            line_api.reply_message(event.reply_token, message)
        elif '+1' in text:
            if User_Info.objects.filter(uid=user_id).exists()==True:
                user_info = User_Info.objects.filter(uid=user_id)
                for user in user_info:
                    points = int(user.points)
                points += 1
                User_Info.objects.filter(uid=user_id).update(points=points)
                message.append(TextMessage(text=f'分數成功+1'))
            else:
                message.append(TextMessage(text=f'您尚未建立會員，請輸入"開始"加入會員'))
            line_api.reply_message(event.reply_token, message)

    elif '每日問答' in text:
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
                    PostbackTemplateAction(label=f'{op1}',data=f"{1-ans}"),
                    PostbackTemplateAction(label=f'{op2}',data=f"{2-ans}"),
                    PostbackTemplateAction(label=f'{op3}',data=f"{3-ans}"),])))
        line_api.reply_message(event.reply_token, message)
    elif '主食罐查詢' in text:
        message.append(TextMessage(text=f'請輸入你要查詢的品牌'))
        line_api.reply_message(event.reply_token, message)
    elif '乖乖吃飯' in text:
        message.append(TemplateSendMessage(
        alt_text='乖乖吃飯',
        template=ButtonsTemplate(
            title='乖乖吃飯',
            text='乖乖吃飯',
            thumbnail_image_url='https://i.imgur.com/D4a3Ale.jpg',
            actions=[
                    MessageTemplateAction(label='香煨嫩雞',text="香煨嫩雞"),
                    MessageTemplateAction(label='青魽凝鮨',text="青魽凝鮨"),
                    MessageTemplateAction(label='極品精鯛',text="極品精鯛"),
                    MessageTemplateAction(label='烈焰火雞',text="烈焰火雞"),
                    ])))
        line_api.reply_message(event.reply_token, message)
    elif '香煨嫩雞' in text:
        food = 乖乖吃飯.objects.filter(num = 0)
        
        for items in food:
            name = items.name
            price = items.price
            grans = items.grans
            protein = items.protein
            fat = items.fat
            carbo = items.carbo
            phos = items.phos
            kcal = items.kcal
            score = items.score
            message.append(TextSendMessage(text=f'{name}\n\n價格：{price}\n重量：{grans}\n蛋白質：{protein}\n\
            脂肪：{fat}\n碳水化合物：{carbo}\n磷含量：{phos}\n熱量：{kcal}\n推薦指數：{score}\n為這個罐罐評個分吧',
                        quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label=f"{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}", data="nothing")),
                            QuickReplyButton(action=PostbackAction(label=f"{stars}{stars}{stars}{stars}{stars}", data="nothing")),
                        ])))
        line_api.reply_message(event.reply_token, message)

    else:
        line_api.reply_message(event.reply_token,TextMessage(text=text))