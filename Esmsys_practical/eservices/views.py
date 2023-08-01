from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import District, Taluka, Village

@csrf_exempt
def get_all_data(request):
    district = District.objects.all()
    taluka = Taluka.objects.all()
    village = Village.objects.all()

    total_districts = district.count()
    total_talukas = taluka.count()
    total_villages = village.count()

    data = {
        "district": list(district.values()),
        "taluka": list(taluka.values()),
        "village": list(village.values()),
        "total_districts": total_districts,
        "total_talukas": total_talukas,
        "total_villages": total_villages,
    }

    return JsonResponse(data)

@csrf_exempt
def add_entry(request):
    if request.method == 'POST':
        name = request.POST.get('t_name')
        taluka_id = request.POST.get('t_id') 

        if not name or not taluka_id:
            return JsonResponse({"error": "Name and Taluka ID are required."}, status=400)

        try:
            taluka = Taluka.objects.get(pk=id)
            village = Village(name=village_name, taluka=t_name)
            village.save()

            return JsonResponse({"message": "Village added successfully."}, status=201)
        except Taluka.DoesNotExist:
            return JsonResponse({"error": "Taluka with the given ID does not exist."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def delete_entry(request, entry_type, id):
    try:
        if entry_type == 'district':
            District.objects.get(pk=id).delete()
        elif entry_type == 'taluka':
            Taluka.objects.get(pk=id).delete()
        elif entry_type == 'village':
            Village.objects.get(pk=id).delete()
        else:
            return JsonResponse({"error": "Invalid entry type."}, status=400)

        return JsonResponse({"message": f"{entry_type.capitalize()} deleted successfully."}, status=200)
    except (District.DoesNotExist, Taluka.DoesNotExist, Village.DoesNotExist):
        return JsonResponse({"error": "Entry not found."}, status=404)
