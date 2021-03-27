from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView



# Create your views here.
from .models import Tour, Zona, User, Salida, Boleto

from .serializers import UserSerializer, ZonaSerializer, TourSerializer, SalidaSerializer



@login_required()
def index(request):
    es_editor = request.user.groups.filter(name="editores").exists()
    tours = Tour.objects.all()
    zonas = Zona.objects.all()


    return render(request, "tours/index.html",
    {"tours":tours, "zonas":zonas, "es_editor":es_editor})


#def login_user(request):
#    """ Atiende las peticiones de GET /login/ """
#
#    usuario_valido= ("rotz", "12345678")
#
#    # Si hay datos vía POST se procesan
#    if request.method == "POST":
#        # Se obtienen los datos del formulario
#        next = request.GET.get("next", "/")
#        user = authenticate(
#            username = request.POST["username"],
#            password = request.POST["password"])
#        if user is not None:
#            # Se agregan datos al request para mantener activa la sesión
#            login(request, user)
#            # Y redireccionamos a next
#            return redirect(next)
#        else:
#            # Usuario malo
#            msg = "Datos incorrectos, intente de nuevo!"
#    else:
#        # Si no hay datos POST
#        msg = "Request invalido"
#
#    return render(request, "registration/login.html")

#def logout_user(request):
#    """ Atiende las peticiones de GET /logout/ """
#    # Se cierra la sesión del usuario actual
#    logout(request)
#
#    return redirect("/login/")

@login_required()
def eliminar_tour(request, idTour):
    """
    Atiende la petición GET
       /tour/eliminar/<int:idTour>/
    """
    # Se obtienen los objetos correspondientes a los id's
    tour = Tour.objects.get(pk=idTour)

    # Se elimina el tour
    tour.delete()

    return redirect("/")

#nombre definido en urls
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all().order_by('id')
    serializer_class = ZonaSerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all().order_by('id')
    serializer_class = TourSerializer

class SalidaViewSet(viewsets.ModelViewSet):
    queryset = Salida.objects.all().order_by('id')
    serializer_class = SalidaSerializer


PAYMENT_METHOD_OXXO = "oxxo"

STATUS_PENDING = "pending"

STATUS_APPROVED = "approved"

class BuyTicketRequestSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    metodo_pago = serializers.ChoiceField(choices=['oxxo', 'debit_card', 'credit_card'])
    salida_id = serializers.IntegerField()

class BuyTicket(APIView):    
    def post(self, request):
        request_serializer = BuyTicketRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        #if request.data["metodo_pago"] == "oxxo":
         #   ticket_status = "pending"
        #else:
        #    ticket_status = "approved"
        ticket_status = self._get_ticket_status(request_serializer)

        #ticket = Boleto(metodo_pago=request.data["metodo_pago"], usuario_id=request.data["usuario_id"], salida_id=request.data["salida_id"], status=ticket_status)
        ticket = self._create_ticket(request_serializer, ticket_status)

        #ticket.save()
        return Response({'id':ticket.id, 'status':ticket.status}, status=status.HTTP_201_CREATED)

    def _get_ticket_status(self, request):
        if request.data["metodo_pago"] == PAYMENT_METHOD_OXXO:
            return STATUS_PENDING
        return STATUS_APPROVED

    def _create_ticket(self, request, ticket_status):
        ticket = Boleto(metodo_pago=request.data["metodo_pago"], usuario_id=request.data["usuario_id"], salida_id=request.data["salida_id"], status=ticket_status)
        ticket.save()
        return ticket

class BuyTicketUseCase():
    def __init__(self, boleto_repository_contract):