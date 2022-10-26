from django.db import models
from functools import partial
from .storage import OverwriteStorage

# Create your models here.
def hukouben_path(p, instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "hukouben/hkb_{}_{}_{}.{}".format(instance.room_id, instance.car_id, p,suffix)

def shenfenzheng_path(p, instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "shenfenzheng/sfz_{}_{}_{}.{}".format(instance.room_id, instance.car_id, p, suffix)

def fangchanzheng_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "fangchanzheng/fcz_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)

def jiehunzheng_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "jiehunzheng/jhz_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)

def lihunzheng_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "lihunzheng/lhz_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)

def changzuxieyi_path(p,instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "changzuxieyi/czxy_{}_{}_{}.{}".format(instance.room_id, instance.car_id, p, suffix)

def xingshizheng_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "xingshizheng/xsz_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)

def changzuxieyi_path(p,instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "changzuxieyi/czxy_{}_{}_{}.{}".format(instance.room_id, instance.car_id, p, suffix)

def gongzhengshu_path(p, instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "gongzhengshu/gzs_{}_{}_{}.{}".format(instance.room_id, instance.car_id, p,suffix)

def zulinhetong_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "zulinhetong/zlht_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)

def chengnuoshu_path(instance,filename):
     #获得文件后缀
     suffix = filename.split(".")[-1]
     return "chengnuoshu/cns_{}_{}.{}".format(instance.room_id, instance.car_id, suffix)


hukouben_path_1 = partial(hukouben_path, 1)
hukouben_path_2 = partial(hukouben_path, 2)
shenfenzheng_path_1 = partial(shenfenzheng_path, 1)
shenfenzheng_path_2 = partial(shenfenzheng_path, 2)
changzuxieyi_path_1 = partial(changzuxieyi_path, 1)
changzuxieyi_path_2 = partial(changzuxieyi_path, 2)
changzuxieyi_path_3 = partial(changzuxieyi_path, 3)
changzuxieyi_path_4 = partial(changzuxieyi_path, 4)
changzuxieyi_path_5 = partial(changzuxieyi_path, 5)
gongzhengshu_path_1 = partial(gongzhengshu_path, 1)
gongzhengshu_path_2 = partial(gongzhengshu_path, 2)


ST_CHECKING = 1
ST_PASS = 2
ST_NO_PASS = 3
ST_OVERDUE = 4
ST_UNKNOWN = 5
#枚举值元数据
STATUS_TYPE = [(ST_CHECKING,"待核验"), (ST_PASS,"通过"),(ST_NO_PASS,"不通过"),
     (ST_UNKNOWN,'资料不全'),(ST_OVERDUE,'欠费')]

class Car(models.Model):
     CAR_OF_OWNER = 1
     CAR_OF_RENTER = 2

     CAR_OF = [(CAR_OF_OWNER,"业主"),(CAR_OF_RENTER,"租户")]

     #卡类型
     CT_GROUND_MONTH = 1
     CT_GROUND_TEMP = 2
     CT_UNDERGROUND_MONTH = 3
     CT_UNDERGROUND_LONGTERM = 4
     CT_OTHER = 5
     #枚举值元数据
     CARD_TYPE = [(CT_GROUND_MONTH,"地面月卡"),(CT_GROUND_TEMP,"地面临时"),
      (CT_UNDERGROUND_MONTH,"地库月卡"), (CT_UNDERGROUND_LONGTERM,"地库固定"),(CT_OTHER,"其它")]
     #自动生成字段
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)
     id = models.IntegerField(verbose_name="序号", unique=True)
     #业务字段
     room_id = models.CharField(max_length=20,verbose_name="房间号码")
     car_id = models.CharField(max_length=20,verbose_name="车牌号码",primary_key=True)
     car_model = models.CharField(max_length=100,verbose_name="车型",null=True,blank=True)
     applicant_name = models.CharField(max_length=20,verbose_name="申请人")
     applicant_id = models.CharField(max_length=20,verbose_name="身份证号码", null=True,blank=True)
     apply_date = models.DateField(auto_now=False, auto_now_add=False,verbose_name="申请日期")
     contact = models.CharField(max_length=100,verbose_name="联系电话", null=True,blank=True)
     card_type = models.IntegerField(choices=CARD_TYPE,verbose_name="卡类型", default=CT_OTHER)
     total_cars = models.IntegerField(verbose_name="一户登记车辆次数",default=1)
     new_car = models.BooleanField(verbose_name="新车入场",default=False)
     car_of = models.IntegerField(choices= CAR_OF,verbose_name="业主/租户",default=1)

     approve_id = models.CharField(max_length=20,verbose_name="认证编号",null=True,blank=True)
     approve_status = models.IntegerField(choices=STATUS_TYPE,verbose_name="审核状态",default=ST_CHECKING)
     notes = models.CharField(max_length=200,verbose_name="备注",null=True,blank=True)
     doc_hukouben_1 = models.FileField(upload_to=hukouben_path_1, max_length=100,
          storage=OverwriteStorage(),verbose_name="户口本页面1",null=True,blank=True)
     doc_hukouben_2 = models.FileField(upload_to=hukouben_path_2,max_length=100,
          storage=OverwriteStorage(),verbose_name="户口本页面2",null=True,blank=True)
     doc_shenfenzheng_1 = models.FileField(upload_to=shenfenzheng_path_1, max_length=100,
          storage=OverwriteStorage(),verbose_name="身份证",null=True,blank=True)
     doc_shenfenzheng_2 = models.FileField(upload_to=shenfenzheng_path_2, max_length=100,
          storage=OverwriteStorage(),verbose_name="身份证反面",null=True,blank=True)
     doc_fangchanzheng = models.FileField(upload_to=fangchanzheng_path, max_length=100,
          storage=OverwriteStorage(),verbose_name="房产证",null=True,blank=True)
     doc_jiehunzheng = models.FileField(upload_to=jiehunzheng_path, max_length=100,
          storage=OverwriteStorage(),verbose_name="结婚证",null=True,blank=True)
     doc_lihunzheng = models.FileField(upload_to=lihunzheng_path, max_length=100,
          storage=OverwriteStorage(),verbose_name="离婚证",null=True,blank=True)
     doc_xingshizheng = models.FileField(upload_to=xingshizheng_path, max_length=4000,
          storage=OverwriteStorage(),verbose_name="行驶证",null=True,blank=True)
     doc_changzuxieyi_1 = models.FileField(upload_to=changzuxieyi_path_1, max_length=100,
          storage=OverwriteStorage(),verbose_name="长租协议页面1",null=True,blank=True)
     doc_changzuxieyi_2 = models.FileField(upload_to=changzuxieyi_path_2, max_length=100,
          storage=OverwriteStorage(),verbose_name="长租协议页面2",null=True,blank=True)
     doc_changzuxieyi_3 = models.FileField(upload_to=changzuxieyi_path_3, max_length=100,
          storage=OverwriteStorage(),verbose_name="长租协议页面3",null=True,blank=True)
     doc_changzuxieyi_4 = models.FileField(upload_to=changzuxieyi_path_4, max_length=100,
          storage=OverwriteStorage(),verbose_name="长租协议页面4",null=True,blank=True)
     doc_changzuxieyi_5 = models.FileField(upload_to=changzuxieyi_path_5, max_length=100,
          storage=OverwriteStorage(),verbose_name="长租协议页面5",null=True,blank=True)
     doc_gongzhengshu_1 = models.FileField(upload_to=gongzhengshu_path_1, max_length=100,
          storage=OverwriteStorage(),verbose_name="公证书页面1",null=True,blank=True)
     doc_gongzhengshu_2 = models.FileField(upload_to=gongzhengshu_path_2, max_length=100,
          storage=OverwriteStorage(),verbose_name="公证书页面2",null=True,blank=True)
     doc_zulinhetong = models.FileField(upload_to=zulinhetong_path, max_length=100,
          storage=OverwriteStorage(),verbose_name="租赁合同页面",null=True,blank=True)
     doc_chengnuoshu = models.FileField(upload_to=chengnuoshu_path, max_length=100,
          storage=OverwriteStorage(),verbose_name="承诺书页面",null=True,blank=True)

     process_info = models.CharField(max_length=100, verbose_name="处理情况",null=True,blank=True)
     underground_fix_no = models.IntegerField(verbose_name="地库车位号",null=True,blank=True)

     class Meta:
          verbose_name = "车辆"
          verbose_name_plural = "所有车辆"

     def __str__(self):
          return "{}:{}".format("车辆:", self.car_id)

     def card_type_str(self):
          for item in Car.CARD_TYPE:
               if self.card_type == item[0]:
                    return item[1]
          else:
               return "无效值"

     def approve_status_str(self):
          for item in STATUS_TYPE:
               if self.approve_status == item[0]:
                    return item[1]
          else:
               return "无效值"

     def approve_id_str(self):
          if self.approve_id:
               return self.approve_id
          else:
               return "无"

class Fee(models.Model):
     id = models.AutoField(primary_key=True, verbose_name="内部ID") 
     room_id = models.CharField(max_length=20,verbose_name="房间号码")
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)

     total_fee = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="合计欠费", default=0)
     total_fee_range = models.CharField(max_length=100,verbose_name="合计欠费期间", null=True, blank=True)
     total_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     prop_fee = models.DecimalField (max_digits=10,decimal_places=2,verbose_name="住宅物管费欠费",default=0)
     prop_fee_range = models.CharField(max_length=100,verbose_name="住宅物管费欠费周期",null=True,blank=True)
     prop_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     busi_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商业物管费欠费",default=0)
     busi_fee_range = models.CharField(max_length=100,verbose_name="商业物管费欠费周期",null=True,blank=True)
     busi_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     water_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="水费欠费",default=0)
     water_fee_range = models.CharField(max_length=100,verbose_name="水费欠费周期",null=True,blank=True)
     water_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     power_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="电费欠费",default=0)
     power_fee_range = models.CharField(max_length=100,verbose_name="电费欠费周期",null=True,blank=True)
     power_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     sewage_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="排污费欠费",default=0)
     sewage_fee_range = models.CharField(max_length=100,verbose_name="排污费欠费周期",null=True,blank=True)
     sewage_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     garbage_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="垃圾处置费欠费",default=0)
     garbage_fee_range = models.CharField(max_length=100,verbose_name="垃圾处置费欠费周期",null=True,blank=True)
     garbage_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)

     base_fee = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="本体维修基金欠费",default=0)
     base_fee_range = models.CharField(max_length=100,verbose_name="本体维修基金欠费周期",null=True,blank=True)
     base_fee_months = models.IntegerField(verbose_name="合计欠费月数", default=0)
     notes = models.CharField(max_length=100,verbose_name="备注", null=True,blank=True)

     class Meta:
          verbose_name = "业主欠费"
          verbose_name_plural = "所有业主欠费"

     def __str__(self):
          return "{}:{}".format("欠费房号:", self.room_id)


