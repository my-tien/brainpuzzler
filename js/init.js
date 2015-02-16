---

---


(function($) {
	$(function() {
        skel.init({
          reset: 'full',
          containers: '95%',
          breakpoints: {
            medium: {
              media: '(min-width: 769px) and (max-width: 1024px)'
            },
            small: {
              media: '(max-width: 768px)'
            }
          }
        });
	});

    $(function() {
        var $window = $(window),
            $body = $('body'),
            $header = $('#header'),
            $all = $body.add($header);

        // Disable animations/transitions until the page has loaded.
            $body.addClass('is-loading');

            $window.on('load', function() {
                window.setTimeout(function() {
                    $body.removeClass('is-loading');
                }, 0);
            });


        if( $('#menu_show').length > 0 ) {
            $('#menu_show').click(function() {
                "use strict";
                $(this).toggleClass('active');
                var $right    = $('#cover__right'),
                    $outside = $('#cover__outside');

                if( !$right.hasClass('hidden') ) {
                    $right.addClass('hidden');
                    setTimeout(function() {
                        $right.css({display: 'none'});
                    }, 1400);
                    $outside.addClass('visible');
                    // $outside.css()
                    // steps_show('#about');

                } else {
                    $outside.removeClass('visible');
                    // setTimeout(function(){
                    //     $outside.removeClass('visible');
                    // }, 1000);
                    // $right.removeClass('hidden').addClass('anims');
                    $right.css({display: 'block'});
                    setTimeout(function() {
                        $right.removeClass('hidden');
                    }, 100);
                }
                return false;
            });
        }


        if( $('#nav--sub').length > 0 ) {
            $('#nav--sub li a').click(function() {
                "use strict";

                var $th          = $(this),
                    current_part = $th.attr('href');

                if( !$th.hasClass('special') ) {

                    $th.parents('ul').find('li a').removeClass('special');
                    $th.addClass('special');
                    $('.part-content').stop( true, true ).fadeOut();
                    $(current_part).stop( true, true ).fadeIn();

                    steps_show(current_part);
                }

                return false;
            });
        }


        $('#gallery--video').poptrox();


        {% if site.deploy == "true" %}
            if( $('#background-slideshow').length > 0 ) {
                $('#background-slideshow').kenburnsy({
                    fullscreen: true
                });
            }
        {% endif %}
    });
})(jQuery);


function steps_show(act) {
    if(act) {
        active_part = act;
    }

    $(active_part+ ' .anims').each( function(i, el){
        setTimeout(function(){
            $(el).addClass('visible');
        }, 100 + ( i * 100 ));
    });
}