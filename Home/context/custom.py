from Home.models import Activity

def activity_count(request):
    count = Activity.objects.all().count()
    return {'total_activity':count}