class Owner(models.Model):
     id = models.AutoField(primary_key=True, verbose_name="内部ID")
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)
     room_id = models.CharField(max_length=20,verbose_name="房间号码")
     owner_name = models.CharField(max_length=20,verbose_name="业主姓名")
     owner_id = models.CharField(max_length=20,verbose_name="身份证号码", null=True,blank=True)
     contact = models.CharField(max_length=100,verbose_name="联系电话")
     wx_id = models.CharField(max_length=100,verbose_name="开放ID", null=True,blank=True)
     approve_status = models.IntegerField(choices=STATUS_TYPE,verbose_name="确认状态", default=1)
     note = models.CharField(max_length=100,verbose_name="备注", null=True,blank=True)
     class Meta:
          verbose_name = "业主联系信息"
          verbose_name_plural = "所有业主联系信息"          

     def approve_status_str(self):
          for item in Car.STATUS_TYPE:
               if self.approve_status == item[0]:
                    return item[1]
          else:
               return "无效值"

     def __str__(self):
          return "{}:{}".format("房号:", self.room_id)


QS_WAITING = 0
QS_CALLED = 1
QS_COMPLETED = 2
QS_CANCEL = 3
#枚举值元数据
PROCESS_STATUS = [(QS_WAITING,"等待中"), (QS_CALLED,"待办理"),(QS_COMPLETED,"已办理"),(QS_CANCEL,"撤销")]
class GroundQueue(models.Model):
     #自动生成字段
     id = models.AutoField(primary_key=True, verbose_name="内部ID") 
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)

     #业务字段
     car = models.ForeignKey(Car,related_name='ground_queue_info',on_delete=models.CASCADE,
          verbose_name="车牌号码")
     apply_date = models.DateField(verbose_name="申请日期",null=True,blank=True)
     apply_id = models.IntegerField(verbose_name="排队申请号", unique=True)
     process_status = models.IntegerField(choices=PROCESS_STATUS,verbose_name="办理情况",default=QS_WAITING)
     complete_date = models.DateField(verbose_name="完成日期",null=True,blank=True)
     notes = models.CharField(max_length=100,verbose_name="备注",null=True,blank=True)

     class Meta:
          verbose_name = "地面排队"
          verbose_name_plural = "所有地面排队"

     def __str__(self):
          return "{}:{}".format("车辆:", self.car_id)

     def process_status_str(self):
          for item in PROCESS_STATUS:
               if self.process_status == item[0]:
                    return item[1]
          else:
               return "无效值"

