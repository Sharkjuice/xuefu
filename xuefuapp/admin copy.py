from django.contrib import admin
from django import forms
from xuefuapp.models import Car,Fee,Owner,GroundQueue,UndergroundQueue,ST_PASS
from xuefuapp.views import port
import requests

admin.site.site_header = '学府花园'
admin.site.index_title = '车辆管理'
admin.site.site_url = '/xuefu/' 
#admin.site.site_header = 'My Site'

class CarAdminForm(forms.ModelForm):
    ground_queue_info =  forms.CharField(label="地面排队情况",required=False)
    underground_queue_info = forms.CharField(label='地库排队情况', required=False)
    class Meta:
        model = Car
        fields = ['ground_queue_info','underground_queue_info']
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)        


    def clean(self):
        cleaned_data = self.cleaned_data
        existing_cars = Car.objects.filter(room_id__iexact=cleaned_data.get('room_id')).all()
        if existing_cars:
            check = cleaned_data.get("car_of")
            count = 1
            for car in existing_cars:
                count += 1
                check += car.car_of
            if(check%count == 0):
                cleaned_data['total_cars'] = len(existing_cars)
            else:
                raise forms.ValidationError(u"此房号下同时有业主和租户车辆, 不符合要求,请处理!")

        return cleaned_data


class CarAdmin(admin.ModelAdmin):
    #fields = []
    #readonly_fields = [f.name for f in Car._meta.get_fields()]
    list_display = ('id','room_id','car_id','applicant_name','approve_status','apply_date')
    search_fields = ('room_id','car_id','applicant_name', 'contact')
    list_filter = ('approve_status','card_type','new_car','car_of')
    fieldsets = (
        ('基本信息',{'fields':('id','room_id','car_id','applicant_name','apply_date','applicant_id',
            'car_model', 'contact','underground_fix_no','new_car','car_of')}),
        ('审核信息',{'fields':('total_cars','card_type', 'approve_status','approve_id', 'process_info','notes')}),
        ('附件',{'fields':('doc_hukouben_1','doc_hukouben_2', 'doc_shenfenzheng_1','doc_shenfenzheng_2',
            'doc_fangchanzheng', 'doc_jiehunzheng','doc_lihunzheng','doc_xingshizheng', 
            'doc_changzuxieyi_1', 'doc_changzuxieyi_2','doc_changzuxieyi_3','doc_changzuxieyi_4',
            'doc_changzuxieyi_5','doc_gongzhengshu_1','doc_gongzhengshu_2','doc_zulinhetong','doc_chengnuoshu')}),
        ('数据信息',{'fields':('create_at','change_at','created_by')})
        )
    form = CarAdminForm
    ordering = ['id']
    
    readonly_fields_for_administrator = ('created_by','create_at','change_at','total_cars')
    readonly_fields_for_operator = ('created_by','create_at','change_at','approve_status','approve_id', 'process_info','total_cars')

    def get_readonly_fields(self, request, obj=None):
        if request.user.username == "admin":
            return self.readonly_fields_for_administrator
        if request.user.groups.filter(name='管理人员').exists():
            return self.readonly_fields_for_administrator
        elif request.user.groups.filter(name='操作人员').exists():
            return self.readonly_fields_for_operator
        else:
            return self.fieldsets[0][1]['fields'] + self.fieldsets[1][1]['fields'] + \
                self.fieldsets[2][1]['fields'] + self.fieldsets[3][1]['fields']

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user.username
            if obj.total_cars == 0:
                obj.total_cars  = 1
            else:
                existing_cars = Car.objects.filter(room_id__iexact=obj.room_id).all()
                car_count = len(existing_cars) + 1
                obj.total_cars  = car_count
                for car in existing_cars:
                    car.total_cars = car_count
                    car.save()
        obj.save()

    def delete_model(self, request, obj):
        room_id = obj.room_id
        obj.delete()
        existing_cars = Car.objects.filter(room_id__iexact=room_id).all()
        for car in existing_cars:
            car.total_cars = len(existing_cars)
            car.save()

