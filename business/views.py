from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from business.models import Business
from voucher.models import Voucher, VoucherUsage
from portal.models import CaptiveSession
# from payments.models import BusinessSubscription
from business.forms import BusinessProfileForm, VoucherGenerationForm
from business.utils import check_subscription_limits
from voucher.services import create_vouchers


def get_current_business(request):
    """Helper to get selected or default business for the current user"""
    business_id = request.session.get('current_business_id')
    if business_id:
        business = get_object_or_404(
            Business, id=business_id, owner=request.user)
        if business:
            return business
    return request.user.businesses.first()


# @login_required
# def select_business(request):
#     """Allow user to select current business to manage"""
#     businesses = request.user.businesses.all()
#     if request.method == 'POST':
#         business_id = request.POST.get('business_id')
#         if Business.objects.filter(id=business_id, owner=request.user).exists():
#             request.session['current_business_id'] = business_id
#             return redirect('business_dashboard')
#     return render(request, 'business/select_business.html', {'businesses': businesses})


@login_required
def business_dashboard(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    total_vouchers = Voucher.objects.filter(business=business).count()
    active_vouchers = Voucher.objects.filter(
        business=business, is_active=True).count()
    expired_vouchers = Voucher.objects.filter(
        business=business, expires_at__lt=timezone.now()).count()
    total_sessions = CaptiveSession.objects.filter().count()

    context = {
        'business': business,
        'total_vouchers': total_vouchers,
        'active_vouchers': active_vouchers,
        'expired_vouchers': expired_vouchers,
        'total_sessions': total_sessions,
        # 'subscription': BusinessSubscription.objects.filter(business=business).first(),
    }
    return render(request, '../templates/business/dashboard.html', context)


@login_required
def my_voucher_list(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    vouchers = Voucher.objects.filter(business=business)
    filter_type = request.GET.get('filter')
    if filter_type == 'active':
        vouchers = vouchers.filter(is_active=True)
    elif filter_type == 'expired':
        vouchers = vouchers.filter(expires_at__lt=timezone.now())
    elif filter_type == 'used':
        vouchers = vouchers.filter(voucherusage__isnull=False)

    return render(request, 'business/voucher_list.html', {'vouchers': vouchers, 'business': business})


@login_required
def generate_vouchers_view(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    if request.method == 'POST':
        form = VoucherGenerationForm(request.POST)
        if form.is_valid():
            if not check_subscription_limits(business):
                form.add_error(
                    None, "Voucher quota exceeded. Upgrade your plan.")
            else:
                count = form.cleaned_data['count']
                duration = form.cleaned_data['duration_minutes']
                duration_days = duration * 1440
                prefix = form.cleaned_data.get('prefix', '')
                try:
                    vouchers = create_vouchers(
                        business=business,
                        count=count,
                        duration_minutes=duration_days,
                        prefix=prefix,
                        created_by=request.user
                    )
                    request.session['generated_voucher_ids'] = [
                        v.id for v in vouchers]
                    return redirect('view_generated_vouchers')
                except Exception as e:
                    form.add_error(None, str(e))
    else:
        form = VoucherGenerationForm()

    return render(request, 'business/generate_vouchers.html', {'form': form, 'business': business})


@login_required
def view_generated_vouchers(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    ids = request.session.get('generated_voucher_ids', [])
    vouchers = Voucher.objects.filter(id__in=ids)
    return render(request, 'business/voucher_generated_list.html', {'vouchers': vouchers, 'business': business})


@login_required
def edit_business_profile(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_dashboard')
    else:
        form = BusinessProfileForm(instance=business)

    return render(request, 'business/edit_profile.html', {'form': form, 'business': business})


@login_required
def usage_stats_view(request):
    business = get_current_business(request)
    # if not business:
    #     return redirect('select_business')

    usage_by_day = (
        VoucherUsage.objects
        .filter(voucher__business=business)
        .values(day=timezone.now().date())  # group logic can be improved
        .annotate(count=Count('id'))
        .order_by('day')
    )
    return render(request, 'business/usage_stats.html', {'usage_by_day': usage_by_day, 'business': business})
