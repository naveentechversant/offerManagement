import datetime, re
from django.core.validators import validate_email, RegexValidator
from django.db.models.query_utils import Q
from django.forms import *
from django.forms.models import *
from django.forms.fields import *
from django.forms.widgets import *
from django.db.models import Q
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from datetime import date
import datetime
from django.forms.widgets import Input
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
import copy
from models import *
from bootstrap3_datetime.widgets import DateTimePicker

'''
This is used to create offer.
'''

DISCOUNT_TYPE = (
    ('','---'),
    ('Percentage', 'Percentage'),
    ('Absolute Amount', 'Absolute Amount'),
    )

class OfferForm(ModelForm):
    code = CharField(widget=TextInput(attrs={'style':"width:100%;"}), max_length=100)
    discount = DecimalField(min_value=0.01, max_digits=10, decimal_places=2, widget = TextInput(attrs={'style':"text-align:right;"}))
    type_of_discount = ChoiceField(choices =(tuple(sorted(DISCOUNT_TYPE, key=lambda item: item[1]))), label='Type of discount')
    
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        for field_name in ('type_of_discount','code','discount'):
            self.fields[field_name].widget.attrs.update({'class' : 'form-control'})
        
        
    def clean_code(self,):
        code = self.cleaned_data.get('code','')
        return code.strip()

    def clean(self):
        data = self.cleaned_data
        code = data.get('code',None)
        type_of_discount = data.get('type_of_discount',None)
        discount = data.get('discount',0.0)
        if type_of_discount == 'Percentage' and not (0 <= discount <= 100):
            self._errors['discount']=self.error_class(["Invalid Percentage"])
        if not Product.objects.filter(code=code).count():
            self._errors['code']=self.error_class(["Invalid Product Code."])

        start = data.get('start')
        end = data.get('end')
        if start and end and  end < start:
            self._errors['end']=self.error_class(["End datetime must be greater than start date"])
        offer_obj = Offers.objects.filter(code=code)
        if self.instance.pk:
            offer_obj = offer_obj.exclude(pk=self.instance.pk)
        bln_lies = False
        # Can also check with filteration using range  or lte or gte(Ideal method)
        for obj in offer_obj:
            if obj.start <= start <= obj.end:
                bln_lies = True
                break
            if obj.start <= end <= obj.end:
                bln_lies = True
                break
        if bln_lies:
            self._errors['code']=self.error_class(["Already product with this code defined under this period.Please edit that."])
        return data
        
    class Meta:
            model = Offers
            fields = ('code', 'start','end', 'discount','type_of_discount')
            widgets = {
            'start': DateTimeWidget(usel10n = True,
                                         bootstrap_version=3,options={'startDate':datetime.date.today().strftime('%Y-%m-%d')}),
            'end': DateTimeWidget(usel10n = True,
                                         bootstrap_version=3,options={'startDate':datetime.date.today().strftime('%Y-%m-%d')})
            }

class CheckProductPrice(Form):
    date = DateTimeField(required=True,widget=DateTimeWidget(usel10n = True,
                                         bootstrap_version=3,options={'startDate':datetime.date.today().strftime('%Y-%m-%d')}))
    code = CharField(required=True,widget=TextInput(attrs={'style':"width:100%;"}), max_length=100)
    

    def clean_code(self,):
        code = self.cleaned_data.get('code','').strip()
        if not Product.objects.filter(code=code).count():
            self._errors['code']=self.error_class(["Invalid Product Code."])
        return code


