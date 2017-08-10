from django import forms

class RecordForm(forms.Form):
    domain = forms.CharField(label='Domain', max_length=100)
    rr = forms.CharField(label='RR', max_length=100)
    type = forms.CharField(label='Type', max_length=100)
    record_value = forms.CharField(label='Record_value', max_length=100)
    ttl = forms.CharField(label='TTL', max_length=100)


