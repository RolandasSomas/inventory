from contextlib import nullcontext

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic


from .forms import ItemForm, ItemForm, LocationForm, CategoryForm, ItemsForm
from .models import Item, Location, ItemAction, ItemCategory, ItemType
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')


class ItemsListView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'items/list.html'
    context_object_name = "items"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ItemForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ItemForm(self.request.GET)

        # del 0 objektu stock lenteleje nerodymo
        # queryset = Item.objects.exclude(quantity=0)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            location = form.cleaned_data.get('location')
            if name:
                queryset = queryset.filter(item_type=name)
            if location:
                queryset = queryset.filter(location=location)
        return queryset
    # Filter


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    context_object_name = "item"
    template_name = 'items/view.html'

    def get_context_data(self, **kwargs):
        # Pass the article or article_id to the template context
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('pk')
        context['item_actions'] = ItemAction.objects.filter(item=item_id)
        return context




class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = Item
    fields = ['item_type', 'quantity', 'location', 'from_location']
    success_url = '/items'
    template_name = 'items/create.html'

    def form_valid(self, form):
        exist = Item.objects.filter(location=form.instance.location, item_type=form.instance.item_type)
        if exist:
            form.add_error(None, "Item already exist in that location")
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Item
    fields = ['item_type', 'quantity', 'location', 'from_location']
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


class LocationListView(LoginRequiredMixin, generic.ListView):
    model = Location
    template_name = 'location/list.html'
    context_object_name = "locations"
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = LocationForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = LocationForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            location = form.cleaned_data.get('location')
            if name:
                queryset = queryset.filter(name=name)
            if location:
                queryset = queryset.filter(address=location)
        return queryset


class LocationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Location
    context_object_name = "location"
    template_name = 'location/view.html'


class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    fields = ['name', 'address']
    success_url = '/locations'
    template_name = 'location/create.html'

    def form_valid(self, form):
        return super().form_valid(form)

class LocationEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Location
    fields = ['name', 'address']
    success_url = '/locations'
    template_name = 'location/edit.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return True


class LocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Location
    success_url = '/locations'
    template_name = 'location/delete.html'

    def test_func(self):
        return True


class ItemActionCreateView(LoginRequiredMixin, generic.CreateView):
    model = ItemAction
    fields = ['action', 'amount', 'move_to', "from_location"]
    template_name = 'item_action/change_amount.html'

    def get_context_data(self, **kwargs):
        # Pass the article or article_id to the template context
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('pk')
        context['item'] = Item.objects.get(id=item_id)
        context['title'] = "Change amount"
        return context

    def form_valid(self, form, **kwargs):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('items:view_item', kwargs={'pk': self.kwargs.get('pk')})

