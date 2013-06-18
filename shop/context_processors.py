
def cart(request):
    print('hey')
    return {'cart': request.cart}