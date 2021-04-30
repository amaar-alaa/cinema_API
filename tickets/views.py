from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Movie, Guest, Reservation
from rest_framework.decorators import api_view
from .serializers import ReservationSerializers, MovieSerializers, GuestSerializers
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
#for authentvtions
from rest_framework.authentication import BasicAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# 1 without model and rest
def no_rest_no_model(request):

    guests = [
        {
            'id': 1,
            'name': 'ali',
                    'mobile': 88890
        },
        {
            'id': 2,
            'name': 'hanza',
                    'mobile': 88890
        }
    ]
    return JsonResponse(guests, safe=False)


# 2 without rest usiog just model
def no_rest_from_model(request):

    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)


# crate == POST
# list == GET
# pk query == GET تستخدم لعرض التفاصيل يعني طلب عنصر واحد
# Update == PUT
# Delete == DELETE

# 3 FBV functions based view

# 3.1 POST GET
@api_view(["POST", "GET"])
def FBV_List(request):

    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 3.2 GET PUT DELETE
@api_view(["PUT", "GET", "DELETE"])
def FBV_pk(request, pk):

    # check of pk
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':

        serializer = GuestSerializers(guest)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializers(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 4 CBV class based view
# 4.1 List and create == GET & POST
class CBV_List(APIView):

    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializers(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)


# 4.2 update & delete & show ==PUT & DELETE &GET
class CBV_pk(APIView):

    def get_object(self, pk):

        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializers(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 5 Mixins
# 5.1 Mixins List
class mixins_List(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 mixins PUT GET DELETE
# RetrieveModelMixin for one row not list
class mixins_pk(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


# 6 Generics
# 6.1 Generics List and create
class Generics_List(generics.ListCreateAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]

# 6.1 Generics update and delete and show
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
    authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]


# 7 viewsets
class Viewsets_guests(viewsets.ModelViewSet):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializers


class Viewsets_movies(viewsets.ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']


class Viewsets_reservations(viewsets.ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializers


# 8 find movie
@api_view(["GET"])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.date['movie']
    )
    serializer = MovieSerializers(movies, many=True)
    return Response(serializer.data)


#create new reservations 
@api_view(["GET"])
def new_reservations(request):
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.date['movie']
    )
    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()
    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)
   
