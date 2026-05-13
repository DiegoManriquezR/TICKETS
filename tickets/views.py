from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Ticket, Cliente, Comentario
from .forms import TicketForm, TicketUpdateForm, ClienteForm, ComentarioForm, TicketFilterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Ticket


def login_view(request):
    """Vista para iniciar sesión"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'usuarios/login.html')  # Plantilla de login


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')  # Redirige al login

@login_required
def dashboard(request):
    """Dashboard principal con estadísticas y resumen"""
    total_tickets = Ticket.objects.count()
    tickets_abiertos = Ticket.objects.filter(estado='abierto').count()
    tickets_en_proceso = Ticket.objects.filter(estado='en_proceso').count()
    tickets_resueltos = Ticket.objects.filter(estado='resuelto').count()
    tickets_cerrados = Ticket.objects.filter(estado='cerrado').count()
    
    tickets_criticos = Ticket.objects.filter(prioridad='critica').exclude(estado='cerrado').count()
    tickets_alta = Ticket.objects.filter(prioridad='alta').exclude(estado='cerrado').count()
    
    tickets_recientes = Ticket.objects.all()[:5]
    
    mis_tickets = None
    if request.user.is_staff:
        mis_tickets = Ticket.objects.filter(tecnico_asignado=request.user).exclude(estado='cerrado')[:5]
    
    total_clientes = Cliente.objects.filter(activo=True).count()
    
    context = {
        'total_tickets': total_tickets,
        'tickets_abiertos': tickets_abiertos,
        'tickets_en_proceso': tickets_en_proceso,
        'tickets_resueltos': tickets_resueltos,
        'tickets_cerrados': tickets_cerrados,
        'tickets_criticos': tickets_criticos,
        'tickets_alta': tickets_alta,
        'tickets_recientes': tickets_recientes,
        'mis_tickets': mis_tickets,
        'total_clientes': total_clientes,
    }
    
    return render(request, 'tickets/dashboard.html', context)


@login_required
def lista_tickets(request):
    """Lista de tickets con filtros"""
    tickets = Ticket.objects.select_related('cliente', 'tecnico_asignado', 'creado_por').all()
    
    form = TicketFilterForm(request.GET)
    if form.is_valid():
        estado = form.cleaned_data.get('estado')
        prioridad = form.cleaned_data.get('prioridad')
        tecnico = form.cleaned_data.get('tecnico')
        buscar = form.cleaned_data.get('buscar')
        
        if estado:
            tickets = tickets.filter(estado=estado)
        if prioridad:
            tickets = tickets.filter(prioridad=prioridad)
        if tecnico:
            tickets = tickets.filter(tecnico_asignado=tecnico)
        if buscar:
            tickets = tickets.filter(
                Q(titulo__icontains=buscar) | 
                Q(descripcion__icontains=buscar) |
                Q(cliente__nombre__icontains=buscar)
            )
    
    context = {
        'tickets': tickets,
        'form': form,
    }
    
    return render(request, 'tickets/lista_tickets.html', context)


@login_required
def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comentarios = ticket.comentarios.all()
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.ticket = ticket
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente.')
            return redirect('detalle_ticket', ticket_id=ticket.id)
    else:
        form = ComentarioForm()
    
    context = {
        'ticket': ticket,
        'comentarios': comentarios,
        'form': form,
    }
    
    return render(request, 'tickets/detalle_ticket.html', context)


@login_required
def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creado_por = request.user
            ticket.save()
            messages.success(request, f'Ticket #{ticket.id} creado exitosamente.')
            return redirect('detalle_ticket', ticket_id=ticket.id)
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TicketForm()
    
    return render(request, 'tickets/form_ticket.html', {'form': form, 'titulo': 'Crear Nuevo Ticket'})


@login_required
def editar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket #{ticket.id} actualizado.')
            return redirect('detalle_ticket', ticket_id=ticket.id)
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TicketUpdateForm(instance=ticket)
    
    return render(request, 'tickets/form_ticket.html', {'form': form, 'ticket': ticket, 'titulo': f'Editar Ticket #{ticket.id}'})


@login_required
def eliminar_ticket(request, id):
    # Obtener el ticket o devolver error 404 si no existe
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'POST':
        # Guardar los datos antes de eliminar
        ticket_id = ticket.id
        titulo = ticket.titulo

        # Eliminar el ticket
        ticket.delete()

        # Mostrar mensaje con el número correcto
        messages.success(request, f"✅ Ticket #{ticket_id} - '{titulo}' eliminado correctamente.")

        # Redirigir a la lista de tickets
        return redirect('lista_tickets')

    # Si no se confirma, mostrar la plantilla de confirmación
    return render(request, 'tickets/eliminar_ticket.html', {'ticket': ticket})



# CRUD Clientes
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    buscar = request.GET.get('buscar', '')
    if buscar:
        clientes = clientes.filter(
            Q(nombre__icontains=buscar) |
            Q(email__icontains=buscar) |
            Q(empresa__icontains=buscar)
        )
    return render(request, 'tickets/lista_clientes.html', {'clientes': clientes, 'buscar': buscar})


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre} creado.')
            return redirect('lista_clientes')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = ClienteForm()
    
    return render(request, 'tickets/form_cliente.html', {'form': form, 'titulo': 'Crear Nuevo Cliente'})


@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {cliente.nombre} actualizado.')
            return redirect('lista_clientes')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'tickets/form_cliente.html', {'form': form, 'cliente': cliente, 'titulo': f'Editar Cliente: {cliente.nombre}'})


@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if cliente.tickets.exists():
        messages.error(request, f'No se puede eliminar {cliente.nombre}, tiene tickets asociados.')
        return redirect('lista_clientes')
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente {cliente.nombre} eliminado.')
        return redirect('lista_clientes')
    
    return render(request, 'tickets/eliminar_cliente.html', {'cliente': cliente})


@login_required
def informes(request):
    total_tickets = Ticket.objects.count()
    tickets_por_estado = Ticket.objects.values('estado').annotate(total=Count('id'))
    tickets_por_prioridad = Ticket.objects.values('prioridad').annotate(total=Count('id'))
    tickets_por_tecnico = Ticket.objects.filter(tecnico_asignado__isnull=False).values('tecnico_asignado__username').annotate(total=Count('id')).order_by('-total')
    
    tickets_resueltos = Ticket.objects.filter(fecha_resolucion__isnull=False)
    tiempos = [t.tiempo_resolucion() for t in tickets_resueltos if t.tiempo_resolucion()]
    tiempo_promedio = sum(tiempos)/len(tiempos) if tiempos else 0
    
    hace_30_dias = timezone.now() - timedelta(days=30)
    tickets_ultimo_mes = Ticket.objects.filter(fecha_creacion__gte=hace_30_dias).count()
    
    top_clientes = Cliente.objects.annotate(num_tickets=Count('tickets')).order_by('-num_tickets')[:10]
    
    context = {
        'total_tickets': total_tickets,
        'tickets_por_estado': tickets_por_estado,
        'tickets_por_prioridad': tickets_por_prioridad,
        'tickets_por_tecnico': tickets_por_tecnico,
        'tiempo_promedio': round(tiempo_promedio, 2),
        'tickets_ultimo_mes': tickets_ultimo_mes,
        'top_clientes': top_clientes,
    }
    
    return render(request, 'tickets/informes.html', context)
