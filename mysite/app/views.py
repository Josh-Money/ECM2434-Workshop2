from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
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