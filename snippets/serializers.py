from rest_framework import serializers
from accounts.views import User
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from accounts.serializers import UserSerializer

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    class Meta:
        model = Snippet
        fields = ['url', 'title', 'code', 'linenos', 'language', 'highlight', 'style', 'owner']