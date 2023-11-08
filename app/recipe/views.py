from core.models import Ingredient, Recipe, Tag
from recipe import serializers
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BaseRecipeAttrViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for recipe attributes"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated User"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredient in database"""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
