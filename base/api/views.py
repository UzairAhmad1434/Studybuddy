from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Room
from .serializers import RoomSerializer  # Import the correct serializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)  # Use RoomSerializer
    return Response(serializer.data)