class OwnerAdmin(admin.ModelAdmin):
    DOMAIN_NAME = 'https://api-cloud.thinmoo.com'
    TOKEN_PATH =  'platCompany/extapi/getAccessToken'
    ADD_PATH = 'persEmpHousehold/extapi/add'
    DEL_PATH = 'persEmpHousehold/extapi/delete'
    #API服务集成接口秘钥:  
    APP_ID = '1f21ac4a98564a9ca809cd3539267f73'
    APP_Secret = '5d424749888f20b5186437349c4ef0f9'
    COMMUNITY_ID = 44572

    list_display = ('room_id','owner_name','contact')
    search_fields = ('room_id','owner_name','contact')
    list_filter = ('approve_status',)
    fieldsets = (
        ('基本信息',{'fields':('room_id','owner_name','owner_id','contact','wx_id')}),
        ('审核信息',{'fields':('approve_status', 'note')}),    
        ('数据信息',{'fields':('create_at','change_at','created_by')})
        )
    
    readonly_fields_for_administrator = ('created_by','create_at','change_at','wx_id')
    readonly_fields_for_operator = ('created_by','create_at','change_at','approve_status','wx_id')

    def get_readonly_fields(self, request, obj=None):
        if request.user.username == "admin":
            return self.readonly_fields_for_administrator
        if request.user.groups.filter(name='管理人员').exists():
            return self.readonly_fields_for_administrator
        elif request.user.groups.filter(name='操作人员').exists():
            return self.readonly_fields_for_operator
        else:
            return self.fieldsets[0][1]['fields'] + self.fieldsets[1][1]['fields'] + \
                self.fieldsets[2][1]['fields']


    def save_model(self, request, obj, form, change):
        #API服务接口域名: 
        if change:
            url = "{}/{}?appId={}D&appSecret={}".format(OwnerAdmin.DOMAIN_NAME, OwnerAdmin.TOKEN_PATH, OwnerAdmin.APP_ID, OwnerAdmin.APP_Secret)
            resp = requests.get(url)
            res = resp.json()
            if res['code'] == 0:
                data = res['data']
                if obj.approve_status == ST_PASS:
                    #注册用户到门禁系统
                    url = '{}/{}'.format(OwnerAdmin.DOMAIN_NAME, OwnerAdmin.ADD_PATH)
                    form_data = {
                        'accessToken': data.accessToken,
                        'extCommunityId': OwnerAdmin.COMMUNITY_ID,
                        'name':  obj.owner_name,
                        'phone': obj.contact,
                        'roomIds': obj.room_id,
                        'uuid': obj.wx_id
                    }
                    res = requests.post(url,data=form_data)
                    print("注册用户结果: ")
                    print(res)
                else:
                    url = '{}/{}'.format(OwnerAdmin.DOMAIN_NAME, OwnerAdmin.DEL_PATH)
                    #取消注册
                    form_data = {
                        'accessToken': data.accessToken,
                        'extCommunityId': OwnerAdmin.COMMUNITY_ID,
                        'uuids': obj.wx_id
                    }
                    res = requests.post(url,data=form_data)
                    print("删除用户结果: ")
                    print(res)
            else:
                print("获取门禁系统token失败:")
                print(res)
        else:
            # the object is being created, so set the user
            obj.created_by = request.user.username
        obj.save()

    def delete_model(self, request, obj):
        url = "{}/{}?appId={}D&appSecret={}".format(OwnerAdmin.DOMAIN_NAME, OwnerAdmin.TOKEN_PATH, OwnerAdmin.APP_ID, OwnerAdmin.APP_Secret)
        resp = requests.get(url)
        res = resp.json()
        if res['code'] == 0:
            data = res['data']
            url = '{}/{}'.format(OwnerAdmin.DOMAIN_NAME, OwnerAdmin.DEL_PATH)
            #取消注册
            form_data = {
                'accessToken': data.accessToken,
                'extCommunityId': OwnerAdmin.COMMUNITY_ID,
                'uuids': obj.wx_id
            }
            res = requests.post(url,data=form_data)
            print("删除用户结果: ")
            print(res)
        obj.delete()

class QueueAdmin(admin.ModelAdmin):
    #fields = []
    readonly_fields = [f.name for f in GroundQueue._meta.get_fields()]
    list_display = ('car_id', 'apply_date','apply_id', 'process_status','complete_date')
    search_fields = ('car_id',)
    list_filter = ('process_status',)
    
    readonly_fields_for_administrator = ('created_by','create_at','change_at')
    readonly_fields_for_operator = ('created_by','create_at','change_at','process_status',
        'approve_id', 'complete_date')
    ordering = ['apply_id']

    def get_readonly_fields(self, request, obj=None):
        if request.user.username == "admin":
            return self.readonly_fields_for_administrator
        if request.user.groups.filter(name='管理人员').exists():
            return self.readonly_fields_for_administrator
        elif request.user.groups.filter(name='操作人员').exists():
            return self.readonly_fields_for_operator
        else:
            return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()            


class FeeAdmin(admin.ModelAdmin):
    #fields = []
    #readonly_fields = [f.name for f in Fee._meta.get_fields()]
    list_display = ('room_id','total_fee','total_fee_range','total_fee_months')
    search_fields = ('room_id',)
    list_filter = ('total_fee_months',)

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()             


class Port():
    class Meta:
        verbose_name = '导入导出'
        model_name = 'port'
        app_label = 'xuefuapp'
        abstract = False
        swapped = False
        app_config = False
        verbose_name_plural = "导入或导出文件"
        object_name = 'port'

    _meta = Meta


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):
        return port(request)
    
    def add_view(self, request, object_id=None, form_url='', extra_context=None):
        return port(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return port(request)

# Register your models here.
admin.site.register(Car, CarAdmin)
admin.site.register(GroundQueue, QueueAdmin)
admin.site.register(UndergroundQueue,QueueAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(Owner,OwnerAdmin)
#admin.site.register(Port, PortAdmin)

