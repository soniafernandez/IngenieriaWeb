from django.shortcuts import render, get_object_or_404, redirect
from .models import Receta, Ingredientes
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


from django.contrib.auth.forms import AuthenticationForm
from .forms import RecetaForm, RegistroForm
from django.forms import inlineformset_factory, TextInput

import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

# Create your views here.

def inicio(request):
    nueva_receta = Receta.objects.latest('fecha_publicacion')
    receta1 = Receta.objects.get(pk=3);
    receta2 = Receta.objects.get(pk=4);
    receta3 = Receta.objects.get(pk=5);
    return render (request, 'blog/inicio.html', {'nueva_receta': nueva_receta, 'receta1': receta1, 'receta2': receta2, 'receta3': receta3})

def listado_recetas(request):
    lista_recetas = Receta.objects.filter(fecha_publicacion__lte= timezone.now())
    return render(request, 'blog/listado_recetas.html', {'lista_recetas': lista_recetas}, )

def receta_detalle(request, pk):
    receta = get_object_or_404 (Receta, pk=pk)
    return render(request, 'blog/receta_detalle.html', {'receta': receta})


def nueva_receta(request, receta_id=None):
    if receta_id:
        receta = Receta.objects.get(pk=receta_id)
    else:
        receta = Receta()

    IngredientesFormSet = inlineformset_factory(Receta,Ingredientes, form = RecetaForm, extra=1, widgets ={'cantidad': TextInput(),}, can_delete=True)
    

    if request.method == "POST":
        form = RecetaForm(request.POST,request.FILES, instance=receta)
        formset = IngredientesFormSet(request.POST, instance=receta, prefix = 'ingrediente')

        if form.is_valid() and formset.is_valid():

            receta = form.save(commit=False)
            receta.autor = request.user
            receta.fecha_publicacion = timezone.now() 
            receta.save()
            formset.save()
            return redirect('receta_detalle', pk=receta.pk)
    else:
        form = RecetaForm()
        formset = IngredientesFormSet(prefix='ingrediente')
    return render(request, 'blog/editar_receta.html', {'formulario': form, 'formset':formset})

def editar_receta(request, pk):
    receta = get_object_or_404 (Receta, pk=pk)
    IngredientesFormSet = inlineformset_factory(Receta,Ingredientes, form = RecetaForm, extra=0, widgets ={'cantidad': TextInput(),})
    ingredientes_list = Ingredientes.objects.filter(receta = receta)

    if request.method == "POST":

        form = RecetaForm(request.POST, request.FILES, instance=receta)
        formset = IngredientesFormSet(request.POST,instance=receta, prefix='ingrediente')

        if form.is_valid() and formset.is_valid():
               
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.save()   
            formset.save()

            return redirect('receta_detalle', pk=receta.pk)
    else:
        form = RecetaForm(instance= receta)
        formset = IngredientesFormSet(instance=receta, prefix='ingrediente')
        
    return render (request, 'blog/editar_receta.html', {'formulario': form, 'formset':formset})

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render (request, 'blog/registro.html', {'formulario': form})

def inicio_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    user= request.user
                    return redirect('inicio' )
                else:
                    return render(request, 'blog/no_activo.html')
            else:
                return render(request, 'blog/no_usuario.html')
    else:
        formulario = AuthenticationForm()
    return render(request, 'blog/inicio_sesion.html', {'formulario': formulario})

@login_required(login_url='/inicio_sesion')
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


def lista_recetas(request):
    if request.is_ajax:
        search=request.GET.get('start','')

        recetas=Receta.objects.filter(nombre__icontains=search)
        
        results=[]
        for receta in recetas:
            receta_json={}
            receta_json['id']=receta.id
            receta_json['nombre']=receta.nombre
            results.append(receta_json)

        data_json=json.dumps(results)

    else:
        data_json='fail'
    mimetype="application/json"
    return HttpResponse(data_json,mimetype)

def busqueda(request):

    query = request.GET.get('receta');
    result = Receta.objects.get(nombre=query)

    return redirect('receta_detalle', result.pk)


