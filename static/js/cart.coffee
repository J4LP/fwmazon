
$ = jQuery

class Cart
    constructor: ->
        @get_cookie()
        @init_ajax()
        @init_events()

    get_cookie: ->
        @csrftoken = $.cookie('csrftoken')

    csrf_safe_method: (method) ->
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

    init_ajax: ->
        $.ajaxSetup
            crossDomain: false
            beforeSend: (xhr, settings) =>
                if !@csrf_safe_method(settings.type)
                    xhr.setRequestHeader 'X-CSRFToken', @csrftoken
    
    init_events: ->
        $('body').on('click', 'a#add-to-cart', @add)
        $('body').on('click', 'a#update-cart', @update)
        $('body').on('click', 'a#delete-from-cart', @delete)

    # Those three functions could probably be made into one

    add: (e) ->
        e.preventDefault()
        id = $(@).data('id')
        type = $(@).data('type')
        amount = $("input[data-id=#{id}][data-type=#{type}]").val()
        if amount == 0 or amount < 0
            return
        req = $.ajax
            url: '/shop/cart/add',
            type: 'POST',
            data: {'item_id': id, 'item_type': type, 'amount': amount}
        req.done (data) ->
            window.location.reload()
        req.error (data) ->
            show_error('An error occured while updating the shopping cart, please try again')

    update: (e) ->
        e.preventDefault()
        id = $(@).data('id')
        type = $(@).data('type')
        amount = $("input[data-id=#{id}][data-type=#{type}]").val()
        if amount < 0
            return
        req = $.ajax
            url: '/shop/cart/update',
            type: 'POST',
            data: {'item_id': id, 'item_type': type, 'amount': amount}
        req.done (data) ->
            window.location.reload()
        req.error (data) ->
            show_error('An error occured while updating the shopping cart, please try again')


    delete: (e) ->
        e.preventDefault()
        id = $(@).data('id')
        type = $(@).data('type')
        req = $.ajax
            url: '/shop/cart/delete',
            type: 'POST',
            data: {'item_id': id, 'item_type': type}
        req.done (data) ->
            window.location.reload()
        req.error (data) ->
            show_error('An error occured while updating the shopping cart, please try again')

window.show_error = (message) ->
    id = Math.floor(Math.random() * 100)
    $('#messages').append("<div class=\"alert alert-danger\" id=\"message-#{id}\">#{message}</div>")
    setTimeout () ->
        hide_message(id)
    , 5000

window.hide_message = (id) ->
    $("#messages #message-#{id}").remove()


$(document).on 'ready', ->
    window.cart = new Cart()