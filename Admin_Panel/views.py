from django.shortcuts import render, redirect, HttpResponse
import json
import requests
from .models import Admin_Panel
from Admin_Panel.models import *
from .forms import  Admin_PanelCreate 
from datetime import datetime
# from firebase import firebase  
# from sseclient import SSEClient
from django.http import HttpResponse, JsonResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials,firestore

Config = {
  'apiKey': "AIzaSyCPDjNQL-3X4h_Kg24s91dObBJtkzK6EAw",
  'authDomain': "juno-production-87945.firebaseapp.com",
  'databaseURL': "https://juno-production-87945-default-rtdb.firebaseio.com",
  'projectId': "juno-production-87945",
  'storageBucket': "juno-production-87945.appspot.com",
  'messagingSenderId': "823135961210",
  'appId': "1:823135961210:web:ca9e3514b1b7cc71e8fbc3"
};


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db=firebase.database()
# firebase_admin.initialize_app(cred, {
#   'projectId': project_id,
# })
cred = credentials.Certificate("./juno-production-87945-firebase-adminsdk-is31l-8ebcc2253f.json")
firebase_admin.initialize_app(cred)
fdb = firestore.client()
#DataFlair
def signin(request):
    return render(request,'Admin_Panel/signin.html')


def index(request):
    email=request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user=auth.sign_in_with_email_and_password(email,passw)
        
    except:
        message="Invalid Credential"
        return render(request,"Admin_Panel/signin.html",{"messg":message})
    
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    # print(request.session['uid'])
    return redirect('userlist')



def logout(request):
    
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request, 'Admin_Panel/signin.html')
    

def userlist(request):
    
    try:
        idtoken=request.session['uid']
        users_ref = fdb.collection(u'user_master')
        docs = users_ref.stream()
        data_list = []
        for doc in docs:
            val=fdb.collection('user_master').document(doc.id).get()
            user_id=val.get('uid')
            wallet=fdb.collection('wallet').document(user_id).get()
            partner_name=val.get('last_consultation_partnerid')
            if(partner_name):
                partner_name_new=partner_name.split('$')[1]
            else:
                partner_name_new= 'No Consultation'
            
            # print(wallet.to_dict())
            user_info = {}
            # user_info['is_active']= val.get('is_active')
            user_info['is_active']=True
            user_info["id"] = doc.id
            user_info["name"] = val.get('name')
            user_info["email"] = val.get('email')
            user_info["nick_name"] = val.get('nick_name')
            user_info["amt"] = wallet.get('amt')

            last_consultation_date=val.get('last_consultation_date')
            if (last_consultation_date):
                lcd= datetime.strptime(last_consultation_date, '%Y-%m-%d %H:%M:%S')
                user_info["last_consultation_date"] = lcd.strftime("%d-%b-%Y %H:%M:%S")
                
            else:     
                user_info["last_consultation_date"] = last_consultation_date

            
            last_login_date=val.get('last_login_date')
            if (last_login_date):
                lld= datetime.strptime(last_login_date, '%Y-%m-%d %H:%M:%S')
                user_info["last_login_date"] = lld.strftime("%d-%b-%Y %H:%M:%S")        
            else:     
                user_info["last_login_date"] = last_login_date

            user_info["last_consultation_partnerid"] = partner_name_new

            user_create_date=val.get('user_create_date')
            if (user_create_date):
                ucd= datetime.strptime(user_create_date, '%Y-%m-%d %H:%M:%S')
                user_info["user_create_date"] = ucd.strftime("%d-%b-%Y %H:%M:%S")        
            else:     
                user_info["user_create_date"] = user_create_date

            user_info["status"] = val.get('status')
            user_info["uid"] = val.get('uid')
            data_list.append(user_info)
            # print(type(user_info["last_login_date"])
            # print(user_info["last_login_date"])
            # exit()
        

        # for i in result:
        #     print(result)
        #     val=fdb.collection('admin_master').document(result.id)
        #     print(val)
        #     
        # print(f'{doc.id} => {doc.email.to_dict()}')
        # shelf = Admin_Panel.objects.all()
        # print(shelf) 
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/Admin_Panel.html', {'data_list': data_list})  


