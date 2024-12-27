from django.shortcuts import render
from rest_framework.views import APIView
from . serializers import *
from.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class InventoryItemAPI(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self,request):
        foo = InventoryItem.objects.all().order_by('-id')
        serializer = InventoryItemSerializer(foo, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            obj=serializer.save()
            return Response({'msg':'Inventory Item Created Successfully','success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors,'success':False, "msg": "Something went wrong! Kindly recheck"}, status=status.HTTP_201_CREATED)
    
    def put(self,request):
        try:
            id = self.request.query_params.get('id')
            foo = InventoryItem.objects.get(id=id)
            serializer = InventoryItemSerializer(foo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Inventory Item Updated Successfully','success':True})
            return Response({'error':serializer.errors,'success':False, "msg": "Something went wrong! Kindly recheck"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e),'success':False, "msg": "Something went wrong! Kindly recheck"})

    def delete(self,request):
        try:
            id = self.request.query_params.get('id')
            foo = InventoryItem.objects.get(id=id)
            foo.delete()
            return Response({'msg': 'Inventory Item Deleted Successfully','success':True})
        except Exception as e:
            return Response({'error': str(e),'success':False, "msg": "Something went wrong! Kindly recheck"})

class ServiceBookingAPI(APIView):

    def get(self,request):
        foo = ServiceBooking.objects.all().order_by('-id')
        serializer = ServiceBookingSerializer(foo, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ServiceBookingSerializer(data=request.data)
        if serializer.is_valid():
            service_items = request.data.get('service_items', [])
            print(service_items)
            stock_validation_errors = []

            # Validate stock availability for all items
            for item_data in service_items:
                item_id = item_data.get('id')
                quantity_requested = item_data.get('quantity')

                try:
                    item = InventoryItem.objects.get(id=item_id)
                    if item.quantity < quantity_requested:
                        stock_validation_errors.append(f"Insufficient stock for item {item.name}")
                except InventoryItem.DoesNotExist:
                    stock_validation_errors.append(f"Item with ID {item_id} does not exist")

            # If any validation errors, return error response
            if stock_validation_errors:
                return Response({'msg': 'Stock validation failed', 'errors': stock_validation_errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            # If stock validation passes, proceed with booking creation
            try:
                booking = serializer.save()
                for item_data in service_items:
                    item_id = item_data.get('id')
                    quantity_requested = item_data.get('quantity')

                    # Fetch inventory item
                    item = InventoryItem.objects.get(id=item_id)

                    # Deduct stock
                    item.quantity -= quantity_requested
                    item.save()

                    # Create ServiceBookingItem
                    ServiceBookingItem.objects.create(
                        booking=booking,
                        item=item,
                        quantity=quantity_requested,
                        cost=item.price * quantity_requested
                    )
                    print(f"{item = }")
                    try:
                        obj = ServiceBooking.objects.filter(id=booking.id).last()
                        obj.service_items.add(item)
                        obj.save()
                    except Exception as e:
                        print(f"{e = }")
                        pass


                return Response({'msg': 'Service Booking Created Successfully', 'success': True}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({'msg': 'Something went wrong!', 'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            id = self.request.query_params.get('id')
            foo = ServiceBooking.objects.get(id=id)

            # Fetch existing service items to handle stock rollback if needed
            existing_service_items = ServiceBookingItem.objects.filter(booking=foo)

            serializer = ServiceBookingSerializer(foo, data=request.data)
            if serializer.is_valid():
                service_items = request.data.get('service_items', [])
                stock_validation_errors = []

                # Validate stock for updated service items
                for item_data in service_items:
                    item_id = item_data.get('id')
                    quantity_requested = item_data.get('quantity')

                    try:
                        item = InventoryItem.objects.get(id=item_id)

                        # Calculate available stock including previously booked quantities
                        previous_quantity = existing_service_items.filter(item_id=item_id).first()
                        previous_quantity = previous_quantity.quantity if previous_quantity else 0
                        effective_stock = item.quantity + previous_quantity

                        if effective_stock < quantity_requested:
                            stock_validation_errors.append(f"Insufficient stock for item {item.name}")
                    except InventoryItem.DoesNotExist:
                        stock_validation_errors.append(f"Item with ID {item_id} does not exist")

                # If any validation errors, return error response
                if stock_validation_errors:
                    return Response({'msg': 'Stock validation failed', 'errors': stock_validation_errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)

                # Update service booking and adjust inventory
                for existing_item in existing_service_items:
                    # Restore inventory for previous booking
                    inventory_item = InventoryItem.objects.get(id=existing_item.item_id)
                    inventory_item.quantity += existing_item.quantity
                    inventory_item.save()
                    # Delete the existing item record
                    existing_item.delete()

                for item_data in service_items:
                    item_id = item_data.get('id')
                    quantity_requested = item_data.get('quantity')

                    # Deduct new quantities
                    item = InventoryItem.objects.get(id=item_id)
                    item.quantity -= quantity_requested
                    item.save()

                    # Update ServiceBookingItem
                    ServiceBookingItem.objects.create(
                        booking=foo,
                        item=item,
                        quantity=quantity_requested,
                        cost=item.price * quantity_requested
                    )

                serializer.save()
                return Response({'msg': 'Service Booking Updated Successfully', 'success': True})

            return Response({'error': serializer.errors, 'success': False, "msg": "Something went wrong! Kindly recheck"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e), 'success': False, "msg": "Something went wrong! Kindly recheck"})

    def delete(self,request):
        try:
            id = self.request.query_params.get('id')

            # Fetch the service booking
            foo = ServiceBooking.objects.get(id=id)

            # Restore inventory stock from service booking items
            service_items = ServiceBookingItem.objects.filter(booking=foo)
            for service_item in service_items:
                inventory_item = InventoryItem.objects.get(id=service_item.item.id)

                # Add back the booked quantity to inventory
                inventory_item.quantity += service_item.quantity
                inventory_item.save()

                # Delete the service booking item
                service_item.delete()

            # Delete the service booking
            foo.delete()

            return Response({'msg': 'Service Booking Deleted Successfully', 'success': True})
        
        except ServiceBooking.DoesNotExist:
            return Response({'msg': 'Service Booking not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e), 'success': False, "msg": "Something went wrong! Kindly recheck"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServiceBookingItemAPI(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self,request):
        foo = ServiceBookingItem.objects.all().order_by('-id')
        serializer = ServiceBookingItemSerializer(foo, many=True)
        return Response(serializer.data)
    
