"""
.. module:: insect_input
   :synopsis: A useful module indeed.
"""

from django.template.loader import render_to_string


def insectInputPage(request, model='', header='', formData=None):
    import insect_parameters

    html = render_to_string('04uberinput_jquery.html', { 'model': model })
    html = html + render_to_string('04uberinput_start.html', {
            'model':model, 
            'model_attributes': header+' Inputs'})
    html = html + render_to_string('insect_ubertool_config_input.html', {})
    # if formData == None:
    #     html = html + str(insect_parameters.InsectInp())
    # else:
    #     html = html + str(insect_parameters.InsectInp(formData))
    html = html + str(insect_parameters.InsectInp(formData))
    html = html + render_to_string('04uberinput_end.html', {'sub_title': 'Submit'})
    html = html + render_to_string('insect_ubertool_config.html', {})
    # Check if tooltips dictionary exists
    try:
        import insect_tooltips
        hasattr(insect_tooltips, 'tooltips')
        tooltips = insect_tooltips.tooltips
    except:
        tooltips = {}
    html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})    

    return html