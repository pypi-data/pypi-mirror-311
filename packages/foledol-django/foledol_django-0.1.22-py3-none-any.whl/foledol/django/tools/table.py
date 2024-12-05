from django.conf import settings
from django.shortcuts import render as _render
from django.core.paginator import Paginator

from foledol.django.utils import paginate, get_param_from_get_or_request, new_context, get_action


class TableFilter:
    def __init__(self, key, label):
        self.key = key
        self.label = label


class TableButton:
    def __init__(self, label, action=None, icon=None, style=None, enabled=None, on_click=None, button_type=None):
        self.label = label
        self.action = action
        self.icon = icon
        self.style = style
        self.enabled = enabled
        self.on_click = on_click
        self.button_type = button_type


class TableButtonIcon:
    def __init__(self, icon, visible=None):
        self.icon = icon
        self.visible = visible


class TableButtonGroup:
    def __init__(self, label, items):
        self.label = label
        self.items = items


class TableButtonDivider:
    def __init__(self):
        None


class TableColumn:
    def __init__(self, key, name="", type=None, value=None, method=None, link=None, sortable=False, buttons=[]):
        self.key = key
        self.name = name
        self.type = type
        self.value = value
        self.method = method
        self.link = link
        self.sortable = sortable
        self.buttons = buttons


class Table:
    def __init__(self, model, columns, rows=None, path=None, base=None, heading=None, create=None, update=None,
                 search=False, upload=False, filters=None, buttons=None, placeholder=None, multiselect=False, extras=None, sort='date_asc'):
        self.model = model
        self.columns = columns
        self.rows = rows
        self.count = rows.count if rows else 0
        self.path = path
        self.base = base
        self.sort = sort
        self.title = None
        self.params = {}
        self.heading = heading
        self.create = create
        self.update = update
        self.search = search
        self.upload = upload
        self.filters = filters
        self.buttons = buttons
        self.template = 'table_view.html'
        self.placeholder = placeholder
        self.multiselect = multiselect
        self.extras = extras

    def sort(self, rows):
        pass

    def formatter(self, row):
        return ''


class TableView(Table):

    def all(self):
        return self.model.objects.all()

    def select(self, rows, search, order_by):
        return rows

    def handle(self, request, context, action, rows):
        return False

    def get_space(self):
        segment = self.path.split(':')
        return segment[1] if len(segment) > 1 else segment[0]

    def get_rows(self, request, context):
        space = self.get_space()
        search = get_param_from_get_or_request(request, context, space, 'search', '').strip()
        order_by = get_param_from_get_or_request(request, context, space, 'sort', self.sort)
        filter_key = get_param_from_get_or_request(request, context, space, 'filter_key', None)
        rows = self.all()
        if filter_key and self.filters and filter_key in self.filters:
            current_filter = self.filters[filter_key]
            rows = current_filter.filter(rows)
            context['filter_title'] = current_filter.title
        return self.select(rows, search, order_by)

    def render(self, request, context=new_context()):
        if context is None:
            context = new_context()
        rows = self.get_rows(request, context)
        space = self.get_space()
        self.rows = paginate(request, context, rows, space=space)
        self.count = rows.count()
        context['base'] = self.base if self.base else settings.DEFAULT_SPACE + '/base.html'
        context['title'] = self.title
        context['table'] = self

        action = get_action(request)
        context['action'] = ''
        result = self.handle(request, context, action, rows)
        if result:
            return result

        return _render(request, self.template, context)

class TablePaginator:

    def __init__(self, rows, space):
        self.rows = rows
        self.init = None
        self.prev = None
        self.next = None
        self.last = None
        self.page = 0
        self.size = 0
        self.count = 0
        self.space = space
        self.enabled = True


    def paginate(self, request, context, results, length=15):

        self.page = 1

        page_attribute = self.space + '_page'
        if page_attribute in request.POST and request.POST[page_attribute]:
            self.page = int(request.POST[page_attribute])
        else:
            full_name = self.space + '.page'
            self.page = request.session[full_name] if full_name in request.session else 1

        if isinstance(self.page, str):
            try:
                self.page = int(self.page)
            except ValueError:
                self.page = 0

        self.size = length
        size_attribute = self.space + '_size'
        if size_attribute in request.POST and request.POST[size_attribute]:
            self.size = int(request.POST[size_attribute])
        else:
            full_name = self.space + '.size'
            self.size = request.session[full_name] if full_name in request.session else length

        paginator = Paginator(results, self.size)

        self.last = paginator.num_pages
        if self.page > self.last:
            self.page = self.last

        self.init = 1
        self.prev = self.page - 1 if self.page > 1 else None
        self.next = self.page + 1 if self.page < self.last else None
        self.count = results.count()
        self.enabled = self.last > 1

        request.session[self.space + '.page'] = self.page
        request.session[self.space + '.size'] = self.size

        context[self.space + '_paginator'] = self

        return paginator.page(self.page)
