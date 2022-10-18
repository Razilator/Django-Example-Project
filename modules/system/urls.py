from django.urls import path

from modules.system.views import ProfileView, ProfileEditView, RegisterCreateView, UserLoginView, \
    UserPasswordChangeView, UserForgotPasswordView, UserPasswordResetConfirmView, UserLogoutView, ActivateAccountView, \
    FeedbackCreateView, ProfileFollowingCreateView

urlpatterns = [
    path('user/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('user/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('user/<str:slug>/follow/', ProfileFollowingCreateView.as_view(), name='follow-to-user'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password-reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create-view'),
]
