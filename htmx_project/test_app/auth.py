from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class KeycloakOIDCBackend(OIDCAuthenticationBackend):
    def get_username(self, claims):
        """Use email as username"""
        return claims.get("email", claims.get("preferred_username"))

    def create_user(self, claims):
        """Customize user creation"""
        user = super().create_user(claims)
        self.update_roles(user, claims)
        return user

    def update_user(self, user, claims):
        """Update user data on login"""
        self.update_roles(user, claims)
        return super().update_user(user, claims)

    def update_roles(self, user, claims):
        """Extract roles from Keycloak's resource_access"""
        resource_access = claims.get("resource_access", {})
        app_roles = resource_access.get("my-backend-app", {}).get("roles", [])

        # Example: Assign Django groups based on Keycloak roles
        from django.contrib.auth.models import Group
        for role in app_roles:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        user.save()


# class KeycloakOIDCBackend(OIDCAuthenticationBackend):
#     def filter_users_by_claims(self, claims):
#         print("Received claims:", claims)  # Debugging
#         return super().filter_users_by_claims(claims)