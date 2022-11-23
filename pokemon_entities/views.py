import folium
import json

from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import now


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now_time = now()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now_time, disappeared_at__gte=now_time)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                f'media/{pokemon_entity.pokemon.photo}'
            )
        )
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(
                f'media/{pokemon.photo}'
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    now_time = now()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now_time, disappeared_at__gte=now_time)
    about_previous_evolution = {}
    about_next_evolution = {}
    if requested_pokemon.previous_evolution:
        about_previous_evolution = {
            'title_ru': requested_pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(
                requested_pokemon.previous_evolution.photo.url
            ),
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'description': requested_pokemon.previous_evolution.description,
            'title_en': requested_pokemon.previous_evolution.title_en,
            'title_jp': requested_pokemon.previous_evolution.title_jp,
        }
    if requested_pokemon.next_evolutions.count() != 0:
        about_next_evolution = {
            'title_ru': requested_pokemon.next_evolutions.all()[0].title,
            'img_url': request.build_absolute_uri(
                requested_pokemon.next_evolutions.all()[0].photo.url
            ),
            'pokemon_id': requested_pokemon.next_evolutions.all()[0].id,
            'description': requested_pokemon.next_evolutions.all()[0].description,
            'title_en': requested_pokemon.next_evolutions.all()[0].title_en,
            'title_jp': requested_pokemon.next_evolutions.all()[0].title_jp,
        }
    about_pokemon = {
        'img_url': request.build_absolute_uri(
            requested_pokemon.photo.url
        ),
        'title_ru': requested_pokemon.title,
        'pokemon_id': requested_pokemon.id,
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'next_evolution': about_next_evolution,
        'previous_evolution': about_previous_evolution,
    }
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            about_pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': about_pokemon
    })
