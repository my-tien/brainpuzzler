---

---

/* skel-baseline v2.0.3 | (c) n33 | getskel.com | MIT licensed */

(function($) {

	skel.init({
		reset: 'full',
		breakpoints: {
			global: {
				href: '{{ "/css/style.css" | prepend: site.baseurl }}',
				containers: 1400,
				grid: { gutters: ['2em', 0] }
			},
			xlarge: {
				media: '(max-width: 1680px)',
				href: '{{ "/css/style-xlarge.css" | prepend: site.baseurl }}',
				containers: 1200
			},
			large: {
				media: '(max-width: 1280px)',
				href: '{{ "/css/style-large.css" | prepend: site.baseurl }}',
				containers: 960,
				grid: { gutters: ['1.5em', 0] },
				viewport: { scalable: false }
			},
			medium: {
				media: '(max-width: 980px)',
				href: '{{ "/css/style-medium.css" | prepend: site.baseurl }}',
				containers: '90%'
			},
			small: {
				media: '(max-width: 736px)',
				href: '{{ "/css/style-small.css" | prepend: site.baseurl }}',
				containers: '90%',
				grid: { gutters: ['1.25em', 0] }
			},
			xsmall: {
				media: '(max-width: 480px)',
				href: '{{ "/css/style-xsmall.css" | prepend: site.baseurl }}'
			}
		},
		// plugins: {
		// 	layers: {
		// 		config: {
		// 			mode: 'transform'
		// 		},
		// 		navPanel: {
		// 			animation: 'pushX',
		// 			breakpoints: 'medium',
		// 			clickToHide: true,
		// 			height: '100%',
		// 			hidden: true,
		// 			html: '<div data-action="moveElement" data-args="nav"></div>',
		// 			orientation: 'vertical',
		// 			position: 'top-left',
		// 			side: 'left',
		// 			width: 250
		// 		},
		// 		navButton: {
		// 			breakpoints: 'medium',
		// 			height: '4em',
		// 			html: '<span class="toggle" data-action="toggleLayer" data-args="navPanel"></span>',
		// 			position: 'top-left',
		// 			side: 'top',
		// 			width: '6em'
		// 		}
		// 	}
		// }
	});

	$(function() {

		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				$body.removeClass('is-loading');
			});



        var foo = $('#gallery--video');
        foo.poptrox();


        if( $('#menu_show').length > 0 ) {
            $('#menu_show').click(function() {
                "use strict";
                $(this).toggleClass('active');
                var $feed    = $('#cover--right'),
                    $content = $('#content');

                if( !$feed.hasClass('hidden') ) {
                    $feed.addClass('hidden');
                    $content.addClass('visible');
                    steps_show('#about');

                } else {
                    $content.removeClass('visible');
                    $feed.removeClass('hidden').addClass('anim');
                }
                return false;
            });
        }

        if( $('#nav').length > 0 ) {
            $('#nav li a').click(function() {
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

        if( $('#background-slideshow').length > 0 ) {
        $('#background-slideshow').kenburnsy({
            fullscreen: true
        });
    }


    });
})(jQuery);


$(window).load(function(){
    if( $('#countdown-block').length > 0 ) {
        vertAlign( $('#countdown-block') );
    }
});





/* Vertical Alignment */
function vertAlign(elem) {
    var height = elem.outerHeight();

    elem.css({'marginTop' : -height/2}).fadeIn().addClass('inited');
}

/* Show steps */
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