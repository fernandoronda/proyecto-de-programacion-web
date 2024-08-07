from django.shortcuts import render
from .models import Tour,Genero, Usuario
from .forms import GeneroForm,UsuarioForm,TourForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def catalogo(request):
    tours = Tour.objects.all()
    context ={
        'tours': tours,
    }
    return render(request, 'pages/catalogo.html', context)

def index(request):
    context={}
    return render(request,"pages/index.html",context)


def iniciousuario(request):
    context={}
    return render(request,"pages/iniciousuario.html",context)



def registro(request):

    context={}
    return render(request,"pages/registro.html",context)

@login_required
def crud(request):
    usuarios = Usuario.objects.all()
    context = {
        "usuarios": usuarios,
    }
    return render(request, "pages/crud.html", context)

@login_required
def user_add(request):
    if request.method != "POST":
        generos = Genero.objects.all()
        context = {
            "generos": generos,
        }
        return render(request, "pages/user_add.html", context)
    else:
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        appPaterno = request.POST["appPaterno"]
        appMaterno = request.POST["appMaterno"]
        fechaNac = request.POST["fecha"]
        genero = request.POST["genero"]
        telefono = request.POST["telefono"]
        correo = request.POST["correo"]
        direccion = request.POST["direccion"]
        password = request.POST["password"]

        objGenero = Genero.objects.get(id_genero=genero)

        obj = Usuario.objects.create(
            rut=rut,
            nombre=nombre,
            apellido_paterno=appPaterno,
            apellido_materno=appMaterno,
            fecha_nacimiento=fechaNac,
            id_genero=objGenero,
            telefono=telefono,
            email=correo,
            direccion=direccion,
            password=password,
        )
        obj.save()
        context = {
            "mensaje": "Registro Exitoso",
        }
        return render(request, "pages/user_add.html", context)

@login_required
def user_del(request, pk):
    try:
        usuario = Usuario.objects.get(rut=pk)
        usuario.delete()

        usuarios = Usuario.objects.all()
        context = {
            "mensaje": "Registro Eliminado",
            "usuarios": usuarios,
        }
        return render(request, "pages/crud.html", context)
    except:
        usuarios = Usuario.objects.all()
        context = {
            "mensaje": "Error,Rut no encontrado...",
            "usuarios": usuarios,
        }
        return render(request, "pages/crud.html", context)

@login_required
def user_findEdit(request,pk):
    if pk!="":
        """ 
            objects.get() = Obtener datos con filtro
            objects.all() = Obtener todos
        """
        usuario = Usuario.objects.get(rut=pk)
        generos = Genero.objects.all()

        context={
            "usuario":usuario,
            "generos":generos,
        }
        return render(request,"pages/user_update.html",context)
    else:
        usuarios = Usuario.objects.all()
        context={
            "mensaje":"Error,Rut no encontrado",
            "usuarios":usuarios
        }
        return render(request,"pages/crud.html",context)

@login_required
def user_update(request):
    if request.method=="POST":
        """ 
            Capturo todos los datos del front
            Identificamos
            Asignamos nombre 
        """
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        appPaterno = request.POST["appPaterno"]
        appMaterno = request.POST["appMaterno"]
        fechaNac = request.POST["fecha"]
        genero = request.POST["genero"]
        telefono = request.POST["telefono"]
        correo = request.POST["correo"]
        password = request.POST["password"]
        direccion = request.POST["direccion"]
        activo = True

        """ Obtengo genero desde la BDD para modificar """
        objGenero = Genero.objects.get(id_genero=genero)

        """ Genero la instancia """

        obj = Usuario(
            rut=rut,
            nombre=nombre,
            apellido_paterno=appPaterno,
            apellido_materno=appMaterno,
            fecha_nacimiento=fechaNac,
            id_genero=objGenero,
            telefono=telefono,
            email=correo,
            password=password,
            direccion=direccion,
            activo=activo,
        )
        obj.save()

        generos = Genero.objects.all()
        context = {
            "mensaje": "Modificado con Exito",
            "generos":generos,
            "usuario":obj,
        }
        return render(request, "pages/user_update.html", context)
    

@login_required
def crud_genero(request):
    generos = Genero.objects.all()

    context={
        "generos":generos,
    }
    return render(request,"pages/crud_genero.html",context)

