$(document).ready(function(){

    /*  Adds padding to body if the navbar is fixed-top
        Also, adds padding dynamically if the navbar reflows on resize
    */
    var $fixedNavbar = $('body > .navbar.navbar-fixed-top');
    if($fixedNavbar.length>0){
        var $body = $('body');

        $(document).on('ready',function(){
            addMargin($fixedNavbar.height());
        });
        $(window).resize(function(){
            addMargin($fixedNavbar.height());
        })

        function addMargin(navbar_height){
            $body.css({'margin-top': navbar_height})
        }
    }

    /* advanced search filter controls */
    function toggleGroup(elem){
        var $this = $(elem),
        group = $this.attr('data-type');

        $this.toggleClass('active');
        $(".group[data-type='"+ group +"']").stop(false,true).slideToggle(500);

    }

    var $toggleSwitch = $('.toggle.switch');
    if($toggleSwitch.length>0){
        $toggleSwitch.on('click',function(e){
            e.preventDefault();
            toggleGroup(this);
        });
    }

    $advOptionsGroup =  $(".adv.group");
    if($advOptionsGroup.length>0){
        $('.adv.group .controls .btn').bind('click', function(e){
            e.preventDefault();
            var $this = $(this);
            if($this.hasClass('submit') || $this.attr('type')=='submit'){
                search.get(this);
            }

            else if($this.hasClass('reset')){
                reset($advOptionsGroup);
            }
        });
    }

    function reset(elem){
        var $elem = $(elem),
        $inputs = $elem.find('input');
        $inputs.attr('value','').val('');
    }

    var search = {
        get: function(elem){
            $($('form .btn[type=submit]')[0]).click()
        }
    }


    /* NOTE: also requires inclusion of  eultheme/js/bootstrap-datepicker.js */
    var $dateInput = $("#date-range input");

    if($dateInput.length>0){
        $dateInput.datepicker({
            format: "yyyy",
            viewMode: "years",
            minViewMode: "years"
        });
    }

    function getCookie(name){
         var pattern = RegExp(name + "=.[^;]*")
         matched = document.cookie.match(pattern)
         if(matched){
             var cookie = matched[0].split('=')
             return cookie[1]
         }
         return false
     }

    var $ribbon = $('body>.ribbon');
    if($ribbon){
        var fadeRibbonCookie = getCookie('mFadeRibbon');
        if(fadeRibbonCookie==false){
            $ribbon.removeClass('fade');
        }
        $ribbon.on('click',function(){
            $(this).addClass('fade');
            document.cookie = "mFadeRibbon=true; expires=60; path=/";
        });
    }

});
