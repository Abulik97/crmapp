from django.core.mail import message, send_mail 
from django.shortcuts import render,redirect
from django.views.generic.edit import UpdateView
from.models import Lead,Agent
from.forms import LeadForm,LeadModelForm
from django.views import generic
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from leads.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorandLoginRequiredMixin
from .models import Category
# Create your views here.




class SignUpView(generic.CreateView):
    template_name='registration/signup.html'
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name='landing.html'

def landing_page(request):
    return render(request,'landing.html')




class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name='leads/lead_list.html'
    context_object_name="leads"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            queryset=queryset.filter(agent__user=user)
        return queryset




def lead_list(request):
    leads=Lead.objects.all()
    return render(request,'leads/lead_list.html',context={'leads':leads})



class LeadDetailView(OrganisorandLoginRequiredMixin,generic.DetailView):
    template_name='leads/lead_detail.html'
    context_object_name="lead"
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            queryset=queryset.filter(agent__user=user)
        return queryset






def lead_detail(request,pk):
    lead=Lead.objects.get(id=pk)
    return render(request,'leads/lead_detail.html',context={'lead':lead})





class LeadCreateView(OrganisorandLoginRequiredMixin,generic.CreateView):
    template_name='leads/lead_create.html'
    form_class=LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        send_mail(
        subject="Lead ugurla yaradildi",message="Yeni Leadi gormek ucun site'i tiklayin",from_email="test@test.com",recipient_list=["test2@test2.com"]

        )
        return super(LeadCreateView,self).form_valid(form)    

def lead_create(request):
    form=LeadModelForm()
    if request.method=="POST":
        form=LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:lead_list')
            
    return render(request,'leads/lead_create.html',context={'form':form})   



class LeadUpdateView(OrganisorandLoginRequiredMixin,generic.UpdateView):
    template_name='leads/lead_update.html'
    form_class=LeadModelForm
    def get_queryset(self):
        user=self.request.user
       
    
        return Lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self):
        return reverse("leads:lead_list")



def lead_update(request,pk):
    lead=Lead.objects.get(id=pk)
    form=LeadModelForm(instance=lead)
    if request.method=="POST":
        form=LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('leads:lead_list')
    return render(request,'leads/lead_update.html',context={'form':form,'lead':lead})   




class LeadDeleteView(OrganisorandLoginRequiredMixin,generic.DeleteView):
    template_name='leads/lead_delete.html'  
    def get_queryset(self):
        user=self.request.user
       
    
        return Lead.objects.filter(organisation=user.userprofile)
 
    def get_success_url(self):
        return reverse("leads:lead_list")    

def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect('leads:lead_list')
    
  
class CategoryList(LoginRequiredMixin,generic.ListView):
    template_name="leads/category_list.html"  
    context_object_name='category'
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset


    def get_context_data(self, **kwargs):
        context=super(CategoryList,self).get_context_data(**kwargs)   
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.profile)
        else:
            queryset=Lead.objetcs.filter(organisation=user.agent.organisation)    
        context.update({"unassigned_lead_count":queryset.filter(category__isnull=True).count()})    


# def lead_create(request):
#     form=LeadForm()
#     if request.method=="POST":
#         form=LeadForm(request.POST)
#         if form.is_valid():
#             first_name=form.cleaned_data['first_name']
#             last_name=form.cleaned_data['last_name']
#             age=form.cleaned_data['age']
#             agent=Agent.objects.first()
#             Lead.objects.create(first_name=first_name,last_name=last_name,age=age,agent=agent)
#             return redirect('leads:lead_list')
            
#     return render(request,'leads/lead_create.html',context={'form':form})         
        