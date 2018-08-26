from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import hashers
from .models import Familia, Solicitud, Match
from datetime import timedelta, date
from django.template import loader
from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Sum
from django.db.models import Q
from django.db.models.base import ObjectDoesNotExist
import json
import datetime


class Index(TemplateView):
    template_name = 'inicio_sesion.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        nombre_familia = request.POST['usuario']
        contrasenia = request.POST['contrasenia']
        try:
            familia = Familia.objects.get(usuario=nombre_familia)
        except Familia.DoesNotExist:
            return redirect('SCPapp:index')
        if (familia.contrasenia1 == contrasenia):
            request.session['usuario'] = familia.usuario
            if (familia.escuela == True):
                return redirect('SCPapp:main')
            return redirect('SCPapp:main')

        return redirect('SCPapp:index')


class Main(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            us = Familia.objects.get(usuario=usuario)
            args = {
                'usuario': usuario,
            }
            if (us.escuela == True):
                return render(request, 'base2.html', args)
            return render(request, 'base.html', args)

    def post(self, request):
        if 'salir' in request.POST:
            try:
                if 'usuario' in request.session:
                    del request.session['usuario']
            except KeyError:
                pass
            return redirect('SCPapp:index')


def listar_familias(request):
    familia = request.GET['usuario']

    familia2 = Familia.objects.get(usuario=familia)
    familias = Familia.objects.filter(colonia=familia2.colonia).exclude(usuario=familia)

    html_codigo = """<table id="customers">
  <tr>
    <th>Nombre</th>
    <th>Pasajeros</th>
    <th>Colonia</th>
    <th>Celular</th>
    <th>Confirmacion</th>

  </tr>"""
    for familia in familias:
        html_codigo += """
          <tr>
    <td>{0}</td>
    <td>{1}</td>
    <td>{2}</td>
    <td>{3}</td>
    <td><button id="{0}-yes" onclick="solicitarPool(this)"> YES</button></td>
  </tr>
        """.format(familia.usuario, familia.pasajeros, familia.colonia, familia.celular)
    html_codigo += "</table>"

    args = {
        'html_codigo': html_codigo,
    }
    return HttpResponse(html_codigo)


def listar_solicitudes(request):
    us1 = request.GET['usuario_sol']
    sols = Solicitud.objects.filter(usuario_recibe_id=us1)
    aceptados = Match.objects.filter(usuario_auto_id=us1)
    for aceptado in aceptados:
        for sol in sols:
            if (aceptado.usuario_acomodado_id == sol.usuario_sol_id):
                sols.remove(sol)

    html_codigo = """<table id="customers">
    <tr>
      <th>Nombre</th>
      <th>Lugares ocupar</th>
      <th>Lugares disponibles</th>
      <th>Colonia</th>
      <th>Celular</th>
      <th>Aceptar/Denegar</th>
    </tr>"""
    for sol in sols:
        html_codigo += """
                <tr>
          <td>{0}</td>
          <td>{1}</td>
          <td>{4}</td>
          <td>{2}</td>
          <td>{3}</td>
        <td><button id="{0}-si" onclick="aceptarPool(this)"> SI</button><button id="{0}-noo" onclick="denegarPool(this)"> NO</button></td>

        </tr>
              """.format(sol.usuario_sol.usuario, sol.usuario_sol.ocupantes, sol.usuario_sol.colonia,
                         sol.usuario_sol.celular, sol.usuario_sol.pasajeros)
    html_codigo += "</table>"
    return HttpResponse(html_codigo, content_type="text/html")


def solicitar(request):
    us1 = request.GET['usuario']
    us2 = request.GET['usuario_sol']

    try:
        sol = Solicitud(usuario_recibe_id=us1, usuario_sol_id=us2)
        sol.full_clean()
        sol.save()
    except ValidationError or ValueError as e:
        return HttpResponse(e.messages, content_type='text/html')

    return HttpResponse("Success", content_type='text/html')


def aceptar(request):
    us_auto = request.GET['usuario_auto']
    us_acomodado = request.GET['usuario_acomodado']

    try:
        sol = Match(usuario_auto_id=us_auto, usuario_acomodado_id=us_acomodado)
        sol.full_clean()
        sol.save()
    except ValidationError or ValueError as e:
        return HttpResponse(e.messages, content_type='text/html')
    try:
        us1 = Familia.objects.get(usuario=us_auto)
        us2 = Familia.objects.get(usuario=us_acomodado)

        us1.pasajeros = us1.pasajeros - us2.ocupantes
        us2.pasajeros = us2.pasajeros - us1.ocupantes
        us1.ocupantes = us1.ocupantes + us2.ocupantes
        us2.ocupantes = us1.ocupantes
        if (us1.pasajeros <= us2.pasajeros):
            us2.pasajeros = us1.pasajeros
        else:
            us1.pasajeros = us2.pasajeros

        us1.full_clean()
        us2.full_clean()
        us1.save()
        us2.save()
    except ValidationError or Familia.DoesNotExist as e:
        return HttpResponse(e.messages)

    return HttpResponse("Success", content_type='text/html')


def listar_matches(request):
    us = request.GET['usuario']
    matches = Match.objects.filter(
        Q(usuario_auto_id=us) |
        Q(usuario_acomodado_id=us)
    )
    html_codigo = """<table id="customers">
        <tr>
          <th>Nombre</th>
          <th>Lugares ocupar</th>
          <th>Colonia</th>
          <th>Celular</th>
        </tr>"""
    for match in matches:
        html_codigo += """
                <tr>
          <td>{0}</td>
          <td>{1}</td>
          <td>{2}</td>
          <td>{3}</td>
        </tr>
              """.format(match.usuario_acomodado.usuario, match.usuario_acomodado.ocupantes,
                         match.usuario_acomodado.colonia, match.usuario_acomodado.celular)
        html_codigo += "</table>"
        html_codigo += """
        <br>
            <table id="customers">
          <tr>
            <th>Lunes</th>
            <th>Martes</th>
            <th>Miercoles</th>
            <th>Jueves</th>
            <th>Viernes</th>
          </tr>
          <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
          </tr>


          <tr>
        <td> <button id="l" onclick="registrarDia(this)">INSCRIBIR</button> </td>
        <td> <button id="m" onclick="registrarDia(this)">INSCRIBIR</button> </td>
        <td> <button id="mi" onclick="registrarDia(this)">INSCRIBIR</button> </td>
        <td> <button id="j" onclick="registrarDia(this)">INSCRIBIR</button> </td>
        <td> <button id="v" onclick="registrarDia(this)">INSCRIBIR</button> </td>
        </tr>
        </table>
            """.format(match.lunes, match.martes, match.miercoles, match.jueves, match.viernes)


    return HttpResponse(html_codigo)

def registrar_dia(request):
    dia = request.GET['dia']
    us = request.GET['usuario']
    if(dia == 'l'):
        try:
            match = Match.objects.get(
                Q(usuario_auto_id=us) |
                Q(usuario_acomodado_id=us)
            )
            match.lunes = us
            match.full_clean()
            match.save()
        except ValidationError as e:
            return HttpResponse(e.messages)
        return HttpResponse("Success")
    elif(dia == 'm'):
        try:
            match = Match.objects.get(
                Q(usuario_auto_id=us) |
                Q(usuario_acomodado_id=us)
            )
            match.martes = us
            match.full_clean()
            match.save()
        except ValidationError as e:
            return HttpResponse(e.messages)
        return HttpResponse("Success")
    elif (dia == 'mi'):
        try:
            match = Match.objects.get(
                Q(usuario_auto_id=us) |
                Q(usuario_acomodado_id=us)
            )
            match.miercoles = us
            match.full_clean()
            match.save()
        except ValidationError as e:
            return HttpResponse(e.messages)
        return HttpResponse("Success")
    elif (dia == 'j'):
        try:
            match = Match.objects.get(
                Q(usuario_auto_id=us) |
                Q(usuario_acomodado_id=us)
            )
            match.jueves = us
            match.full_clean()
            match.save()
        except ValidationError as e:
            return HttpResponse(e.messages)
        return HttpResponse("Success")
    elif (dia == 'v'):
        try:
            match = Match.objects.get(
                Q(usuario_auto_id=us) |
                Q(usuario_acomodado_id=us)
            )
            match.viernes = us
            match.full_clean()
            match.save()
        except ValidationError as e:
            return HttpResponse(e.messages)
        return HttpResponse("Success")
    return HttpResponse("Error")


