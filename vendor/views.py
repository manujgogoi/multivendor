from django.shortcuts import render

# Create your views here.
def home(request, *args, **kwargs):
    context = {"name": "Manuj Gogoi", "address": "Likson Gaon, Kakotibari, Charaideo, Assam"}
    return render(request, "vendor/index.html", context)