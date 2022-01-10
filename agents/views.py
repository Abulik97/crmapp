from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from.forms import AgentModelForm
from.mixins import OrganisorandLoginRequiredMixin
from django.core.mail import send_mail
import random

# Create your views here.
class AgentListView(OrganisorandLoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorandLoginRequiredMixin,generic.CreateView):
    template_name='agents/agent_create.html'
    form_class=AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')

    def form_valid(self, form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(user=user,organisation=self.request.user.userprofile)
        send_mail(subject="Your re invited to be agent",message="Agent olaraq elave edilmisiniz,baslamax ucun site daxil olarax qyeidytanda kecin",
        from_email="admintest@mail.com",recepient_list=[user.email])
       
        return super(AgentCreateView,self).form_valid(form) 



class AgentDetailView(OrganisorandLoginRequiredMixin,generic.DetailView):
    template_name='agents/agent_detail.html'
    context_object_name='agent'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)




class AgentUpdateView(OrganisorandLoginRequiredMixin,generic.UpdateView):
    template_name='agents/agent_update.html'
    form_class=AgentModelForm
    def get_queryset(self):
        return Agent.objects.all()

    def get_success_url(self):
        return reverse('agents:agent_list')


class AgentDeleteView(OrganisorandLoginRequiredMixin,generic.DeleteView):
    template_name='agents/agent_delete.html'
    context_object_name='agent'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    def get_success_url(self):
        return reverse('agents:agent_list')          

    



