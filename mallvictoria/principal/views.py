# Create your views here.
from principal.models import Categoria, Usuario, Articulo, Tipo, ArticuloUsuario, Visita
from principal.forms import ArticuloForm, ArticuloFormEdit, UsuarioForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render_to_response, get_object_or_404
import datetime
from django.utils.timezone import utc

DIAS_PUBLICACION=15 
NUM_ELEMENTOS_POR_PAGINA=30
now_=datetime.date.today()
quincedias=datetime.timedelta(days=DIAS_PUBLICACION)+now_;

def home(request):
	return render_to_response('home.html',context_instance=RequestContext(request))

def ayuda(request):
	return render_to_response('administracion/ayuda.html',context_instance=RequestContext(request))

def lista_categorias(request):
	categorias=Categoria.objects.all()
	return render_to_response('base/categorias.html',{'lista':categorias})

def login(request): 
	try:
		u=Usuario.objects.get(correo=request.POST['m_correo'])
		if u.password == request.POST['m_password']:
			return HttpResponse('{"nombre":"'+u.nombre+'","id":"'+ str(u.id) +'","correo":"'+u.correo+'","password":"'+u.password+'"}')
		else:
			return HttpResponse('0');	
	except Usuario.DoesNotExist:
		return HttpResponse('0');

def lista_articulos(request):
	#articulos=Articulo.objects.filter(fecha_publicacion__range=(now_,quincedias)).order_by('-fecha_publicacion').exclude(status=False)
	#exclude(articulo__fecha_vencimiento__lte=now_)
	articulos=Articulo.objects.filter(fecha_vencimiento__gte=datetime.date.today()).order_by('-fecha_publicacion').exclude(status=False)
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	page=request.POST['pagina']
	if int(page)<=paginator.num_pages:
		contacts = paginator.page(page)
		return render_to_response('articulos.html',{'lista':contacts},context_instance=RequestContext(request))
	else:
		return HttpResponse('')

def busqueda_articulos(request):
	try:
		palabra=request.POST['texto_busqueda']
		if len(palabra)>3:
			articulos=Articulo.objects.exclude(status=False).filter(fecha_vencimiento__gte=datetime.date.today(),titulo__icontains=palabra).order_by('-fecha_publicacion')
			paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
			contacts = paginator.page(1)
			return render_to_response('busquedas.html',{'lista':contacts,'palabra':palabra},context_instance=RequestContext(request))
		else:
			msg='La palabra ('+palabra+') de busqueda es demaciado corta intente con una mayor a 3 caracteres.'
			return render_to_response('busquedas.html',{'palabra':palabra,'msg':msg},context_instance=RequestContext(request))
	except Exception as e:
		return redirect('/')

def paginar_articulos(request):
	palabra=request.POST['palabra']
	articulos=Articulo.objects.exclude(status=False).filter(fecha_vencimiento__gte=datetime.date.today(),titulo__icontains=palabra).order_by('-fecha_publicacion')
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	page=request.POST['pagina']
	if int(page)<=paginator.num_pages:
		contacts = paginator.page(page)
		return render_to_response('articulos_busqueda.html',{'lista':contacts},context_instance=RequestContext(request))
	else:
		return HttpResponse('')

def lista_articulos_categoria(request):
	idcategoria=request.GET['idcategoria']
	articulos=Articulo.objects.exclude(status=False).filter(fecha_vencimiento__gte=datetime.date.today(),categoria__id=idcategoria).order_by('-fecha_publicacion')
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	contacts = paginator.page(1)
	return render_to_response('categoria.html',{'lista':contacts,'idcategoria':idcategoria},context_instance=RequestContext(request))

def paginar_articulos_categoria(request):
	idcategoria=request.POST['idcategoria']
	articulos=Articulo.objects.exclude(status=False).filter(fecha_vencimiento__gte=datetime.date.today(),categoria__id=idcategoria).order_by('-fecha_publicacion')
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	page=request.POST['pagina']
	if int(page)<=paginator.num_pages:
		contacts = paginator.page(page)
		return render_to_response('articulos_categoria_busquedas.html',{'lista':contacts},context_instance=RequestContext(request))
	else:
		return HttpResponse('')