def partnerlist(request):
    try:
        idtoken=request.session['uid']
        partners_ref = fdb.collection(u'partner_master')
        docs = partners_ref.stream()
        data_list = []
        for doc in docs:
            val=fdb.collection('partner_master').document(doc.id).get()
            partner_info = {}
            partner_info["id"] = doc.id
            partner_info["name"] = val.get('name')

            partner_info["email"] = val.get('email')
            # partner_info["Availble"] = val.get('Availble')
            partner_info["price"] = val.get('price')
            partner_info["session"] = val.get('Session')
            partner_info["Degree"] = val.get('Degree')
            partner_info["Experience"] = val.get('Session')
            partner_info["Expertise"] = val.get('Expertise')
            partner_info["balance"] = val.get('balance')
            partner_info["last_consultation_date"] = val.get('last_consultation_date')
            partner_info["last_consultation_id"] = val.get('last_consultation_id')
            partner_info["last_login"] = val.get('last_login')
            partner_info["voicecall_available"] = val.get('voicecall_availble')
            partner_info["videocall_available"] = val.get('videocall_availble')
            # partner_info["is_active"] = val.get('is_active')
            # partner_info["is_block"] = val.get('is_block')
        


            
            data_list.append(partner_info) 
            # ID=data_list.id
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/Admin_Panel_partner.html', {'data_list': data_list})


