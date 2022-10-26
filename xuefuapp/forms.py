from dataclasses import Field
import pdb
from tabnanny import verbose
from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Column,Row

from . import models
 
class CarForm(forms.ModelForm):
    ground_queue_info =  forms.CharField(label="地面排队情况",required=False)
    underground_queue_info = forms.CharField(label='地库排队情况_1', required=False)
    underground_queue_info_2 = forms.CharField(label='地库排队情况_2', required=False)

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].disabled = True

    class Meta:
        model = models.Car
        fields = ['ground_queue_info','underground_queue_info', 'underground_queue_info_2']
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        
        readonly_fields = fields

class GroundQueueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroundQueueForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].disabled = True

    class Meta:
        model = models.GroundQueue
        fields = []
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        readonly_fields = fields

class UndergroundQueueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UndergroundQueueForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].disabled = True

    class Meta:
        model = models.UndergroundQueue
        fields = []
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        readonly_fields = fields

class UndergroundQueueForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UndergroundQueueForm2, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].disabled = True

    class Meta:
        model = models.UndergroundQueue2
        fields = []
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        readonly_fields = fields

class OwnerForm(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = []
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        readonly_fields = fields


class FeeForm(forms.ModelForm):
    class Meta:
        model = models.Fee
        fields = []
        for f in model._meta.get_fields():
            if f.name not in ['create_at', 'change_at']:
                fields.append(f.name)
        readonly_fields = fields


    def __init__(self, *args, **kwargs):
        super(FeeForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('room_id'), Column('notes'),Submit('return', '返回列表', css_class='btn btn-info'),css_class="justify-content-between"),
            Row(Column('total_fee'), Column('total_fee_range'), Column('total_fee_months'), css_class="justify-content-between"),
            Row(Column('prop_fee'), Column('prop_fee_range'), Column('prop_fee_months'), css_class="justify-content-between"),
            Row(Column('water_fee'), Column('water_fee_range'), Column('water_fee_months'), css_class="justify-content-between"),
            Row(Column('sewage_fee'), Column('sewage_fee_range'), Column('sewage_fee_months'), css_class="justify-content-between"),
            Row(Column('garbage_fee'), Column('garbage_fee_range'), Column('garbage_fee_months'), css_class="justify-content-between"),
            Row(Column('base_fee'), Column('base_fee_range'), Column('base_fee_months'), css_class="justify-content-between"),
            Row(Column('power_fee'), Column('power_fee_range'), Column('power_fee_months'), css_class="justify-content-between"),
            Row(Column('busi_fee'), Column('busi_fee_range'), Column('busi_fee_months'), css_class="justify-content-between"),
        )

class PortForm(forms.Form):
    select_fee_file = forms.FileField(label="选择物业水电欠费文件", required=False)
    select_car_file = forms.FileField(label="选择车辆表格文件",required=False)
    select_ground_queue_file = forms.FileField(label="选择地面排队文件",required=False)
    select_underground_queue_file = forms.FileField(label="选择地库排队文件",required=False)
    
    def __init__(self, *args, **kwargs):
        super(PortForm,self).__init__(*args, **kwargs)
        # Your code
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-5'
        self.helper.field_class = 'col-md-7'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('select_fee_file'), 
                Submit('upload_fee_file', '上传物业文件'), 
                css_class='align-items-start'),
            # Row(Column('select_car_file'), 
            #     Submit('upload_car_file', '上传车辆文件', css_class='btn-danger'), 
            #     css_class='align-items-start mt-3'),
            
            # Row(Column('select_ground_queue_file'), 
            #     Submit('upload_ground_queue_file', '上传地面排队文件',css_class='btn-danger'), 
            #     css_class='align-items-start mt-3'), 

            # Row(Column('select_underground_queue_file'), 
            #     Submit('upload_underground_queue_file', '上传地库排队文件', css_class='btn-danger'), 
            #     css_class='align-items-start mt-3'), 

            Row(Submit('download_fee_file', '下载物业文件(还没有实现)', css_class='btn-info'), 
                Submit('download_car_file', '下载车辆文件(还没有实现）', css_class='btn-info ml-3'),
                css_class='justify-content-end mt-3'),
            )
        


 


 