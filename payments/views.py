from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PaymentTransaction, WebhookLog
from business.models import Business
import json

# simplified webhook handler


@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        WebhookLog.objects.create(
            business_id=payload.get("business_id"),
            event=payload.get("event", "unknown"),
            payload=payload
        )
        return JsonResponse({"status": "received"})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def mpesa_webhook(request):
    # Stub: parse incoming payload and log it
    if request.method == 'POST':
        data = request.POST.dict()

        # Extract relevant fields (customize for Daraja payload)
        txn_id = data.get('transaction_id')
        phone = data.get('phone_number')
        amount = data.get('amount')
        business_id = data.get('business_id')  # Optional

        # Basic check
        if not all([txn_id, phone, amount]):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # Save transaction
        PaymentTransaction.objects.get_or_create(
            transaction_id=txn_id,
            defaults={
                'phone_number': phone,
                'amount': amount,
                'status': 'SUCCESS',
                'business_id': business_id if business_id else None
            }
        )
        # Voucher generation logic to be added here
        return JsonResponse({'message': 'OK'}, status=200)

    return JsonResponse({'error': 'Invalid method'}, status=405)
