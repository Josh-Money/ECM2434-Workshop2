from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import AmountType, ItemType, IndividualItem, ShoppingList
import json 

@require_http_methods(["PUT"])
def add_item(request):
    try:
        data = json.loads(request.body)

        required_fields = ['itemType', 'expirationDate', 'amount']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
            
        try:
            expiration_date = datetime.strptime(data['expirationdate'], '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'messsage': 'Invalid date format. Use YYYY-MM-DD'
            }, status=400)
        
        if not isinstance(data['amount'], int) or data['amount'] <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Amount must be a positive integer'
            }, status=400)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Item added successfully',
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@require_http_methods(['DELETE'])
def delete_item(request):
    try:
        data = json.loads(request.body)

        if 'ID' not in data:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required field: ID'
            }, status=400)

        item_id = data['ID']

        IndividualItem.objects.filter(id=item_id).delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Item deleted successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@require_http_methods(['DELETE'])
def delete_items(request):
    try:
        data = json.loads(request.body)

        if not isinstance(data, list):
            return JsonResponse({
                'status': 'error',
                'message': 'Request body must be a list'
            }, status=400)
    
        item_ids = [item['ID'] for item in data if 'ID' in item]

        if not item_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required field: ID'
            }, status=400)
        
        IndividualItem.objects.filter(id__in=item_ids).delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Items deleted successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(['PUT'])
def new_type (request):
    try:
        data = json.loads(request.body)
    
        required_fields = ['unique_barcode', 'name', 'amount_type']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        if not isinstance(data['unique_barcode'], str) or not data['unique_barcode']:
            return JsonResponse({
                'status': 'error',
                'message': 'Unique barcode must be a non-empty string'
            }, status=400)
        
        if not isinstance(data['name'], str) or not data['name']:
            return JsonResponse({
                'status': 'error',
                'message': 'Name must be a non-empty string'
            }, status=400)
        
        if not isinstance(data['amount_type'], str) or not data['amount_type']:
            return JsonResponse({
                'status': 'error',
                'message': 'Amount type must be a non-empty string'
            }, status=400)
        
        if not AmountType.objects.filter(name=data['amount_type']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Amount type does not exist'
            }, status=400)
        
        ItemType.objects.create(
            unique_barcode=data['unique_barcode'],
            name=data['name'],
            amount_type=AmountType.objects.get(name=data['amount_type']))
        
        return JsonResponse({
            'status': 'success',
            'message': 'Type added successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(['DELETE'])
def remove_type(request):
    try:
        data = json.loads(request.body)

        if 'unique_barcode' not in data:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required field: unique_barcode'
            }, status=400)
        
        unique_barcode = data['unique_barcode']

        if IndividualItem.objects.filter(item_type__unique_barcode=unique_barcode).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Cannot remove type because items of this type exist'
            }, status=400)

        ItemType.objects.filter(unique_barcode=unique_barcode).delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Type removed successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@require_http_methods(['PUT'])
def add_to_shopping_list(request):
    try:
        data = json.loads(request.body)

        required_fields = ['itemType', 'amount']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        if not isinstance(data['amount'], int) or data['amount'] <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Amount must be a positive integer'
            }, status=400)
        
        if not ItemType.objects.filter(unique_barcode=data['itemType']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Item type does not exist'
            }, status=400)
        
        item_type = ItemType.objects.get(unique_barcode=data['itemType'])
        
        shopping_list_item, created = ShoppingList.objects.get_or_create(
            item_type=item_type,
            defaults={'amount': data['amount']}
        )
        
        if not created:
            shopping_list_item.amount += data['amount']
            shopping_list_item.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Item added to shopping list successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(['DELETE'])
def remove_from_shopping_list(request):
    try:
        data = json.loads(request.body)

        required_fields = ['itemType', 'amount']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        if not isinstance(data['amount'], int) or data['amount'] <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Amount must be a positive integer'
            }, status=400)
        
        if not ItemType.objects.filter(unique_barcode=data['itemType']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Item type does not exist'
            }, status=400)
        
        item_type = ItemType.objects.get(unique_barcode=data['itemType'])

        try:
            shopping_list_item = ShoppingList.objects.get(item_type=item_type)
        except ShoppingList.DoesNotExist:
            return JsonResponse({
            'status': 'error',
            'message': 'Item not found in shopping list'
            }, status=400)

        shopping_list_item.amount -= data['amount']
        
        if shopping_list_item.amount <= 0:
            shopping_list_item.delete()
        else:
            shopping_list_item.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Item removed from shopping list successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@require_http_methods(['PATCH'])
def purchase_item(request):
    try:
        data = json.loads(request.body)
        required_fields = ['itemType', 'amount', 'expirationDate']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        if not isinstance(data['amount'], int) or data['amount'] <= 0:
            return JsonResponse({
            'status': 'error',
            'message': 'Amount must be a positive integer'
            }, status=400)
        
        try:
            expiration_date = datetime.strptime(data['expirationDate'], '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
            'status': 'error',
            'message': 'Invalid date format. Use YYYY-MM-DD'
            }, status=400)
        
        if not ItemType.objects.filter(unique_barcode=data['itemType']).exists():
            return JsonResponse({
            'status': 'error',
            'message': 'Item type does not exist'
            }, status=400)
        
        item_type = ItemType.objects.get(unique_barcode=data['itemType'])

        try:
            shopping_list_item = ShoppingList.objects.get(item_type=item_type)
        except ShoppingList.DoesNotExist:
            return JsonResponse({
            'status': 'error',
            'message': 'Item not found in shopping list'
            }, status=400)

        if shopping_list_item.amount < data['amount']:
            return JsonResponse({
            'status': 'error',
            'message': 'Not enough amount in shopping list'
            }, status=400)

        shopping_list_item.amount -= data['amount']
        
        if shopping_list_item.amount <= 0:
            shopping_list_item.delete()
        else:
            shopping_list_item.save()

        IndividualItem.objects.create(
            item_type=item_type,
            amount=data['amount'],
            expiration_date=expiration_date
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Item purchased and added to fridge successfully'
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
        