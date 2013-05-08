# Create your views here.
from principal.models import Categoria, Usuario, Articulo, Tipo
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render_to_response, get_object_or_404

NUM_ELEMENTOS_POR_PAGINA=3

def home(request):
	return render_to_response('home.html',context_instance=RequestContext(request))

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
	articulos=Articulo.objects.all()
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
		articulos=Articulo.objects.filter(titulo__icontains=palabra)
		paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
		contacts = paginator.page(1)
		return render_to_response('busquedas.html',{'lista':contacts,'palabra':palabra},context_instance=RequestContext(request))
	except Exception as e:
		return redirect('/')

def paginar_articulos(request):
	palabra=request.POST['palabra']
	articulos=Articulo.objects.filter(titulo__icontains=palabra)
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	page=request.POST['pagina']
	if int(page)<=paginator.num_pages:
		contacts = paginator.page(page)
		return render_to_response('articulos_busqueda.html',{'lista':contacts},context_instance=RequestContext(request))
	else:
		return HttpResponse('')

def lista_articulos_categoria(request):
	idcategoria=request.GET['idcategoria']
	articulos=Articulo.objects.filter(categoria__id=idcategoria)
	paginator = Paginator(articulos, NUM_ELEMENTOS_POR_PAGINA)
	contacts = paginator.page(1)
	return render_to_response('categoria.html',{'lista':contacts,'idcategoria':idcategoria},context_instance=RequestContext(request))

def paginar_articulos_categoria(request):
	idcategoria=request.POST['idcategoria']
	articulos=Articulo.objects.filter(categoria__id=idcategoria)
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
	articulos_relacionados=Articulo.objects.filter(categoria__id=articulo.categoria.id).order_by('?')[:4]
	return render_to_response('detalle.html',{'articulo':articulo,'articulos_relacionados':articulos_relacionados},context_instance=RequestContext(request))

def administracion(request):
	return render_to_response('administracion/principal.html',{'range':range(3)},context_instance=RequestContext(request))

def locker(request):
	categorias=Categoria.objects.all()
	tipos=Tipo.objects.all()
	idlocker=request.GET['id']
	return render_to_response('administracion/locker.html',{'idlocker':idlocker,'tipos':tipos,'categorias':categorias},context_instance=RequestContext(request))
	#return HttpResponse(page+'<script>$("#num_pagina").val("'+page+'");</script>');
	#try:
	#	contacts = paginator.page(page)
	#except PageNotAnInteger:
	#	contacts = paginator.page(1)
	#except EmptyPage:
	#	contacts = paginator.page(paginator.num_pages)	
	#return render_to_response('articulos.html',{'lista':contacts},context_instance=RequestContext(request))
