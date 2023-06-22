from django.shortcuts import render
from account.models.professional import Professional
from django.db.models import Q
from search.models import Search


def search(request, ID):
    professionals = Professional.objects.all()
    last_searches = Search.get_last_professionals_search_by_client(user=ID)

    context = {
        'professionals': professionals,
        'last_searches': last_searches,
    }

    if request.method == 'GET':
        return render(request, 'search/search.html', context=context)

    elif request.method == 'POST':
        professionals = Professional.objects.all()
        profession: str = request.POST.get("profession", "")
        # Convert profession label -> profession key
        if profession:
            for profession_key, profession_label in Professional.Professions.choices:
                if profession.lower() in profession_label.lower():
                    profession = profession_key
                    break
        # Capitalize each word in each parameter
        first_name = ' '.join([word.capitalize() for word in request.POST.get("first-name", "").split()])
        last_name = ' '.join([word.capitalize() for word in request.POST.get("last-name", "").split()])
        city = ' '.join([word.capitalize() for word in request.POST.get("city", "").split()])

        professionals = professionals.filter(
            Q(profession=profession) if profession else Q(),
            Q(user__first_name__startswith=first_name) if first_name else Q(),
            Q(user__last_name__startswith=last_name) if last_name else Q(),
            Q(user__city__startswith=city) if city else Q()
        )
        if not professionals.exists():
            professionals = []
        context = {
            'professionals': professionals,
            'last_searches': last_searches,
        }
        return render(request, 'search/search.html', context=context)
