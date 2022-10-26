from datetime import date,datetime
from django.db.utils import IntegrityError
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, reverse, redirect
from django.db.models import Sum
import pandas as pd

from . import filters,models,forms
from .storage import OverwriteStorage
from xuefusite import settings


import pdb
# Create your views here.

class FilterCarView(ListView):
    model = models.Car
    filterset_class = filters.CarFilter
    context_object_name = 'all'
    template_name = 'list_car.html'
    paginate_by = 20  # 每页记录个数
    ordering = ("id",)    # 排序字段列表
    #queryset =  models.Car.objects.all()

    def get_queryset(self):
        queryset = super(FilterCarView,self).get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(FilterCarView,self).get_context_data(**kwargs)
        context['filter'] = self.filterset
        # query_items = []
        # for k, v in self.request.GET.items():
        #     query_items.append(v)
        # if any(query_items):
        #     context['qs'] = self.filterset.qs
        # else:
        #     context['qs'] = models.Car.objects.all()
        return context

class FilterFeeView(ListView):
    model = models.Fee
    filterset_class = filters.FeeFilter
    context_object_name = 'all'
    template_name = 'list_fee.html'
    paginate_by = 20  # 每页记录个数
    ordering = ("-total_fee",)    # 排序字段列表
    #queryset =  models.Car.objects.all()

    def get_queryset(self):
        queryset = super(FilterFeeView,self).get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(FilterFeeView,self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filter'] = self.filterset
        return context

class CarDetailView(UpdateView): 
    model = models.Car 
    template_name = 'detail_car.html'
    form_class = forms.CarForm 

    def post(self, request, *args, **kwargs):
        return redirect(reverse('car_query'))


class FeeDetailView(UpdateView):
    model = models.Fee
    form_class = forms.FeeForm 
    template_name = 'detail_fee.html'

    def post(self, request, *args, **kwargs):
        return redirect(reverse('fee_list'))

class FilterGroundView(ListView):
    model = models.GroundQueue
    filterset_class = filters.QueueFilter
    context_object_name = 'all'
    template_name = 'list_ground.html'
    paginate_by = 20  # 每页记录个数
    ordering = ("apply_id",)    # 排序字段列表

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        #pdb.set_trace()
        queryset = super(FilterGroundView,self).get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(FilterGroundView,self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filter'] = self.filterset
        context['url_name'] = 'ground_list'
        return context

class FilterUndergroundView(ListView):
    model = models.UndergroundQueue
    filterset_class = filters.QueueFilter
    context_object_name = 'all'
    template_name = 'list_ground.html'
    paginate_by = 20  # 每页记录个数
    ordering = ("apply_id",)    # 排序字段列表
    #queryset =  models.Car.objects.all()

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        #pdb.set_trace()
        queryset = super(FilterUndergroundView,self).get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(FilterUndergroundView,self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filter'] = self.filterset
        context['url_name'] = 'underground_list'
        return context

class FilterUndergroundView2(ListView):
    model = models.UndergroundQueue2
    filterset_class = filters.QueueFilter
    context_object_name = 'all'
    template_name = 'list_ground.html'
    paginate_by = 20  # 每页记录个数
    ordering = ("apply_id",)    # 排序字段列表
    #queryset =  models.Car.objects.all()

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        #pdb.set_trace()
        queryset = super(FilterUndergroundView2,self).get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(FilterUndergroundView2,self).get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filter'] = self.filterset
        context['url_name'] = 'underground_list_2'
        return context


#202202-202204;
#202202(500.00);202204(1000.00);
def get_normal_range(date_range_string):
    if pd.isnull(date_range_string):
        return 0
    #去掉末尾的;
    print('get_normal_range', date_range_string)
    date_range_string = date_range_string.rstrip(";")
    date_range_list = date_range_string.split(";")
    month_count = 0
    for data_range in date_range_list:
        #分割by '-'
        date_tuple = data_range.split("-")
        #判断是有一个来时两个
        if len(date_tuple) == 2:
            begin_y = int(date_tuple[0][:4])
            end_y = int(date_tuple[1][:4])
            begin_m = int(date_tuple[0][4:6])
            end_m = int(date_tuple[1][4:6])
            month_count +=  (end_y-begin_y)*12 + end_m - begin_m + 1
        else:
            month_count += 1
    return (date_range_string, month_count)
    
    
def get_default(value):
    return 0 if pd.isnull(value) else value

def port(request):
    errors = []
    code = 0
    if request.method == 'POST':
        if request.POST.get("upload_fee_file"):
            print("upload_fee_file")
            fee_file = request.FILES['select_fee_file']
            fs = OverwriteStorage()
            filename = fs.save(fee_file.name, fee_file)
            code, errors = import_file(filename,'fee', request.user.username)
        elif request.POST.get("upload_car_file"):
            fee_file = request.FILES['select_car_file']
            fs = OverwriteStorage()
            filename = fs.save(fee_file.name, fee_file)
            code, errors =   import_file(filename,'car', request.user.username)
        elif request.POST.get("upload_underground_queue_file"):
            fee_file = request.FILES['select_underground_queue_file']        
            fs = OverwriteStorage()
            filename = fs.save(fee_file.name, fee_file)
            code, errors =   import_file(filename,'underground', request.user.username)
        elif request.POST.get("upload_ground_queue_file"):
            fee_file = request.FILES['select_ground_queue_file']        
            fs = OverwriteStorage()
            filename = fs.save(fee_file.name, fee_file)
            code, errors =   import_file(filename,'ground', request.user.username)

        elif request.POST.get("download_fee_file"):
            print("download_fee_file")
            errors = ["下载欠费文件:", "还没有实现"]
        elif request.POST.get("download_car_file"):
            print("download_car_file")
            errors = ["下载车辆文件:","还没有实现"]

    form = forms.PortForm()
    all = models.Port.objects.all()
    return render(request, "port.html", {"form": form, 
        'has_error': code < 0, 'errors': errors, 'all': all})

def get_card_type(card_type_str):
    if card_type_str == "地面月卡":
        return models.Car.CT_GROUND_MONTH
    if card_type_str == "地库固定":
        return models.Car.CT_UNDERGROUND_LONGTERM

    if card_type_str == "地面临时":
        return models.Car.CT_GROUND_TEMP

    if card_type_str == "地库月卡":
        return models.Car.CT_UNDERGROUND_MONTH

    return models.Car.CT_OTHER

def get_status_type(status_type_str):
    if status_type_str == "通过":
        return models.ST_PASS
    if status_type_str == "待核验":
        return models.ST_CHECKING

    if status_type_str == "不通过":
        return models.ST_NO_PASS

    if status_type_str == "欠费":
        return models.ST_OVERDUE

    return models.ST_UNKNOWN

def process_row_fee(row):
    data = {}
    if pd.isnull(row[0]) or len(row[0]) < 4:
        return (1,)
    data['room_id'] = row[0]

    data['total_fee'] = get_default(row[1])               
    data['total_fee_months'] = 0
    if not pd.isnull(row[2]):                     
        range, months = get_normal_range(row[2])
        data['total_fee_range'] = range
        data['total_fee_months'] = months

    data['prop_fee'] = get_default(row[3])
    data['prop_fee_months'] = 0
    if not pd.isnull(row[4]):
        range, months = get_normal_range(row[4])
        data['prop_fee_range'] = range
        data['prop_fee_months'] = months

    data['busi_fee'] =  get_default(row[5])
    data['busi_fee_months'] = 0
    if not pd.isnull(row[6]):                     
        range, months = get_normal_range(row[6])
        data['busi_fee_range'] = range
        data['busi_fee_months'] = months

    data['water_fee'] =  get_default(row[7])
    data['water_fee_months'] = 0
    if not pd.isnull(row[8]):                     
        range, months = get_normal_range(row[8])
        data['water_fee_range'] = range
        data['water_fee_months'] = months

    data['power_fee'] =  get_default(row[9])
    data['power_fee_months'] = 0
    if not pd.isnull(row[10]):                     
        range, months = get_normal_range(row[10])
        data['power_fee_range'] = range
        data['power_fee_months'] = months

    data['sewage_fee'] =  get_default(row[11])
    data['sewage_fee_months'] = 0
    if not pd.isnull(row[12]):                     
        range, months = get_normal_range(row[12])
        data['sewage_fee_range'] = range
        data['sewage_fee_months'] = months

    data['garbage_fee'] = get_default(row[13])
    data['garbage_fee_months'] = 0
    if not pd.isnull(row[14]):                 
        range, months = get_normal_range(row[14])
        data['garbage_fee_range'] = range
        data['garbage_fee_months'] = months

    data['base_fee'] =  get_default(row[15])
    data['base_fee_months'] = 0
    if not pd.isnull(row[16]):
        range, months = get_normal_range(row[16])
        data['base_fee_range'] = range
        data['base_fee_months'] = months

    return (0, data)

def process_row_car(row):
    data = {}
    data['id'] = row[0]

    if len(row[1]) < 4:
        return (1,)
    data['room_id'] = row[1]

    data['car_id'] = row[2]
    data['applicant_name'] = row[3]

    if not pd.isnull(row[4]):
        data['car_model'] = row[4]    

    if not pd.isnull(row[5]):
        data['apply_date'] = date(year=row[5].year, month=row[5].month, day= row[5].day)
    else:
        data['apply_date'] = datetime.now().date()

    if not pd.isnull(row[6]):
        data['applicant_id'] = row[6]
    if not pd.isnull(row[7]):
        data['contact'] = row[7]

    if not pd.isnull(row[8]):
        data['card_type'] = get_card_type(row[8])

    if not pd.isnull(row[9]):
        data['underground_fix_no'] = row[9]

    if not pd.isnull(row[10]):
        data['new_car'] = True
    else:
        data['new_car'] = False

    if not pd.isnull(row[11]):
        data['total_cars'] = row[11]

    if not pd.isnull(row[12]):
        data['approve_id'] = row[12]

    data['approve_status'] = get_status_type(row[13])

    if not pd.isnull(row[14]):
        data['notes'] = row[14]

    return (0, data)

def process_row_queue(row):
    data = {}
    data['apply_id'] = row[0]
    data['car'] = models.Car.objects.filter(car_id=row[2]).first()

    if not pd.isnull(row[6]):
        data['apply_date'] = date(year=row[6].year, month=row[6].month, day= row[6].day)

    if not pd.isnull(row[12]):
        data['notes'] = row[12]
  
    #data['process_status'] = get_process_status(row[7])

    return (0, data)


def get_process_status(status_type_str):
    if status_type_str == "已办理":
        return models.QS_COMPLETED
    if status_type_str == "房子已卖":
        return models.QS_CANCEL

    return models.QS_WAITING


import_map = {
    "fee": (models.Fee, process_row_fee),
    "car": (models.Car, process_row_car),
    "ground": (models.GroundQueue, process_row_queue),
    "underground": (models.UndergroundQueue, process_row_queue)
}

def import_file(filename, filetype, username):
    try:
        worksheet = pd.read_excel(settings.MEDIA_ROOT + filename, sheet_name=0, skiprows=1, header=None)
    except Exception as err:
        code = -1
        content = ["上传文件失败:", err]
        return (code, content)
    #excel第一列是标题
    instances = []
    code = 0 
    content = []
    klass = import_map[filetype][0]
    process_row = import_map[filetype][1]
    for _, row in worksheet.iterrows(): 
        res = process_row(row)
        if res[0] == -1:
            code = -1
            content = ["上传文件失败:", res[1]]
            break
        elif res[0] == 1:
            continue
        else:
            try:
                instance = klass(**res[1])
                instance.created_by= username
                instances.append(instance)
            except ValueError as err:
                code = -1
                content = ["上传文件失败:",err]
                break
    else:
        try:
            klass.objects.all().delete()
            klass.objects.bulk_create(instances)
            code = 0
            content = ["上传文件成功:", filename, "共{}条数据".format(len(instances))]
            models.Port.objects.create(created_by=username, filename=filename, filetype=filetype, operation=models.OP_IMPORT)
        except IntegrityError as err:
            code = -1
            content = ["上传文件失败:", err]
    return (code, content)

def overview(request):
    total_cars = models.Car.objects.count()
    approved_cars = models.Car.objects.filter(approve_id__isnull=False).count()
    underground_fix_cars =  models.Car.objects\
        .filter(card_type= models.Car.CT_UNDERGROUND_LONGTERM).count()
    unground_month_cars = models.Car.objects\
        .filter(card_type=models.Car.CT_UNDERGROUND_MONTH).count()
    ground_month_cars = models.Car.objects\
        .filter(card_type=models.Car.CT_GROUND_MONTH).count()
    ground_temp_cars = models.Car.objects\
        .filter(card_type=models.Car.CT_GROUND_TEMP).count()

    ground_queue_cars = models.GroundQueue.objects\
        .filter(process_status=models.QS_WAITING).count()
    underground_queue_cars = models.UndergroundQueue.objects\
        .filter(process_status=models.QS_WAITING).count()

    total_fee = models.Fee.objects.all().aggregate(total_fee=Sum("total_fee"))['total_fee']
    total_room =  models.Fee.objects.all().distinct().count()
    gte_3month = models.Fee.objects.filter(total_fee_months__gte=3)\
        .values("room_id").distinct().count()
    lt_3month =  models.Fee.objects.filter(total_fee_months__lt=3)\
        .values("room_id").distinct().count()   

    return render(request, "overview.html", {
        'total_cars':total_cars,
        'approved_cars':approved_cars,
        'underground_fix_cars':underground_fix_cars,
        'unground_month_cars':unground_month_cars,
        'ground_month_cars':ground_month_cars,
        'ground_temp_cars':ground_temp_cars,
        'ground_queue_cars':ground_queue_cars,
        'underground_queue_cars':underground_queue_cars,
        'total_fee':total_fee,
        'total_room':total_room,
        'gte_3month':gte_3month,
        'lt_3month':lt_3month,
     })

