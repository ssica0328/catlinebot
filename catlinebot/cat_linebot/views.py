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
            handle_message(event)
    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


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
            User_Info.objects.create(uid=user_id, name=display_name, pic_url=picture_url, text=text, mdt=now, points=0)
            message.append(TextMessage(text='會員資料新增完畢'))
        elif User_Info.objects.filter(uid=user_id).exists()==True:
            message.append(TextMessage(text='會員資料新增完畢'))
            user_info = User_Info.objects.filter(uid=user_id)
            for user in user_info:
                info = f'UID={user.uid}\nNAME={user.name}'
            message.append(TextSendMessage(text=info))
        line_api.reply_message(event.reply_token, message)
    else:
        line_api.reply_message(event.reply_token,TextMessage(text=text))