def user_call_detail(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        print(id)
        
        # print(id)  
        total_partners = fdb.collection('call_record/user/user/answered_call/answered_call').document(id).collection(id)
        docs=total_partners.stream()

        # print(* docs)

        detail_list = []
        for doc in docs:

            # print(doc.id)
            # partner_consult_ref=total_partners.document(doc.id)
            # consult=partner_consult_ref.stream()
        
            # for consultation in consult:
            #     val=fdb.collection('partner_master').document(doc.id).get()
            dtl=total_partners.document(doc.id).get()
            user_detail = {}
            user_detail["callCharges"] = dtl.get('callCharges')
            user_detail["callPrice"] = dtl.get('callPrice')
            user_detail["duration"] = dtl.get('duration')
            user_detail["end"] = dtl.get('end')
            # user_detail["end_time"] = dtl.get('start')
            user_detail["from"] = dtl.get('from')
            user_detail["to"] = dtl.get('to')
            user_detail["topic"] = dtl.get('topic')
            detail_list.append(user_detail)   
        # print(* detail_list) 
        # print(* detail_list) 
        # return HttpResponse(detail_list)
        # return JsonResponse(detail_list, safe=False)
        # return redirect('detail')
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/call_detail.html', {'detail_list': detail_list})


def partner_call_detail(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        
        # print(id)  
        total_partners = fdb.collection('call_record/partner/partner/answered_call/answered_call').document(id).collection(id)
        docs=total_partners.stream()

        # print(* docs)

        detail_list = []
        for doc in docs:

            # print(doc.id)
            # partner_consult_ref=total_partners.document(doc.id)
            # consult=partner_consult_ref.stream()
        
            # for consultation in consult:
            #     val=fdb.collection('partner_master').document(doc.id).get()
            dtl=total_partners.document(doc.id).get()
            user_detail = {}
            user_detail["callCharges"] = dtl.get('callCharges')
            user_detail["callPrice"] = dtl.get('callPrice')
            user_detail["duration"] = dtl.get('duration')
            user_detail["end"] = dtl.get('end')
            # user_detail["end_time"] = dtl.get('start')
            user_detail["from"] = dtl.get('from')
            user_detail["to"] = dtl.get('to')
            user_detail["topic"] = dtl.get('topic')
            detail_list.append(user_detail)   
        # print(* detail_list) 
        # print(* detail_list) 
        # return HttpResponse(detail_list)
        # return JsonResponse(detail_list, safe=False)
        # return redirect('detail')
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/call_detail.html', {'detail_list': detail_list})



def create_coupon(request):
    try:
        idtoken=request.session['uid']
        import time 
        from datetime import datetime, timezone
        import pytz
        tz=pytz.timezone('Asia/Kolkata')
        # print(tz)
        time_now=datetime.now(timezone.utc)
        # print(time_now)
        cid=str(int(time.mktime(time_now.timetuple())))
        # print(cid)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        # idtoken=request.session['uid']
        # a=auth.get_account_info(idtoken)
        # a=a['users']
        # a=a[0]
        # a=a['localId']
        # print (a)
        expiry_date=request.POST.get('expiry')
        
        expd= datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M')
        expiry = expd.strftime("%d-%m-%Y %H:%M:00")
        # print(expiry)
        data = {
        u'amount':request.POST.get('amount'),
        u'counter': request.POST.get('counter'),
        u'created_date_time': dt_string,
        'id': cid,
        u'name': request.POST.get('name'),
        u'expiry': expiry,
        u'status': u'Success',
        u'is_active': True
        }
        fdb.collection(u'coupon').document(cid).set(data)
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return redirect('coupons')


def coupons(request):
    try:
        idtoken=request.session['uid']
        coupon_ref = fdb.collection(u'coupon')
        docs = coupon_ref.stream()
        data_list = []
        for doc in docs:
            val=fdb.collection('coupon').document(doc.id).get()
            coupon_info = {}
            coupon_info["id"] = doc.id
            coupon_info["name"] = val.get('name')
            coupon_info["amount"] = val.get('amount')
            coupon_info["expiry"] = val.get('expiry')
            coupon_info["status"] = val.get('status')
            coupon_info["created_date_time"]=val.get('created_date_time')
            coupon_info["counter"] = val.get('counter')
                
            data_list.append(coupon_info) 
            # ID=data_list.id
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/coupon.html', {'data_list': data_list})


def user_missed_call_report(request):

    
    try:
        idtoken=request.session['uid']
        users_ref = fdb.collection(u'user_master')
        docs = users_ref.stream()
        data_list = []
        for doc in docs:
            call_records = fdb.collection('call_record/user/user/missed_call/missed_call').document(doc.id).collection(doc.id)
            users=call_records.stream()
            for user in users:
                val=call_records.document(user.id).get()            
                # print(wallet.to_dict())
                
                call_info = {}
                call_info["name"] = val.get('from')
                call_info["partnername"] = val.get('to')
                time= val.get('start')
                if (time):
                    cdt= datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    call_info["time"] = cdt.strftime("%d-%b-%Y %H:%M:%S")
                else:     
                    call_info["time"] = time
                call_info["topic"] = val.get('topic')
                call_info["calltype"] = val.get('callType')
                data_list.append(call_info)
                # print(type(user_info["last_login_date"])
                # print(user_info["last_login_date"])
                # exit()
        # print(*data_list)
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/missed_call_report.html', {'data_list': data_list})  

def user_inactive(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        user_profile=fdb.collection(u'user_master').document(id)
        if(user_profile.get().get(u'is_active')):
            user_profile.set({
                u'is_active':False
            }, merge=True)
        else:
            user_profile.set({
                u'is_active':True
            }, merge=True)
        

        # check_active=user_profile.get().get(u'is_active')
        is_active={
            "check_active":user_profile.get().get(u'is_active')
        }
        # check_active.append(user_detail) 
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})

    return render(request, 'Admin_Panel/Admin_Panel.html',{'check_active': is_active})

def partner_inactive(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        user_profile=fdb.collection(u'user_master').document(id)
        if(user_profile.get().get(u'is_active')):
            user_profile.set({
                u'is_active':False
            }, merge=True)
        else:
            user_profile.set({
                u'is_active':True
            }, merge=True)


        # check_active=user_profile.get().get(u'is_active')
        is_active={
            "check_active":user_profile.get().get(u'is_active')
        }
        # check_active.append(user_detail) 
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})

    return render(request, 'Admin_Panel/Admin_Panel.html',{'check_active': is_active})


