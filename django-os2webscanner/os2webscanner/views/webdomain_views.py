from ..models.domain_model import Domain
from ..models.webdomain_model import WebDomain
from ..validate import get_validation_str
from .domain_views import DomainList, DomainCreate, DomainUpdate
from .views import RestrictedDeleteView


class WebDomainList(DomainList):

    """Displays list of domains."""

    model = WebDomain
    type = 'web'


class WebDomainCreate(DomainCreate):

    """Web domain create form."""

    model = WebDomain
    fields = ['url', 'exclusion_rules', 'download_sitemap', 'sitemap_url',
              'sitemap']

    def get_success_url(self):
        """The URL to redirect to after successful creation."""
        return '/webdomains/%s/created/' % self.object.pk


class WebDomainUpdate(DomainUpdate):
    """Update a web domain view."""

    model = WebDomain
    fields = ['url', 'exclusion_rules', 'download_sitemap',
              'sitemap_url', 'sitemap']

    def get_context_data(self, **kwargs):
        """Get the context used when rendering the template."""
        context = super().get_context_data(**kwargs)
        for value, desc in WebDomain.validation_method_choices:
            key = 'valid_txt_' + str(value)
            context[key] = get_validation_str(self.object, value)
        return context

    def get_success_url(self):
        """The URL to redirect to after successful updating.

        Will redirect the user to the validate view if the form was submitted
        with the 'save_and_validate' button.
        """
        if 'save_and_validate' in self.request.POST:
            return 'validate/'
        else:
            return '/webdomains/%s/saved/' % self.object.pk


class WebDomainDelete(RestrictedDeleteView):

    """Delete a domain view."""

    model = Domain
    success_url = '/webdomains/'