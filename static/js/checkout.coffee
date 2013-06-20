
$ = jQuery

class Shipping
    constructor: ->
        @_volume = $('span#js-volume').data('volume')
        @init_events()
        @update_shipping()
    
    init_events: ->
        #$('body').on('click', 'a#add-to-cart', @add)
        $('body').on('change', 'select#shipping', @update_shipping)

    update_shipping: (e) =>
        if e
            e.preventDefault()
            $option = $(e.currentTarget).children(':selected')
        else
            $option = $('select#shipping').children(':selected')
        cost = parseFloat($option.data('cost'))
        delay = parseFloat($option.data('delay'))
        total_shipping = (cost * @_volume)
        $('span#js-shipping-cost').text(total_shipping.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")).data('cost', total_shipping)
        $('body').trigger('cost_update')

window.show_error = (message) ->
    id = Math.floor(Math.random() * 100)
    $('#messages').append("<div class=\"alert alert-danger\" id=\"message-#{id}\">#{message}</div>")
    setTimeout () ->
        hide_message(id)
    , 5000

window.hide_message = (id) ->
    $("#messages #message-#{id}").remove()


class CostUpdater
    constructor: ->
        @fitting = $('span#js-fitting-price').data('price')
        $('body').on('cost_update', @update_price)
        $('body').on('change', 'input#fitting', @update_price)

    update_price: =>
        shipping = $('span#js-shipping-cost').data('cost')
        $('span#js-review-shopping').text(@to_comma(shipping))
        if $('input#fitting').prop('checked')
            $('span#js-options-cost').text(@to_comma(@fitting))
        else
            $('span#js-options-cost').text('0')

    to_comma: (int) ->
        return int.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

$(document).on 'ready', ->
    window.cost_update = new CostUpdater()
    window.shipping = new Shipping()