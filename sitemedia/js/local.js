$.widget("custom.categorycomplete", $.ui.autocomplete, {
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
    _renderItem: function( ul, item ) {
        if (! item.desc) {
            item.desc = '';
        }
        return $('<li></li>')
            .data('ui-autocomplete-item', item)
            .append('<a>' + item.label + '<span>' + item.desc + '</span></a>')
            .appendTo(ul);

    }
});

$(document).ready(function(){
   $(".access li[data-toggle='tooltip']").tooltip();

   // whenever a form is submitted, disable submit inputs and buttons
   // to avoid double-clicks
   // NOTE: custom js validation methods must now re-enable
   // submit buttons when validation fails
   $("form").on("submit", function(event) {
      $(this).find(":submit").attr("disabled", true)
   });

});
