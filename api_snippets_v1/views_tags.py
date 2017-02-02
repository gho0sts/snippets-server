from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Tag, TagSnippetRelation
from .serializers import TagSerializer, TagSnippetRelationWriteSerializer


class TagList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Tag.objects \
            .filter(owner__pk=self.request.user.pk)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagSnippetRelationCreateView(generics.CreateAPIView):
    """
    Creates a new TagSnippetRelation from the request.
    Request should contain only the IDs of the associated objects, like:
    {
        _tag: 35,
        _snippet: 40
    }
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSnippetRelationWriteSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override of default create() method to provide a different Response body
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # modify the contents of the response body to match
        # what the client expects
        tag_id = serializer.data.get('_tag')
        res_data = {
            'id': tag_id,
            '_tag': str(Tag.objects.get(pk=tag_id))
        }
        return Response(res_data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class TagSnippetRelationDeleteView(generics.GenericAPIView):
    """
    Concrete view for deleting a TagSnippetRelation instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TagSnippetRelation.objects\
            .filter(owner__pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        try:
            # find the Snippet that matches owner/tag/snippet ids
            tag_id = request.data.get('tag_id')
            snippet_id = request.data.get('snippet_id')
            instance = TagSnippetRelation.objects.filter(
                owner__pk=request.user.pk,
                _tag__pk=tag_id,
                _snippet__pk=snippet_id).get()
            instance.delete()
        except TagSnippetRelation.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
