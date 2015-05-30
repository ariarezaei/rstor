from django import forms
from monitor.views import cache_list
from manageCaches.views import disks

MODE_CHOICES = (
        ("wb", "wb"),
        ("wt", "wt"),
        ("ro", "ro")
    )

PODE_CHOICES = (
        ("smart", "smart"),
        ("rand", "rand"),
        ("fifo", "fifo"),
        ("lru", "lru")
    )
BODE_CHOICES= (
        ("2048", "2048"),
        ("4096", "4096"),
        ("8192", "8192")
)

CACHES = cache_list()

FIELD_ATTR = 'form-control cache-input'


class CacheForm(forms.Form):
    error_css_class = 'text-danger'

    name = forms.CharField(label='Cache Name', max_length=30, required=True,
                           error_messages={"required": "Please enter the cache name."},
                           widget=forms.TextInput(attrs={'class': FIELD_ATTR}),)
    mode = forms.ChoiceField(label="Mode",
        choices=MODE_CHOICES,
        initial='',
        widget=forms.Select(attrs={'class': FIELD_ATTR}),
        required=False
    )
    block_size = forms.ChoiceField(label="Block Size",
        choices=BODE_CHOICES,
        initial='',
        widget=forms.Select(attrs={'class': FIELD_ATTR}),
        required=False
    )
    eviction = forms.ChoiceField(label="Eviction",
        choices=PODE_CHOICES,
        initial='',
        widget=forms.Select(attrs={'class': FIELD_ATTR}),
        required=False
    )
    ssd = forms.ChoiceField(label="SSD",
        choices=disks(),
        initial='',
        widget=forms.Select(attrs={'class': FIELD_ATTR}),
        required=True
    )
    hdd = forms.ChoiceField(label="SRC",
        choices=disks(),
        initial='',
        widget=forms.Select(attrs={'class': FIELD_ATTR}),
        required=True
    )