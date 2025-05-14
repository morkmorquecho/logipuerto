# custom_tags.py
from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()

#Renderiza los mensajes de django en un formato bootstrap
@register.simple_tag(takes_context=True)
def RenderMensajesDjango(context):
    messages = context.get('messages')
    if not messages:
        return ''
    
    html = ['<div class="mt-3">']
    for message in messages:
        tag = 'danger' if message.tags == 'error' else message.tags
        alert_html = f'''
            <div class="alert alert-{tag} text-uppercase" role="alert">
                {message}
            </div>
        '''
        html.append(alert_html)
    html.append('</div>')

    return mark_safe(''.join(html))

#Renderiza sweet alerts para los mensajes de django
@register.simple_tag(takes_context=True)
def RenderMensajesSweetAlert(context):
    messages = context.get('messages')
    if not messages:
        return ''
    
    mensajes = [
        {
            'tags': m.tags,
            'text': str(m)
        } for m in messages
    ]
    js = f"""
    <script>
        const django_messages = {json.dumps(mensajes)};
        console.log(django_messages);
    </script>
    """
    return mark_safe(js)

#Te permite hacer focus en el campo indicado
@register.simple_tag
def CampoAutoFocus(field_id, when=True):
    if not when:
        return ''
    
    html = f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const field = document.getElementById('{field_id}');
            if (field) {{
                field.focus();
            }}
        }});
    </script>
    """
    return mark_safe(html)