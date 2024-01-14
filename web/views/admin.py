from django.shortcuts import render, redirect
from django.http import JsonResponse
from web import models
from django import forms
from utils.encrypt import md5
def admin_list(request):
    queryset = models.Admin.objects.all().order_by('-id')
    return render(request, 'admin_list.html',{"queryset": queryset})


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs=({'class': 'form-control'})

def add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, "admin_form.html",{"form":form})
    form = AdminModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, "admin_form.html",{"form":form})
    form.instance.password = md5(form.instance.password)
    form.save()
    return redirect("/admin/list/")


def admin_edit(request, aid):
    admin_object = models.Admin.objects.filter(id=aid).first()
    if request.method == 'GET':
        form = AdminModelForm(instance=admin_object)
        return render(request, "admin_form.html", {"form": form})
    form = AdminModelForm(instance=admin_object, data=request.POST)
    if not form.is_valid():
        return render(request, "admin_form.html", {"form": form})
    form.save()
    return redirect("/admin/list/")


def admin_delete(request):
    aid = request.GET.get("aid")
    models.Admin.objects.filter(id=aid).delete()
    return JsonResponse({"status": True})