class UndergroundQueue(models.Model):
     #自动生成字段
     id = models.AutoField(primary_key=True, verbose_name="内部ID") 
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)
     #业务字段
     car= models.ForeignKey(Car,  related_name='underground_queue_info', on_delete=models.CASCADE,
          verbose_name="车牌号码")
     apply_date = models.DateField(verbose_name="申请日期",null=True,blank=True)
     apply_id = models.IntegerField(verbose_name="排队申请号", unique=True)
     process_status = models.IntegerField(choices=PROCESS_STATUS,verbose_name="办理情况",default=QS_WAITING)
     complete_date = models.DateField(verbose_name="完成日期",null=True,blank=True)
     notes = models.CharField(max_length=100,verbose_name="备注",null=True,blank=True)

     class Meta:
          verbose_name = "地库排队"
          verbose_name_plural = "所有地库排队"

     def __str__(self):
          return "{}:{}".format("车辆:", self.car_id)

     def process_status_str(self):
          for item in PROCESS_STATUS:
               if self.process_status == item[0]:
                    return item[1]
          else:
               return "无效值"

class UndergroundQueue2(models.Model):
     #自动生成字段
     id = models.AutoField(primary_key=True, verbose_name="内部ID") 
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="录入日期")
     change_at = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="修改日期")
     created_by = models.CharField(max_length=20, verbose_name="录入人员",null=True,blank=True)
     #业务字段
     car= models.ForeignKey(Car,  related_name='underground_queue_info_2', on_delete=models.CASCADE,
          verbose_name="车牌号码")
     apply_date = models.DateField(verbose_name="申请日期",null=True,blank=True)
     apply_id = models.IntegerField(verbose_name="排队申请号", unique=True)
     process_status = models.IntegerField(choices=PROCESS_STATUS,verbose_name="办理情况",default=QS_WAITING)
     complete_date = models.DateField(verbose_name="完成日期",null=True,blank=True)
     notes = models.CharField(max_length=100,verbose_name="备注",null=True,blank=True)

     class Meta:
          verbose_name = "地库排队2"
          verbose_name_plural = "所有地库排队2"

     def __str__(self):
          return "{}:{}".format("车辆:", self.car_id)

     def process_status_str(self):
          for item in PROCESS_STATUS:
               if self.process_status == item[0]:
                    return item[1]
          else:
               return "无效值"


OP_IMPORT = 0
OP_EXPORT = 1
#枚举值元数据
PORT_STATUS = [(OP_IMPORT,"导入文件"), (OP_EXPORT,"导出文件")]
class Port(models.Model):
     id = models.AutoField(primary_key=True, verbose_name="内部ID") 
     create_at = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="操作日期")
     created_by = models.CharField(max_length=20, verbose_name="操作人员")
     filename = models.CharField(max_length=100, verbose_name="文件名称")
     filetype = models.CharField(max_length=20, verbose_name="文件类型")
     operation = models.IntegerField(choices=PORT_STATUS,verbose_name="文件操作",default=OP_IMPORT)
     class Meta:
          verbose_name = "导入导出文件"
          verbose_name_plural = "导入导出文件"

     def filetype_str(self):
          if self.filetype == 'fee':
               return "物业管理费"
          if self.filetype == 'car':
               return "车辆列表"

          if self.filetype == 'ground':
               return "地面车库排队列表"

          if self.filetype == 'underground':
               return "地下车库排队列表"

          return "其它文件"

     def operation_str(self):
          for item in PORT_STATUS:
               if self.operation == item[0]:
                    return item[1]
          else:
               return "其它操作"

