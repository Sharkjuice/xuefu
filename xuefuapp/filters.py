import django_filters
from . import models

class CarFilter(django_filters.FilterSet):
    # 原始查询 + lookup_exprr查询表达式
    room_id = django_filters.CharFilter(field_name='room_id', lookup_expr='iexact')
    car_id = django_filters.CharFilter(field_name='car_id', lookup_expr='iexact')
    applicant_name = django_filters.CharFilter(field_name='applicant_name', lookup_expr='iexact')
    card_type = django_filters.ChoiceFilter(choices=models.Car.CARD_TYPE,field_name='card_type', lookup_expr='iexact')
    approve_status = django_filters.ChoiceFilter(choices=models.STATUS_TYPE,field_name='approve_status', lookup_expr='iexact')

    class Meta:
        model = models.Car
        fields = ['room_id','car_id','applicant_name','card_type','approve_status']

class QueueFilter(django_filters.FilterSet):
    # 原始查询 + lookup_exprr查询表达式
    car = django_filters.CharFilter(field_name='car__car_id', lookup_expr='iexact')
    apply_id = django_filters.NumberFilter(field_name='apply_id', lookup_expr='iexact')
    process_status = django_filters.ChoiceFilter(choices=models.PROCESS_STATUS, field_name='process_status',
        lookup_expr='iexact')

    class Meta:
        model = models.GroundQueue
        fields = ['car','apply_id','process_status']

# class UndergroundQueueFilter(django_filters.FilterSet):
#     # 原始查询 + lookup_exprr查询表达式
#     car = django_filters.CharFilter(field_name='car__car_id', lookup_expr='iexact')
#     apply_id = django_filters.NumberFilter(field_name='apply_id', lookup_expr='iexact')
#     process_status = django_filters.ChoiceFilter(choices=models.PROCESS_STATUS, field_name='process_status',
#         lookup_expr='iexact')

#     class Meta:
#         model = models.UndergroundQueue
#         fields = ['car','apply_id','process_status']


class FeeFilter(django_filters.FilterSet):
    # 原始查询 + lookup_exprr查询表达式
    total_fee_months_min = django_filters.NumberFilter(label='欠费月数大于(含)', 
        field_name = 'total_fee_months', lookup_expr='gte')
    total_fee_months_max = django_filters.NumberFilter(label='欠费月数小于', 
        field_name='total_fee_months',lookup_expr='lt')
    total_fee_min = django_filters.NumberFilter(label='欠费金额大于(含)', 
        field_name='total_fee', lookup_expr='gte')
    total_fee_max = django_filters.NumberFilter(label='欠费金额小于', 
        field_name = 'total_fee',lookup_expr='lt')
    room_id = django_filters.CharFilter(label='房间号码(包含)', 
        field_name = 'room_id', lookup_expr='icontains')
    
    class Meta:
        model = models.Fee
        fields = ['total_fee_months_min','total_fee_months_max','total_fee_min','total_fee_max','room_id']
        #     'total_fee_months': ['gte','lt'],,
        #     'total_fee': ['gte','lt']
        #     }
    