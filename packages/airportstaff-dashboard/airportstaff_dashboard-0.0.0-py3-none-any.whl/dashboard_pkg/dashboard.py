
from django.shortcuts import render
from .models import Feedbacks, TheLostItems

def airportstaffdashboard(request):
    feedbacks_list = Feedbacks.objects.all()
    founditems_list = TheLostItems.objects.filter(found=True)
    context = {
        'feedbacks_list': feedbacks_list,
        'founditems_list': founditems_list,
    }
    return render(request, 'airport_staff/airport_staff_dashboard.html', context)

# This function displays the dashboard for airport staff.
# Gets a list of all feedback entries from the database.
# Gets a list of all items that have been marked as found.
# The function then prepares a context dictionary containing these lists.
# It is used in my web application for dashboard template ('airport_staff/airport_staff_dashboard.html') for feedbacks and found items.
