from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.home', name='mallvictoria'),
    url(r'^ayuda$', 'principal.views.ayuda'),
    url(r'^categorias/$', 'principal.views.lista_categorias'),
    url(r'^articulos/$', 'principal.views.lista_articulos'),
    url(r'^articulos_busqueda/$', 'principal.views.paginar_articulos'),
    url(r'^categoria$', 'principal.views.lista_articulos_categoria'),
    url(r'^articulos_categoria_busqueda/$', 'principal.views.paginar_articulos_categoria'),
    url(r'^detalle$', 'principal.views.articulo_detalle'),
    url(r'^busquedas$', 'principal.views.busqueda_articulos'),
    url(r'^login$', 'principal.views.login'),
    #urls admin
    url(r'^administracion/$', 'principal.views.administracion'),
    url(r'^administracion/locker$', 'principal.views.locker'),
    url(r'^locker$', 'principal.views.frmarticulos'),
    url(r'^editlocker$', 'principal.views.frmarticulosedit'),
    url(r'^perfil$', 'principal.views.frmusuarioedit'),
    url(r'^articulo_locker$', 'principal.views.busca_articulos_usuario'),
    url(r'^termina_publicacion$', 'principal.views.termina_publicacion'),
    url(r'^ciudades$', 'principal.views.ciudades'),
    
    # url(r'^mallvictoria/', include('mallvictoria.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
     	{'document_root':settings.MEDIA_ROOT,}
     	),    
)