class ItemActionAddCreateView(ItemActionCreateView):
    fields = ['amount', "from_location"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add amount"
        return context

    def form_valid(self, form, **kwargs):
        item_id = self.kwargs.get('pk')
        item = Item.objects.get(id=item_id)
        form.instance.item = item
        form.instance.created_by = self.request.user
        form.instance.action = 1
        valid = super().form_valid(form)
        if valid:
            item.quantity = item.quantity + form.instance.amount
            item.save()
        return valid

class ItemActionMoveCreateView(ItemActionCreateView):
    fields = ['amount', 'move_to']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Move amount"
        return context

    def form_valid(self, form, **kwargs):
        item_id = self.kwargs.get('pk')
        item = Item.objects.get(id=item_id)
        form.instance.item = item
        form.instance.action = 3
        form.instance.reason = "Moved to " + form.instance.move_to.address + " location"
        # form.instance.from_location = item.location.address
        if form.instance.amount > item.quantity:
            form.add_error('amount', "Can not remove more items when it is in storage")
            return self.form_invalid(form)
        valid = super().form_valid(form)
        if valid:
            move_to = form.instance.move_to
            item.quantity = item.quantity - form.instance.amount
            item.save()

            try:
                new_item = Item.objects.get(location=move_to, item_type=item.item_type)
                new_item.quantity += form.instance.amount
            except ObjectDoesNotExist:
                new_item = item
                new_item.id = None
                new_item.location = move_to
                new_item.quantity = form.instance.amount

            new_item.save()
            nia = ItemAction()
            nia.item = new_item
            nia.move_to = None
            nia.amount = form.instance.amount
            nia.from_location = item.location.address
            nia.action = 3
            nia.created_by = self.request.user
            nia.reason = "Moved from " + item.location.address + " location"
            nia.save()

        return valid


class ItemActionRemoveCreateView(ItemActionCreateView):
    fields = ['amount', 'reason']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Remove amount"
        return context

    def form_valid(self, form, **kwargs):
        item_id = self.kwargs.get('pk')
        item = Item.objects.get(id=item_id)
        form.instance.item = item
        form.instance.action = 2
        form.instance.created_by = self.request.user
        if form.instance.amount > item.quantity:
            form.add_error('amount', "Can not remove more items when it is in storage")
            return self.form_invalid(form)
        valid = super().form_valid(form)
        if valid:
            item.quantity = item.quantity - form.instance.amount
            item.save()
        return valid


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = ItemCategory
    template_name = 'category/list.html'
    context_object_name = "categories"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CategoryForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CategoryForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            if title:
                queryset = queryset.filter(title=title)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = ItemCategory
    context_object_name = "category"
    template_name = 'category/view.html'


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = ItemCategory
    fields = ['title']
    success_url = '/categories'
    template_name = 'category/create.html'

    def form_valid(self, form):
        return super().form_valid(form)

class CategoryEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = ItemCategory
    fields = ['title']
    success_url = '/categories'
    context_object_name = "category"

    template_name = 'category/edit.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return True


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = ItemCategory
    context_object_name = "category"

    success_url = '/categories'
    template_name = 'category/delete.html'

    def form_valid(self, form):
        parent = self.get_object()
        if parent.category.exists():
            messages.error(self.request, "Cannot be deleted, because you have related data on it.")
            return self.form_invalid(form)
        return super().form_valid(form)
    def test_func(self):
        return True



class ItemTypeListView(LoginRequiredMixin, generic.ListView):
    model = ItemType
    template_name = 'item_type/list.html'
    context_object_name = "item_types"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ItemsForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ItemsForm(self.request.GET)
        if form.is_valid():
            id_number = form.cleaned_data.get('serial_number')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            if id_number:
                queryset = queryset.filter(id_number=id_number)
            if title:
                queryset = queryset.filter(title=title)
            if category:
                queryset = queryset.filter(category=category)
        return queryset

class ItemTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = ItemType
    context_object_name = "item_type"
    template_name = 'item_type/view.html'


class ItemTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = ItemType
    fields = ['title', 'id_number', 'price', 'quantity_type', 'category']
    success_url = '/item_types'
    template_name = 'item_type/create.html'

    def form_valid(self, form):
        item_code = form.instance.id_number
        if item_code:
            try:
                item_type = ItemType.objects.get(id_number=item_code)
            except ObjectDoesNotExist:
                item_type = None
            if item_type:
                form.add_error('id_number', "Item code already exists")
                return self.form_invalid(form)
        return super().form_valid(form)

class ItemTypeEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = ItemType
    fields = ['title', 'id_number', 'price', 'quantity_type', 'category']
    success_url = '/item_types'
    context_object_name = "item_type"

    template_name = 'item_type/edit.html'

    def form_valid(self, form):
        item_code = form.instance.id_number
        if item_code:
            try:
                item_type = ItemType.objects.get(id_number=item_code)
            except ObjectDoesNotExist:
                item_type = None
            if item_type and item_type.id != form.instance.id:
                form.add_error('id_number', "Item code already exists")
                return self.form_invalid(form)
        return super().form_valid(form)

    def test_func(self):
        return True


class ItemTypeDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = ItemType
    context_object_name = "item_type"

    success_url = '/item_types'
    template_name = 'item_type/delete.html'

    def form_valid(self, form):
        parent = self.get_object()
        if parent.item_name.exists():
            messages.error(self.request, "Cannot be deleted, because you have related data on it.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def test_func(self):
        return True