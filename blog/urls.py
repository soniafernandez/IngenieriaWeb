from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
        url(r'^$', views.inicio,  name='inicio' ),
		url(r'^listado_recetas/$', views.listado_recetas,  name='listado_recetas'),
		url(r'^receta/(?P<pk>\d+)/$', views.receta_detalle, name='receta_detalle'),
		url(r'^receta/nueva/$', views.nueva_receta, name='nueva_receta'),
		url(r'^receta/(?P<pk>\d+)/editar/$', views.editar_receta, name='editar_receta'),
		url(r'^registro/$', views.registrar_usuario, name='registro'),
		url(r'^iniciarsesion/$', views.inicio_sesion, name='inicio_sesion'),
		url(r'^cerrarsesion/$', views.cerrar_sesion, name='cerrar_sesion'),
	    url(r'^buscar_basedatos/$',views.lista_recetas),
	    url(r'^busqueda/$', views.busqueda),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)