def articulo_detalle(request):
	idarticulo=request.GET['idarticulo']
	articulo=Articulo.objects.get(pk=idarticulo)
	Visita.objects.create(articulo=articulo,ip=request.META.get('REMOTE_ADDR'))
	tweet=articulo.titulo.replace(" ","%20")
	articulos_relacionados=Articulo.objects.exclude(status=False).filter(fecha_vencimiento__gte=datetime.date.today()).filter(categoria__id=articulo.categoria.id).order_by('?')[:4]
	return render_to_response('detalle.html',{'articulo':articulo,'tweet':tweet,'articulos_relacionados':articulos_relacionados},context_instance=RequestContext(request))

def administracion(request):
	return render_to_response('administracion/principal.html',context_instance=RequestContext(request))

def busca_articulos_usuario(request):
	idusuario=request.POST['idusuario']
	#articulos_usuario=ArticuloUsuario.objects.exclude(articulo__status=False).filter(usuario__id=idusuario).filter(articulo__fecha_publicacion__range=(now_,quincedias))
	articulos_usuario=ArticuloUsuario.objects.exclude(articulo__status=False).filter(articulo__fecha_vencimiento__gte=datetime.date.today(),usuario__id=idusuario)
	lista=range(3)
	for count in articulos_usuario:
		#fecha1=datetime.datetime(int(count.articulo.fecha_vencimiento.year),int(count.articulo.fecha_vencimiento.month),int(count.articulo.fecha_vencimiento.day),0,0,0)
		fecha2=datetime.datetime(int(count.articulo.fecha_publicacion.year),int(count.articulo.fecha_publicacion.month),int(count.articulo.fecha_publicacion.day),0,0,0)
		fecha1=datetime.timedelta(days=DIAS_PUBLICACION)+fecha2
		dias=fecha1-fecha2
		visitas=Visita.objects.filter(articulo=count.articulo).count()
		lista[count.orden]=[count,dias.days,visitas]
	return render_to_response('administracion/articulo_locker.html',{'lista':lista},context_instance=RequestContext(request))

def locker(request):
	categorias=Categoria.objects.all()
	tipos=Tipo.objects.all()
	idlocker=request.GET['id']
	return render_to_response('administracion/locker.html',{'idlocker':idlocker,'tipos':tipos,'categorias':categorias},context_instance=RequestContext(request))

def frmarticulos(request):
	idlocker=request.GET['id']
	if request.method == 'POST':
		formulario = ArticuloForm(request.POST, request.FILES)
		if formulario.is_valid():
			#f=formulario.save(commit=False)
			#f.fecha_publicacion=f.fecha_publicacion+15
			#f.save()
			f=formulario.save()
			f.fecha_publicacion=datetime.datetime.now()
			f.fecha_vencimiento=datetime.timedelta(days=DIAS_PUBLICACION)+datetime.datetime.now()
			f.save()
			u=Usuario.objects.get(pk=request.POST['usuario'])
			a=Articulo.objects.get(pk=f.id)
			idloc=eval(idlocker)-1
			ArticuloUsuario.objects.create(usuario=u,articulo=a,orden=idloc)
			return HttpResponseRedirect('/administracion/')
	else:
		formulario=ArticuloForm()	
	return render_to_response('administracion/locker.html',{'idlocker':idlocker,'formulario':formulario},context_instance=RequestContext(request))

def frmarticulosedit(request):
	idlocker=request.GET['id']
	idarticulo=request.GET['idarticulo']
	articulo=get_object_or_404(Articulo,pk=idarticulo)
	if request.POST:
		formulario=ArticuloFormEdit(request.POST,instance=articulo)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/administracion/')
	else:
		formulario=ArticuloFormEdit(instance=articulo)
	return render_to_response('administracion/editlocker.html',{'imagen':articulo.imagen.thumbnail.url,'idlocker':idlocker,'formulario':formulario},context_instance=RequestContext(request))

def frmusuarioedit(request):
	idusuario=request.GET['idusuario']
	usuario=get_object_or_404(Usuario,pk=idusuario)
	if request.POST:
		formulario=UsuarioForm(request.POST,instance=usuario)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario=UsuarioForm(instance=usuario)
	return render_to_response('administracion/perfil.html',{'formulario':formulario},context_instance=RequestContext(request))
	
def termina_publicacion(request):
	if request.method== 'POST':
		articulo=Articulo.objects.get(pk=request.POST['idarticulo'])
		articulo.status=0
		articulo.save()
	return HttpResponseRedirect('/')
