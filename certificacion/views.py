from django.shortcuts import render

def crear_orden(request):
    return render(request, 'crear_orden.html')
