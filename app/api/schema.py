import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from .models import Followers, UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class ProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class FollowerType(DjangoObjectType):
    class Meta:
        model = Followers


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class CreateFollower(graphene.Mutation):
    id = graphene.Int()
    user_id = graphene.Field(UserType)
    followed_by_id = graphene.Field(UserType)
    followed_at = graphene.DateTime()

    class Arguments:
        user_id = graphene.Int(required=True)

    def mutate(self, info, user_id):
        user = info.context.user or None

        follower = Followers(
            user_id_id=user_id,
            followed_by_id=user
        )

        follower.save()

        return CreateFollower(
            id=follower.id,
            user_id=follower.user_id,
            followed_by_id=follower.followed_by_id,
            followed_at=follower.followed_at
        )


class EditProfile(graphene.Mutation):
    location = graphene.String()
    company = graphene.String()
    birthday = graphene.Date()
    profile = graphene.Field(ProfileType)

    class Arguments:
        location = graphene.String(required=True)
        company = graphene.String(required=True)
        birthday = graphene.Date(required=False)

    def mutate(self, info, location, company, birthday):
        user = info.context.user or None
        print(user, user.id)
        print(UserProfile.objects.all())
        profile = UserProfile.objects.get(user_id=user.id)
        profile.company = company
        profile.location = location
        profile.birthday = birthday

        profile.save()

        return EditProfile(
            company = profile.company,
            location = profile.location,
            birthday = profile.birthday
        )


class DeleteFollower(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        follower = Followers.objects.get(pk=id)
        follower.delete()
        return DeleteFollower(
            ok=True
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_follower = CreateFollower.Field()
    edit_profile = EditProfile.Field()
    delete_follower = DeleteFollower.Field()


class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(), name=graphene.String())
    all_users = graphene.List(UserType)
    follower = graphene.Field(FollowerType, user_id=graphene.Int())
    all_followers = graphene.List(FollowerType)
    all_following = graphene.List(FollowerType)
    all_profiles = graphene.List(ProfileType)

    def resolve_all_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_all_profiles(self,info, **kwargs):
        return UserProfile.objects.all()

    def resolve_all_following(self,info, **kwargs):
        return Followers.objects.filter(followed_by_id=info.context.user.id)

    def resolve_all_followers(self,info,**kwargs):
        return Followers.objects.filter(user_id=info.context.user.id)

    def resolve_user(self,info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
