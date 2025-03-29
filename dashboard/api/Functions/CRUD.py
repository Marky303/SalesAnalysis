import json
from datetime import datetime, timedelta
import random
import string
from decimal import Decimal
import math
from django.db.models import Sum, F, Min, Max, ExpressionWrapper, DecimalField
from calendar import monthrange
from pytz import UTC  


# Import models
from sales.models import *
from analysis.models import *

# CRUD functions
def getOverviewThisMonthCRUD():
    # Get last month's date
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Calculate rev
    recent_orders = SalesOrderHeaderFact.objects.filter(OrderDate__gte=thirty_days_ago)
    revenue = recent_orders.aggregate(total=Sum('SubTotal'))['total']
    
    # Calculate cost
    cost = float(0)
    for order in recent_orders:        
        # Get the salesorderdetail
        salesOrderDetailLst = SalesOrderDetailFact.objects.filter(SalesOrder=order)
        
        for item in salesOrderDetailLst:
            # Get quantity
            quantity = item.OrderQty
            
            # Get cost
            singleCost = item.Product.StandardCost
            
            # Add to cost
            cost = cost + float(quantity) * float(singleCost)

    # Calculate profit
    profit = (float(revenue) if revenue else float(0)) - cost
    
    # Create result template
    result = {
        "revenue": round(float(revenue) if revenue else float(0), 1),
        "profit": round(profit, 1),
        "cost": round(cost, 1)
    }
    
    # Return the thingy
    return result



def getOverviewLastMonthsCRUD():
    # Get current UTC date
    now = datetime.now(UTC)
    
    # Create the result list
    results = []
    
    for i in range(0, 6):  
        current_month = (now.month - i - 1) % 12 + 1
        current_year = now.year + (now.month - i - 1) // 12
        
        month_start = datetime(current_year, current_month, 1, 0, 0, 0, tzinfo=UTC)
        last_day = monthrange(current_year, current_month)[1]
        month_end = datetime(current_year, current_month, last_day, 23, 59, 59, tzinfo=UTC)
        
        monthly_orders = SalesOrderHeaderFact.objects.filter(OrderDate__range=[month_start, month_end])
        
        # TEST ONLY
        # print(str(monthly_orders.query))
        
        revenue = monthly_orders.aggregate(total=Sum('SubTotal'))['total']
        
        # Calculate cost
        cost = float(0)
        for order in monthly_orders:
            # Get the sales order details
            salesOrderDetailLst = SalesOrderDetailFact.objects.filter(SalesOrder=order)
            
            for item in salesOrderDetailLst:
                # Get quantity and cost
                quantity = item.OrderQty
                singleCost = item.Product.StandardCost
                
                # Add to cost
                cost += float(quantity) * float(singleCost)
        
        # # Calculate profit
        # profit = (float(revenue) if revenue else float(0)) - cost
        
        # Add the result for the month
        results.append({
            "time": month_start.strftime("%B %Y"),  # e.g., "November 2024"
            "revenue": round(float(revenue) if revenue else float(0), 1),
            # "profit": round(profit, 1),
            "cost": round(cost, 1)
        })
    
    # Reverse the list to make it in order
    results.reverse()
    
    return results



def getTopProductsCRUD():
    # Get the 30 days ago date
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Filter SalesOrderDetailFact by orders placed in the last 30 days
    top_products = (
        SalesOrderDetailFact.objects
        .filter(SalesOrder__OrderDate__gte=thirty_days_ago)  
        .values('Product__id', 'Product__Name')  
        .annotate(total_revenue=Sum('LineTotal'))  
        .order_by('-total_revenue')[:3]  
    )
    
    # Result template
    result = [
        {
            "id": product['Product__id'],
            "name": product['Product__Name'],
            "revenue": float(product['total_revenue'])
        }
        for product in top_products
    ]
    
    return result



def getTopTerritoryCRUD():
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    sales_orders = SalesOrderHeaderFact.objects.filter(OrderDate__gte=thirty_days_ago)
    
    territories_data = (
        sales_orders
        .values('Customer__Territory__id', 'Customer__Territory__Name')  # Group by Territory ID and Name
        .annotate(
            total_revenue=Sum('SubTotal'),  # Calculate revenue
            total_cost=Sum(
                F('salesorderdetailfact__OrderQty') * F('salesorderdetailfact__Product__StandardCost')  # Calculate cost
            ),
        )
    )
    
    # # Calculate profit for each territory
    # for territory in territories_data:
    #     territory['profit'] = float(territory['total_revenue']) - float(territory['total_cost'] or 0)
    
    # Sort by revenue and get 3 highest
    top_territories = sorted(territories_data, key=lambda x: x['total_revenue'], reverse=True)[:3]
    
    # Create result template
    result = [
        {
            "id": territory['Customer__Territory__id'],
            "name": territory['Customer__Territory__Name'],
            "revenue": round(float(territory['total_revenue']), 2),
            "cost": round(float(territory['total_cost'] or 0), 2),
            # "profit": round(float(territory['profit']), 2),
        }
        for territory in top_territories
    ]
    
    return result