def call_modal(request):
    data=request.POST.get("data")
    print(*data)
    return render(request, 'Admin_Panel/Admin_Panel.html',{'data': data})

def edit(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        val=fdb.collection('partner_master').document(id).get()
        partner_info = {}
        partner_info["id"] = id
        partner_info["name"] = val.get('name')
        partner_info["email"] = val.get('email')
        partner_info["Location"] = val.get('Location')
        partner_info["mobilnumber"] = val.get('mobilnumber')
        partner_info["Languages_Spoken"] = val.get('Languages_Spoken')
        partner_info["Profile_Summary"] = val.get('Profile_Summary')
        partner_info["video_link"] = val.get('video_link')

        partner_info["ProfilePic"] = val.get('ProfilePic')
        partner_info["Rate"] = val.get('Rate')
        # partner_info["Availble"] = val.get('Availble')
        partner_info["price"] = val.get('price')
        partner_info["Degree"] = val.get('Degree')
        partner_info["Session"] = val.get('Session')
        partner_info["Expertise"] = val.get('Expertise')
        partner_info["balance"] = val.get('balance')
        partner_info["last_consultation_date"] = val.get('last_consultation_date')
        partner_info["last_consultation_id"] = val.get('last_consultation_id')
        partner_info["last_login"] = val.get('last_login')
        partner_info["topic"] = val.get('Topic')
        partner_info["is_active"] = val.get('is_active')
        partner_info["is_block"] = val.get('is_block')
        # partner_info["is_active"] = val.get('is_active')
        # partner_info["is_block"] = val.get('is_block')
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})

    return render(request, 'Admin_Panel/partner_form.html', {'detail':partner_info})

