# -*- coding: utf-8 -*-
from django.forms import ModelForm,ValidationError
from app.models import Moment,Diagonos

class MomentForm(ModelForm):
   class Meta:
      model = Moment
      fields = '__all__'

   def clean(self):
      cleaned_data=super(MomentForm,self).clean()
      fault_describe=cleaned_data.get("fault_describe")
      if fault_describe is None:
         raise ValidationError("请输入fault_describe内容!")
      elif fault_describe.find("ABCD")>=0:
         raise ValidationError("不能输入敏感字ABCD!")
      return cleaned_data

class DiagonosForm(ModelForm):
   class Meta:
      model = Diagonos
      fields = '__all__'   

   def clean(self):
      cleaned_data=super(DiagonosForm,self).clean()
      dgs_codeA=cleaned_data.get("dgs_codeA")
      if dgs_codeA is None:
         raise ValidationError("请输入dgs_codeA内容!")
      elif dgs_codeA.find("ABCD")>=0:
         raise ValidationError("不能输入敏感字ABCD!")
      return cleaned_data

