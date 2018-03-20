from rest_framework.renderers import JSONRenderer


class ChatterRenderer(JSONRenderer):
    """
    Renderer which serializes to custom json.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status = False

        if renderer_context is not None:
            response = renderer_context['response']

            if 200 <= response.status_code <= 299:
                status = True

            data['status_code'] = response.status_code

        data['success'] = status
        return super(ChatterRenderer, self).render(data, accepted_media_type, renderer_context)
