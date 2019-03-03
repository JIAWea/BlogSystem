from django import forms
from django.forms import fields
from django.forms import widgets
from repository import models

class articleForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(articleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['blog_id']
        self.fields['category_id'].choices = models.Category.objects.filter(bid_id=blog_id).values_list('id','caption')
        self.fields['tags'].choices = models.Tag.objects.filter(bid_id=2).values_list('id','caption')

    title = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'文章标题'})
    )
    summary = fields.CharField(
        widget=widgets.Textarea(attrs={'class':'form-control','placeholder':'文章简介','rows':'3'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'kind-content','id':'editor_id'})
    )
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Article.type_choices)
    )
    category_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect()
    )
    tags = fields.MultipleChoiceField(
        choices=[],
        widget=widgets.CheckboxSelectMultiple
    )


