from time import strptime
from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions
from rest_framework import generics
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
import requests
from . import models,serializers
from datetime import datetime

import pdb
# Create your views here.

requests.packages.urllib3.disable_warnings()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cars': reverse('car-list', request=request, format=format),
        'ground': reverse('ground-list', request=request, format=format),
        'underground': reverse('underground-list', request=request, format=format),
        'fees': reverse('fee-list', request=request, format=format),
        'owners': reverse('owner-list', request=request, format=format),
        'open-door': reverse('open-door', request=request, format=format),

    })

@api_view(['GET'])
def ground_list(request, format=None):
    queue_status = request.query_params.get('status')
    cars = models.GroundQueue.objects.filter(process_status=queue_status).order_by('apply_id')
    serializer = serializers.GroundQueueSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def underground_list(request, format=None):
    queue_status = request.query_params.get('status')
    cars = models.UndergroundQueue.objects.filter(process_status=queue_status).order_by('apply_id')
    serializer = serializers.UndergroundQueueSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def car_detail(request, pk, format=None):
    try:
        car = models.Car.objects.get(pk=pk)
    except models.Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer =  serializers.CarSerializer(car)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer =  serializers.CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.created_by == request.user

class CarList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = models.Car.objects.all()
        #room_id = self.request.query_params.get('room_id')
        car_id = self.request.query_params.get("car_id")
            
        if car_id is not None:
                queryset = queryset.filter(car_id__icontains=car_id)
        else:
            queryset = models.Car.objects.none()

        return queryset


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsOwnerOrReadOnly]
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer

class FeeList(generics.ListCreateAPIView):
    queryset = models.Fee.objects.all()
    serializer_class = serializers.FeeSerializer

    def get_queryset(self):
        queryset = models.Fee.objects.all()
        room_id = self.request.query_params.get('room_id')
        input_code = self.request.query_params.get('code')

        org_code = models.Owner.objects.filter(room_id__iexact=room_id).first()
        if org_code.endswith(input_code):
            queryset = queryset.filter(room_id__icontains=room_id)
        else:
            queryset = models.Fee.objects.none()   

        return queryset

@api_view(['GET'])
def fee_list(request, format=None):
    room_id = request.query_params.get('room_id')
    input_code = request.query_params.get('code')
    wx_id = request.query_params.get('wx_id')
    org_code = ""
    if wx_id:
        org_code = models.Owner.objects.filter(room_id__iexact=room_id, wx_id__iexact=wx_id).first()
    else:
        org_code = models.Owner.objects.filter(room_id__iexact=room_id).first()

    fee = models.Fee.objects.none()
    serializer = serializers.FeeSerializer(fee, many=True)

    if not org_code or not input_code:
        return Response(serializer.data,status=400)

    if org_code.contact and org_code.contact.endswith(input_code):
        fee = models.Fee.objects.filter(room_id__icontains=room_id)
        serializer = serializers.FeeSerializer(fee, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.data,status=400)

class OwnerList(generics.ListCreateAPIView):
    queryset = models.Owner.objects.all()
    serializer_class = serializers.OwnerSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else: 
            return Response(serializer.errors,status=400)
       
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = models.Owner.objects.all()
        wx_id = self.request.query_params.get('wx_id')
        if wx_id is not None:
            print(wx_id)
            queryset = queryset.filter(wx_id=wx_id)
        else:
            queryset = models.Owner.none()
            print(wx_id)
        
        return queryset


class OwnerDetail(generics.RetrieveAPIView):
    queryset = models.Owner.objects.all()
    serializer_class = serializers.OwnerSerializer


import pdb
@api_view(['GET'])
def on_wx_login(request, format=None):
    auth = {
        'appid': 'wx217c5dad89320f30',
        'secret': '8e759d9372448f4caaf802c0365d211a',
        'js_code': request.query_params["code"],
        'grant_type':'authorization_code'
    }
    #pdb.set_trace()    
    response = requests.get("https://api.weixin.qq.com/sns/jscode2session?", params = auth, verify=False)
    #print("on_wx_login:", response)
    return Response(response.json())

DOMAIN_NAME = 'https://api-cloud.thinmoo.com'
TOKEN_PATH =  'platCompany/extapi/getAccessToken'
AUTH_PATH = '/persEmpHousehold/extapi/getAuthorizationDevList'
#API服务集成接口秘钥:  
APP_ID = '1f21ac4a98564a9ca809cd3539267f73'
APP_SECRET = '5d424749888f20b5186437349c4ef0f9'
COMMUNITY_ID = 44572
ACCESS_TOKEN = ''
TOKEN_EXPIRE_IN = 3600
TOKEN_CREATE_TIME = None
USER_DEV_MAP = {}

def updateAccessToken():
    global TOKEN_EXPIRE_IN,TOKEN_CREATE_TIME,ACCESS_TOKEN
    now = datetime.now()
    if(not ACCESS_TOKEN or (now - TOKEN_CREATE_TIME).seconds < TOKEN_EXPIRE_IN):
        print("getAccessToken from server")
        response = requests.get(
            '{}/{}?appId={}&appSecret={}'.format(DOMAIN_NAME, TOKEN_PATH, APP_ID, APP_SECRET),
            verify=False)
        res = response.json()
        print(res)
        if res['code'] == 0:
            data = res['data']
            TOKEN_CREATE_TIME = datetime.strptime(data['createTime'], "%Y-%m-%d %H:%M:%S")
            ACCESS_TOKEN = data['accessToken']
            TOKEN_EXPIRE_IN = data['expiresIn']
            return True
        else:
            return False                  
    else:
        print("getAccessToken from local")
        return True


def getUserDev(user_id):
    user_dev_list = USER_DEV_MAP.get(user_id)
    if(not user_dev_list):
        print("updateUserDev from server")
        url = '{}/{}'.format(DOMAIN_NAME, AUTH_PATH)
        data = {
            'accessToken': ACCESS_TOKEN,
            'extCommunityId': COMMUNITY_ID,
            'uuid': user_id
        }

        response = requests.get(url, params=data, verify=False)
        res = response.json()
        if res['code'] == 0:
            USER_DEV_MAP.update({user_id: res['data']})
            return res['data']
        else:
            print("getAccessToken from server error", res)
            return []
    else:
        print("getAccessToken from local")
        return []



@api_view(['POST','GET'])
@permission_classes([permissions.AllowAny])
def on_open_door(request):    
    #pdb.set_trace()
    secret = request.META.get("HTTP_X_SECRET_TOKEN")
    if secret != '8e759d9372448f4caaf802c0365d211a':
        print("二维码认证失败")
        return JsonResponse({"code":-1, "msg":"输入认证失败"},status=200)
    devSn = request.data.get('devSn')
    validData = request.data.get('validData')
    dataType = request.data.get('dataType')
    print(devSn, validData, dataType)    
    if not all([devSn,validData,dataType]):
        print("二维码认证参数无效")
        return JsonResponse({"code":-1, "msg":"输入参数无效"},status=200)
    data_tuple = validData.split("###")
    
    if(updateAccessToken()):
        user_dev_list = getUserDev(data_tuple[0])
        for dev in user_dev_list:
            if devSn == dev['devSn']:
                break                
        else:
            print("没有开门权限")
            return JsonResponse({"code":-1, "msg":"没有开门权限"},status=200)    
        return JsonResponse({"code":0, "msg":"成功"},status=200)
    else:
        print("获取平台token失败")
        return JsonResponse({"code":-1, "msg":"获取token失败"},status=200)


