from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name="register"),
    path('logout_user', views.logout_user, name="logout_user"),

    path(r'', views.index, name='index'),
    path(r'account/<slug:account_id>/balance', views.get_balance, name='get_balance'),
    path(r'account/<slug:account_id>/balance/confirm/',
         views.deposit_balance, name='deposit_balance'),

    path(r'bet/finished', views.show_finished, name='show_finished'),
    path(r'<slug:account_id>/<slug:fixture_id>/confirm/',
         views.make_bet, name='make_bet'),
    path(r'<slug:account_id>/<slug:fixture_id>',
         views.go_bet, name='go_bet'),

    path(r'account/<slug:account_id>/bets', views.account_bets, name='account_bets'),

    path(r'admin/bet/add/', views.add_bet_admin, name='add_bet_admin'),
    path(r'admin/bet/delete/<slug:bet_id>', views.admin_delete_bet, name='admin_delete_bet'),
    path(r'admin/edit/bet/<slug:bet_id>', views.admin_edit_bet, name='admin_edit_bet'),
    path(r'admin/edit/bet/<slug:bet_id>/confirm/', views.admin_edit_bet_confirm, name='admin_edit_bet_confirm'),

]