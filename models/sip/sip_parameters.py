"""
.. module:: sip_parameters
   :synopsis: A useful module indeed.
"""
from django import forms
from django.utils.safestring import mark_safe
from django.core import validators
from models.forms import validation

Species_of_the_tested_bird_CHOICES=(('0','Make a selection'),('178','Northern bobwhite quail'),('1580','Mallard duck'),('1','Other'))
Species_of_the_bird_NOAEC_CHOICES=(('0','Make a selection'),('1','Northern bobwhite quail NOAEC'),('2','Mallard duck NOAEC'),('3','"Other" Bird species NOAEC'))
Species_of_the_tested_mamm_CHOICES=(('0','Make a selection'),('350','Laboratory rat'),('1','Other'))
#SELECT_RECEPTOR = (('Avian','Avian'),('Mammalian','Mammalian'),('Both','Both'))


class SipInp(forms.Form):
    chemical_name = forms.CharField(
            widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}), 
            initial='Quinoxyfen',
            required=True,
            validators=[validators.validate_slug])
    solubility = forms.FloatField(
            required=True,
            label='Solubility',
            initial=0.128,
            validators=[validation.validate_greaterthan0])
    ld50_mammal_water = forms.FloatField(
            required=True, 
            label=mark_safe('Mammalian LD<sub>50</sub> (mg/kg-bw)'), 
            initial=5000,
            validators=[validation.validate_greaterthan0])
    species_tested_mammal = forms.ChoiceField(required=True,
            label='Species of the tested mammal',
            choices=Species_of_the_tested_mamm_CHOICES,
            initial='Laboratory rat',
            validators=[validation.validate_choicefield])
    bodyweight_rat=forms.FloatField(
            required=True,
            label='Body weight of the tested mammal (g)',
            initial=350,
            validators=[validation.validate_greaterthan0])
    bodyweight_tested_mammal_other=forms.FloatField(
            required=True,
            label='Body weight of the "other" mammal (g)',
            initial=500,
            validators=[validation.validate_greaterthan0])
    bodyweight_assessed_mammal = forms.FloatField(
            required=True,
            label='Body weight of assessed mammal (g)',
            initial=1000,
            validators=[validation.validate_greaterthan0])
    NOAEL = forms.FloatField(
            required=True,
            label='Mammalian NOAEL (mg/kg-bw)',
            initial=20,
            validators=[validation.validate_positive])
    ld50_avian_water = forms.FloatField(
            required=True,
            label=mark_safe('Avian LD<sub>50</sub> (mg/kg-bw) of the tested bird'),
            initial=2292,
            validators=[validation.validate_positive])
    species_tested_bird = forms.ChoiceField(
            required=True,
            label=mark_safe('Species of the tested bird with LD<sub>50</sub> data'),
            choices=Species_of_the_tested_bird_CHOICES,
            initial='Mallard duck',
            validators=[validation.validate_choicefield])
    bodyweight_quail = forms.FloatField(
            required=True,
            label='Weight of the tested bird (g)',
            initial= 178,
            validators=[validation.validate_greaterthan0])
    bodyweight_duck = forms.FloatField(
            required=True,
            label='Weight of the tested bird (g)',
            initial=1580,
            validators=[validation.validate_greaterthan0])
    bodyweight_bird_other = forms.FloatField(
            required=True,
            label='Weight of the "other" bird (g)',
            initial= 200,
            validators=[validation.validate_greaterthan0])
    bodyweight_assessed_bird = forms.FloatField(
            required=True,
            label='Body weight of assessed bird (g)',
            initial=20,
            validators=[validation.validate_greaterthan0])
    mineau_scaling_factor = forms.FloatField(
            required=True,
            label='Mineau scaling factor',
            initial=1.15,
            validators=[validation.validate_greaterthanequalto1])
    
    # NOAEC = forms.ChoiceField(required=True,label='Species with NOAEC value', choices=Species_of_the_bird_NOAEC_CHOICES, initial='Make a selection')

    NOAEC_species = forms.ChoiceField(
            required=True,
            label=mark_safe('Species of the tested bird with NOAEC data'),
            choices=Species_of_the_bird_NOAEC_CHOICES,
            initial='Mallard duck NOAEC',
            validators=[validation.validate_choicefield])
    NOAEC_d = forms.FloatField(
            required=True,
            label='Mallard duck NOAEC (mg/kg-diet)',
            initial=465,
            validators=[validation.validate_positive])
    NOAEC_q = forms.FloatField(
            required=True,
            label='Northern bobwhite quail NOAEC (mg/kg-diet)',
            initial=435,
            validators=[validation.validate_positive])
    NOAEC_o = forms.FloatField(
            required=True,
            label='"Other" Bird species NOAEC (mg/kg-diet)',
            initial=0,
            validators=[validation.validate_positive])
    # NOAEC_o2 = forms.FloatField(required=True, label=mark_safe('"2<sup>nd</sup> Other" Bird species NOAEC (mg/kg-diet)'), initial=0)

#  select_receptor = forms.ChoiceField(required=True, choices=SELECT_RECEPTOR, initial='Both')
#  body_weight_of_bird = forms.FloatField(required=True, label='Body weight of bird (kg)', initial='4')
#  body_weight_of_mammal = forms.FloatField(required=True,label='Body weight of mammal (kg)', initial='5')
#  bodyweight_tested_bird = forms.FloatField(required=True, label='Body weight of assessed bird (g)', initial='8')
#  body_weight_of_the_assessed_mammal = forms.FloatField(required=True, label='Body weight of assessed mammal (kg)', initial='5')