@login_required
def genero_add(request):
    formGenero = GeneroForm()
    formUsuario = UsuarioForm()
    if request.method=="POST":
        nuevo = GeneroForm(request.POST)
        if nuevo.is_valid():
            nuevo.save()

            context={
                "mensaje":"Agregado con exito",
                "form":formGenero
            }
            return render(request,"pages/genero_add.html",context)
    else:
        context = {
            "form":formGenero,
            "form2":formUsuario
        }
        return render(request,"pages/genero_add.html",context)
    
@login_required
def genero_del(request,pk):
    try:
        genero = Genero.objects.get(id_genero=pk)
        genero.delete()

        generos = Genero.objects.all()
        context={
            "mensaje":"Registro eliminado exitosamente",
            "generos":generos
        }
        return render(request,"pages/crud_genero.html",context)
    except:
        generos = Genero.objects.all()
        context={
            "mensaje":"Error, Genero no encontrado...",
            "generos":generos
        }
        return render(request,"pages/crud_genero.html",context)
    
@login_required
def genero_edit(request,pk):
    if pk!="":
        genero = Genero.objects.get(id_genero=pk)
        form = GeneroForm(instance=genero)
        if request.method=="POST":
            nuevo = GeneroForm(request.POST,instance=genero)

            if nuevo.is_valid():
                nuevo.save()

                context ={
                    "mensaje":"Modificado con exito",
                    "form":nuevo
                }
                return render(request,"pages/genero_edit.html",context)
        else:
            context={
                "form":form,
            }
            return render(request,"pages/genero_edit.html",context)
    else:
        generos = Genero.objects.all()
        context={
            "mensaje":"Error, genero no encontrado",
            "generos":generos
        }
        return render(request,"pages/crud_genero.html",context)


@login_required
def crud_tour(request):
    tours = Tour.objects.all()

    context={
        "tours":tours,
    }
    return render(request,"pages/crud_tour.html",context)

@login_required
def tour_add(request):
    formTour = TourForm()
    if request.method=="POST":
        nuevo = TourForm(request.POST)
        if nuevo.is_valid():
            nuevo.save()

            context={
                "mensaje":"Agregado con exito",
                "form":formTour
            }
            return render(request,"pages/tour_add.html",context)
    else:
        context = {
            "form":TourForm,
        }
        return render(request,"pages/tour_add.html",context)
    
@login_required
def tour_del(request,pk):
    try:
        tour = Tour.objects.get(id_tour=pk)
        tour.delete()

        tours = Tour.objects.all()
        context={
            "mensaje":"Registro eliminado exitosamente",
            "tours":tours
        }
        return render(request,"pages/crud_tour.html",context)
    except:
        tours = Tour.objects.all()
        context={
            "mensaje":"Error, Genero no encontrado...",
            "tours":tours
        }
        return render(request,"pages/crud_tour.html",context)
    
@login_required
def tour_edit(request,pk):
    if pk!="":
        tour = Tour.objects.get(id_tour=pk)
        form = TourForm(instance=tour)
        if request.method=="POST":
            nuevo = TourForm(request.POST,instance=tour)

            if nuevo.is_valid():
                nuevo.save()

                context ={
                    "mensaje":"Modificado con exito",
                    "form":nuevo
                }
                return render(request,"pages/tour_edit.html",context)
        else:
            context={
                "form":form,
            }
            return render(request,"pages/tour_edit.html",context)
    else:
        tours = Tour.objects.all()
        context={
            "mensaje":"Error, genero no encontrado",
            "tours":tours
        }
        return render(request,"pages/crud_tour.html",context)




def loginSession(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username=="juanka" and password=="juanka":
            request.session["user"] = username
            usuarios = Usuario.objects.all()
            context = {
                "usuarios":usuarios,
            }
            return render(request,"pages/crud.html",context)
        else:
            context = {
                "mensaje":"Usuario o contraseña incorrecta",
                "design":"alert alert-danger w-50 mx-auto text-center",
            }
            return render(request,"pages/login.html",context)
    else:
        context = {

        }
        return render(request,"pages/login.html",context)

def conectar(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            usuarios = Usuario.objects.all()
            context = {
                "usuarios":usuarios,
            }
            return render(request,"pages/crud.html",context)
        else:
            context = {
                "mensaje":"Usuario o contraseña incorrecta",
                "design":"alert alert-danger w-50 mx-auto text-center",
            }
            return render(request,"pages/login.html",context)
    else:
        context = {

        }
        return render(request,"pages/login.html",context)

def desconectar(request):   
    if request.user.is_authenticated:
        logout(request)
    
    context = {
        "mensaje":"Desconectado con exito",
        "design":"alert alert-success w-50 mx-auto text-center",
    }
    return render(request,"pages/login.html",context)
