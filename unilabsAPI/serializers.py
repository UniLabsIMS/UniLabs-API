from rest_framework import viewsets

class MultiSerializerAPIView(viewsets.ModelViewSet):
    
    read_serializer = None
    write_serializer = None

    def get_serializer_class(self):
        
        if self.serializer_class is not None:
            return self.serializer_class
        method = self.request.method
        if method == 'GET':
            return self.read_serializer
        else:
            return self.write_serializer