# ___________________________________________________________________
def getQueryDatesCRUD(request):
    dict_body = request.body.decode("UTF-8")
    dateInfo = json.loads(dict_body)

    earliestDate = SalesOrderHeaderFact.objects.aggregate(earliest=Min('OrderDate'))['earliest']
    if earliestDate and earliestDate.tzinfo:
        earliestDate = earliestDate.replace(tzinfo=None)
        
    latestDate = SalesOrderHeaderFact.objects.aggregate(latest=Max('OrderDate'))['latest']
    if latestDate and latestDate.tzinfo:
        latestDate = latestDate.replace(tzinfo=None)

    if dateInfo['startDate'] is None:
        startDate = earliestDate
    else:
        startDateObj = datetime.strptime(dateInfo['startDate'], '%Y-%m-%d')
        startDate = earliestDate if earliestDate and earliestDate > startDateObj else startDateObj

    if dateInfo['endDate'] is None:
        endDate = latestDate
    else:
        endDateObj = datetime.strptime(dateInfo['endDate'], '%Y-%m-%d')
        endDate = latestDate if latestDate and latestDate < endDateObj else endDateObj

    return startDate, endDate

def getDashboardCRUD(startDate, endDate):
    dashboardData = {
        'KPI': None,
        'Products': None,
        'Regions': None,
        'Progression': None,
    }
    
    dashboardData['KPI'] = getKPI(startDate, endDate)
    dashboardData['Products'] = getProducts(startDate, endDate)
    dashboardData['Regions'] = getRegions(startDate, endDate)
    dashboardData['Progression'] = getProgression(startDate, endDate)

    return dashboardData

def getKPI(startDate, endDate):
    KPIData = {
        'orders':   SalesOrderHeaderFact.objects.filter(OrderDate__gte=startDate, OrderDate__lte=endDate).count(),
        'revenue':  float(SalesOrderHeaderFact.objects.filter(OrderDate__gte=startDate, OrderDate__lte=endDate).aggregate(total=Sum('TotalDue'))['total'] or 0),
        'tax':      float(SalesOrderHeaderFact.objects.filter(OrderDate__gte=startDate, OrderDate__lte=endDate).aggregate(total=Sum('TaxAmt'))['total'] or 0),
        'freight':  float(SalesOrderHeaderFact.objects.filter(OrderDate__gte=startDate, OrderDate__lte=endDate).aggregate(total=Sum('Freight'))['total'] or 0),
        'sales':    float(SalesOrderHeaderFact.objects.filter(OrderDate__gte=startDate, OrderDate__lte=endDate).aggregate(total=Sum('SubTotal'))['total'] or 0),
        'cost':     - float(SalesOrderDetailFact.objects.filter(
                        SalesOrder__OrderDate__gte=startDate,
                        SalesOrder__OrderDate__lte=endDate
                    ).aggregate(
                        total=Sum(
                            ExpressionWrapper(
                                (F('Product__ListPrice') * (1 - F('SpecialOffer__DiscountPct'))) - F('Product__StandardCost'),
                                output_field=DecimalField()
                            ) * F('OrderQty')
                        )
                    )['total'] or 0)
    }
    KPIData['profit'] = KPIData['sales'] - KPIData['cost']
    return KPIData

def getProducts(startDate, endDate):
    products = list(
        SalesOrderDetailFact.objects.filter(
            SalesOrder__OrderDate__gte=startDate,
            SalesOrder__OrderDate__lte=endDate
        ).values(
            'Product__id', 'Product__Name'
        ).annotate(
            sales=Sum(F('OrderQty') * F('Product__ListPrice') * (1 - F('SpecialOffer__DiscountPct'))),
            sold=Sum('OrderQty')
        ).order_by('-sales')[:5]
    )
    for product in products:
        product['sales']    = float(product['sales'] or 0)
        product['sold']     = int(product['sold'] or 0)
        product['id']       = product.pop('Product__id')
        product['name']     = product.pop('Product__Name')
    return products

def getRegions(startDate, endDate):
    regions = list(
        SalesOrderDetailFact.objects.filter(
            SalesOrder__OrderDate__gte=startDate,
            SalesOrder__OrderDate__lte=endDate
        ).values(
            'SalesOrder__Customer__Territory__id', 
            'SalesOrder__Customer__Territory__Name'
        ).annotate(
            sales=Sum(F('OrderQty') * F('Product__ListPrice') * (1 - F('SpecialOffer__DiscountPct'))),
            sold=Sum('OrderQty')
        ).order_by('-sales')[:5]
    )
    for region in regions:
        region['sales']     = float(region['sales'] or 0)
        region['sold']      = int(region['sold'] or 0)
        region['id']        = region.pop('SalesOrder__Customer__Territory__id')
        region['name']      = region.pop('SalesOrder__Customer__Territory__Name')
    return regions

def getProgression(startDate, endDate):
    progression = []
    currentDate = startDate

    while currentDate <= endDate:
        daily_stats = SalesOrderHeaderFact.objects.filter(OrderDate__date=currentDate).aggregate(
            order=Sum(1),
            revenue=Sum('TotalDue'),
            tax=Sum('TaxAmt'),
            freight=Sum('Freight'),
            sales=Sum('SubTotal'),
            cost=Sum(F('salesorderdetailfact__Product__StandardCost') * F('salesorderdetailfact__OrderQty')),
            profit=Sum('SubTotal') - Sum(F('salesorderdetailfact__Product__StandardCost') * F('salesorderdetailfact__OrderQty'))
        )

        progression.append({
            'date':     currentDate.strftime('%Y-%m-%d'),
            'order':    float(daily_stats['order'] or 0),
            'revenue':  float(daily_stats['revenue'] or 0),
            'tax':      float(daily_stats['tax'] or 0),
            'freight':  float(daily_stats['freight'] or 0),
            'sales':    float(daily_stats['sales'] or 0),
            'cost':     float(daily_stats['cost'] or 0),
            'profit':   float(daily_stats['profit'] or 0)
        })

        currentDate += timedelta(days=1)

    return progression