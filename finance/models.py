import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from finance.utils.zarinpal import zpal_request_handler, zpal_verify_handler


class Gateway(models.Model):
    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_PARSIAN = 'PARSIAN'
    GATEWAY_FUNCTION = (
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_ZARRINPAL, _('Zarrinpal')),
        (FUNCTION_PARSIAN, _('Parsian')),
    )

    title = models.CharField(max_length=100, verbose_name=_('gateway title'))
    gateway_request_url = models.CharField(max_length=150, verbose_name=_('request url'), null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=_('verify url'), null=True, blank=True)
    gateway_code = models.CharField(max_length=12, verbose_name=_('gateway code'), choices=GATEWAY_FUNCTION)
    is_enable = models.BooleanField(_('is enable'), default=True)
    auth_data = models.TextField(verbose_name=_('auth_data'), blank=True, null=True)

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_ZARRINPAL: zpal_request_handler,
            self.FUNCTION_PARSIAN: None
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_ZARRINPAL: zpal_verify_handler,
            self.FUNCTION_PARSIAN: None
        }
        return handlers[self.gateway_code]


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_('invoice number'), default=uuid.uuid4, unique=True)
    amount = models.PositiveIntegerField(verbose_name=_('pay amount'), editable=True)
    gateway = models.ForeignKey(Gateway, related_name='payments', null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name=_('gateway'))
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid status'))
    payment_log = models.TextField(blank=True, verbose_name=_('logs'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.SET_NULL, null=True)
    authority = models.CharField(max_length=64, verbose_name=_('authority'), blank=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    def __str__(self):
        return self.invoice_number.hex

    def get_handler_data(self):
        return dict(merchant_id=self.gateway.auth_data, amount=self.amount, description="",
                    email=self.user.email, mobile=getattr(self.user, 'phone_number', None),
                    callback='http://127.0.0.1:8000/basket/verify')

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data()
            link, authority = handler(**data)
            if authority is not None:
                self.authority = authority
                self.save()
            return link

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            self.is_paid, _ = handler(**data)
            self.save()
        return self.is_paid


