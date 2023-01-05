from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: # Autenticação do user
            return redirect("filme:homefilmes")
        else: # Pag padrão
            return super().get(request, *args, **kwargs) # Redireciona para a homepag

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse("filme:login")
        else:
            return reverse('filme:criarconta')

# def homepage(request): # Request --> GET(Quando você entra no site, me de as infos) - POST(Quando você preenche um form
#     # e envia para o site)
#     return render(request, "homepage.html")


# LoginRequiredMixin sempre tem que ser a primeira classe (parametros) que se passa, antes de qualquer uma, por padrão
class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list --> Lista de itens do modelo

# # URL - VIEW - HTML
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all() # Você pega todos objetos do seu banco de dados
#     context['lista_filmes'] = lista_filmes
#     return render(request, 'homefilmes.html', context)


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # object -> 1 Item do nosso filme

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # Redireciona o user para (page|url) final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # Filtrar a tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da pagina -- (object)
        # self.get_object()
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]# Caso queira pegar determinado
        # numero de filmes, você pode por um final como [0:3] para poder cortar a lista
        context["filmes_relacionados"] = filmes_relacionados

        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme


    # Editando o object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse("filme:homefilmes")


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')