def user_wallet(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        name=fdb.collection('user_master').document(id).get().get('name')
        # print(name)
        path=id+'$'+name
        # print(path)
        user_collection=fdb.collection(u'wallet').document(path).get().get('history')
        # collections=user_collection
        # wallet_detail=[]
        # for doc in collections:
            
        #     # val=user_collection.get(doc)
        #     wallet_detail.append(doc)
        

        
        # print(user_collection)
        # return JsonResponse(user_collection, safe=False)
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/wallet.html',{'wallet_detail':user_collection})

def partner_wallet(request):
    try:
        idtoken=request.session['uid']
        id=request.POST.get("id")
        name=fdb.collection('partner_master').document(id).get().get('name')
        # print(name)
        path=id+'$'+name
        # print(path)
        user_collection=fdb.collection('wallet/partner/partner').document(path).get().get('history')
        # collections=user_collection
        # wallet_detail=[]
        # for doc in collections:
            
        #     # val=user_collection.get(doc)
        #     wallet_detail.append(doc)
        

        
        # print(user_collection)
        # return JsonResponse(user_collection, safe=False)
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/wallet.html',{'wallet_detail':user_collection})


def edit_detail(request):
    try:
        idtoken=request.session['uid']
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        id=request.POST.get('id')
        name=request.POST.get('name')
        price=request.POST.get('price')
        degree=request.POST.get('degree')
        session=request.POST.get('session')
        expertise=request.POST.get('expertise')
        location=request.POST.get('location')
        summary=request.POST.get('summary')
        videolink=request.POST.get('videolink')
        mobilenumber=request.POST.get('mobilenumber')
        language=request.POST.get('language')
        rate=request.POST.get('rate')
        is_active=request.POST.get('is_active')
        is_block=request.POST.get('is_block')
        # topic=request.POST.get('topic')/
        data={
            'name':name,
            'price':price,
            'Degree':degree,
            'Session':session,
            'Expertise':expertise,
            'Location':location,
            'Profile_Summary':summary,
            'video_link':videolink,
            'mobilnumber': mobilenumber,
            'Languages_Spoken':language,
            'Rate':rate,
            'is_active':eval(is_active),
            'is_block':eval(is_block),
            'last_updated': dt_string,
            'updated_by': 'Admin'
            # 'Topic':topic

        }
        fdb.collection('partner_master').document(id).update(data)
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return redirect('partnerlist')

def daily_report(request):
    try:
        idtoken=request.session['uid']
        # print(id)  
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        # print(dt_string)
        users_ref = fdb.collection(u'user_master')
        docs = users_ref.stream()
        detail_list = []
        for doc in docs:
            total_partners = fdb.collection('call_record/user/user/answered_call/answered_call').document(doc.id).collection(doc.id)
            docs2=total_partners.stream()

            # print(* docs)

            
            for doc2 in docs2:
                dtl=total_partners.document(doc2.id).get()
                consul=dtl.get('end')
                ucd= datetime.strptime(consul, '%Y-%m-%d %H:%M:%S')
                consul_date = ucd.strftime("%Y-%m-%d")
                # print(consul_date)
                if(consul_date==dt_string):
                # print(doc.id)
                # partner_consult_ref=total_partners.document(doc.id)
                # consult=partner_consult_ref.stream()
            
                # for consultation in consult:
                #     val=fdb.collection('partner_master').document(doc.id).get()
                
                    user_detail = {}
                    user_detail["callCharges"] = dtl.get('callCharges')
                    user_detail["callPrice"] = dtl.get('callPrice')
                    user_detail["duration"] = dtl.get('duration')
                    user_detail["end"] = dtl.get('end')
                    # user_detail["end_time"] = dtl.get('start')
                    user_detail["from"] = dtl.get('from')
                    user_detail["to"] = dtl.get('to')
                    user_detail["topic"] = dtl.get('topic')
                    detail_list.append(user_detail)   
        # print(* detail_list) 
        # print(* detail_list) 
        # return HttpResponse(detail_list)
        # return JsonResponse(detail_list, safe=False)
        # return redirect('detail')
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/daily_report.html', {'detail_list': detail_list})

def monthly_report(request):
    try:
        idtoken=request.session['uid']
            # print(id)  
        now = datetime.now()
        dt_string = now.strftime("%Y-%m")
        # print(dt_string)
        users_ref = fdb.collection(u'user_master')
        docs = users_ref.stream()
        detail_list = []
        for doc in docs:
            total_partners = fdb.collection('call_record/user/user/answered_call/answered_call').document(doc.id).collection(doc.id)
            docs2=total_partners.stream()

            # print(* docs)

            
            for doc2 in docs2:
                dtl=total_partners.document(doc2.id).get()
                consul=dtl.get('end')
                ucd= datetime.strptime(consul, '%Y-%m-%d %H:%M:%S')
                consul_date = ucd.strftime("%Y-%m")
                # print(consul_date)
                if(consul_date==dt_string):
                # print(doc.id)
                # partner_consult_ref=total_partners.document(doc.id)
                # consult=partner_consult_ref.stream()
            
                # for consultation in consult:
                #     val=fdb.collection('partner_master').document(doc.id).get()
                
                    user_detail = {}
                    user_detail["callCharges"] = dtl.get('callCharges')
                    user_detail["callPrice"] = dtl.get('callPrice')
                    user_detail["duration"] = dtl.get('duration')
                    user_detail["end"] = dtl.get('end')
                    # user_detail["end_time"] = dtl.get('start')
                    user_detail["from"] = dtl.get('from')
                    user_detail["to"] = dtl.get('to')
                    user_detail["topic"] = dtl.get('topic')
                    detail_list.append(user_detail)   
        # print(* detail_list) 
        # print(* detail_list) 
        # return HttpResponse(detail_list)
        # return JsonResponse(detail_list, safe=False)
        # return redirect('detail')
    except KeyError:
        message="Please login first"
        return render(request, 'Admin_Panel/signin.html', {'messg': message})
    return render(request, 'Admin_Panel/monthly_report.html', {'detail_list': detail_list})