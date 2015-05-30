from django import forms
from monitor.views import cache_list, disks

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


class CacheForm(forms.Form):
    error_css_class = 'text-danger'

    name = forms.CharField(label='Cache Name', max_length=30, required=True,
                           name="Cache Name",
                           error_message={"required": "Please enter the cache name."})
    mode = forms.ChoiceField(label="mode",
        choices=MODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False,
        label="Mode"
    )
    block_size = forms.ChoiceField(label="block size",
        choices=BODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False
    )
    eviction = forms.ChoiceField(label="eviction",
        choices=PODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False
    )
    ssd = forms.ChoiceField(label="ssd",
        choices=disks(),
        initial='',
        widget=forms.Select(),
        required=True
    )
    hdd = forms.ChoiceField(label="src",
        choices=disks(),
        initial='',
        widget=forms.Select(),
        required=True
    )