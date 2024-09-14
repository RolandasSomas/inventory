from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .forms import ItemForm
from .models import Item



def home(request):
    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')


# def get_item(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     context = {'item': item, 'pk': pk}
#     return render(request, 'items/view.html', context)
#
#
# def create_item(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             item = Item(
#                 title=data['title'],
#                 quantity=data['quantity'],
#                 quantity_type=data['quantity_type'],
#             )
#             item.save()
#             return redirect('items:get_items_list')
#     form = ItemForm()
#     context = {
#         form: form,
#     }
#     return render(request, 'items/create.html', context)


class ItemsListView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'items/list.html'
    context_object_name = "items"
    paginate_by = 5


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    context_object_name = "item"
    template_name = 'items/view.html'


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = Item
    fields = ['title', 'quantity', 'quantity_type']
    success_url = '/items'
    template_name = 'items/create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Item
    fields = ['title', 'quantity', 'quantity_type']
    success_url = '/items'
    template_name = 'items/edit.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.created_by or self.request.user.has_perm('items.change_item')


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Item
    success_url = '/items'
    template_name = 'items/delete.html'

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.created_by or self.request.user.has_perm('items.change_item')