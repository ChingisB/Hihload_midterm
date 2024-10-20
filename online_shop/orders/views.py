from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Customer, Order, ShippingAddress
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer, ShippingAddressSerializer


class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Customer.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("Customer profile already exists for this user.")
        serializer.save(user=self.request.user)


class CustomerDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()


class OrderInfoView(generics.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id=None):
        if order_id:
            try:
                order = Order.objects.get(id=order_id, customer__user=request.user)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.filter(customer__user=request.user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save(customer=request.user.customer)

            total_amount = sum(item.get_total_price() for item in order.items.all())
            order.total_amount = total_amount
            order.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer__user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order_serializer = OrderSerializer(order, data=request.data, partial=True)
        if order_serializer.is_valid():
            updated_order = order_serializer.save()

            total_amount = sum(item.get_total_price() for item in updated_order.items.all())
            updated_order.total_amount = total_amount
            updated_order.save()

            return Response(OrderSerializer(updated_order).data, status=status.HTTP_200_OK)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer__user=request.user)
            order.delete()
            return Response({"detail": "Order deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ShippingAddressCreateView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        return serializer.create(user=self.request.user)

class ShippingAddressDetailView(generics.RetrieveUpdateAPIView):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).first
