$(document).ready(function() {
    // move to the first form element for user convenience
    document.edit_form.elements[1].focus();

    // make .toggle headers hide/show the following section
    $(".toggle").click(function () {
        var header = $(this);
        header.toggleClass('collapsed');
        header.next().toggle();
    });

    /* Toggle help-text warning based on checkbox value for items with class checkbox-warning.
       (Currently used by Rights block external access field).
    */
    $('.checkbox-warning').change(function() {
       $(this).siblings('.help-block').find('span').toggleClass('text-danger', $(this).is(':checked'));
   });
    /* trigger change once manually so initial display will reflect field starting value */
    $('.checkbox-warning').change();

});
