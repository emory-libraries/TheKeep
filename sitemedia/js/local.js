$(document).ready(function () {
    $("a.tip[title]").tooltip({'position': 'bottom center'});
});


$.widget( "custom.categorycomplete", $.ui.autocomplete, {
    _renderMenu: function( ul, items ) {
	var self = this,
	currentCategory = "";
	$.each( items, function( index, item ) {
	    if (item.category && item.category != currentCategory) {
		ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
		currentCategory = item.category;
	    }
	    self._renderItem( ul, item );
	});
    },
    _renderItem: function(ul, item) {
        if (! item.desc) {
            item.desc = '';
        }
        return $('<li></li>')
            .data('item.autocomplete', item)
            .append('<a>' + item.label + '<span>' + item.desc + '</span></a>')
            .appendTo(ul);
    },
});