from .balance_data import *


def balance_context(request):
    # Function to make global context
    if request.user.is_authenticated:
        if balance(request.user) > 0:
            balance_color = 'green'
        else:
            balance_color = 'red'

        return {'global_balance': balance(request.user),
                'global_contribution': all_contributions(request.user),
                'global_expences': all_expences(request.user),
                'balance_color': balance_color
                }
    else:
        return {'global_balance': '',
                'global_contribution': '',
                'global_expences': ''
                }
