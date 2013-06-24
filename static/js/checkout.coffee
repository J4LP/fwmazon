
$ = jQuery

class Shipping
    constructor: ->
        @_volume = $('span#js-volume').data('volume')
        @init_events()
        @update_shipping()
    
    init_events: ->
        $('body').on('change', 'select#shipping', @update_shipping)

    update_shipping: (e) =>
        $option = $('select#shipping').children(':selected')
        cost = parseFloat($option.data('cost'))
        delay = parseFloat($option.data('delay'))
        total_shipping = (cost * @_volume)
        $('span#js-shipping-cost').text(to_comma(total_shipping)).data('cost', total_shipping)
        $('body').trigger('cost_update')

window.show_error = (message) ->
    id = Math.floor(Math.random() * 100)
    $('#messages').append("<div class=\"alert alert-danger\" id=\"message-#{id}\">#{message}</div>")
    setTimeout () ->
        hide_message(id)
    , 5000

window.hide_message = (id) ->
    $("#messages #message-#{id}").remove()

window.to_comma = (int) ->
        return int.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")

class CostUpdater
    constructor: ->
        @fitting = $('span#js-fitting-price').data('price')
        $('body').on('cost_update', @update_price)
        $('body').on('change', 'input#fitting', @update_price)

    update_price: =>
        @collect_prices()
        $('span#js-review-shipping').text(to_comma(@prices.shipping))
        $('span#js-review-options').text(to_comma(@prices.options))
        $('span#js-review-tax').text(to_comma(@prices.tax))
        $('span#js-review-total').text(to_comma(@prices.total))

    collect_prices: ->
        @prices.sub_total = parseFloat($('span#js-review-subtotal').data('subtotal'))
        @prices.shipping = parseFloat($('span#js-shipping-cost').data('cost'))
        if $('input#fitting').prop('checked')
            @prices.options = @fitting
        else
            @prices.options = 0.0
        @prices.tax = (@prices.sub_total + @prices.shipping + @prices.options) * 0.05
        @prices.total = @prices.sub_total + @prices.shipping + @prices.options + @prices.tax

    prices: {
        'sub_total': 0.0
        'shipping': 0.0
        'options': 0.0
        'tax': 0.0
        'total': 0.0
    }


$(document).on 'ready', ->
    window.cost_updater = new CostUpdater()
    window.shipping = new Shipping()