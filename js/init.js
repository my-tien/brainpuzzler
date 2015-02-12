---

---

/* skel-baseline v2.0.3 | (c) n33 | getskel.com | MIT licensed */

(function($) {

	skel.init({
		reset: 'full',
		breakpoints: {
			global:		{ range: '*', href: '{{ "/css/style.css" | prepend: site.baseurl }}', containers: 1400, grid: { gutters: 50 } },
			wide:		{ range: '-1680', href: '{{ "/css/style-wide.css | prepend: site.baseurl }}', containers: 1200, grid: { gutters: 40 } },
			normal:		{ range: '-1280', href: '{{ "/css/style-normal.css | prepend: site.baseurl }}', containers: 960, grid: { gutters: 30 }, viewport: { scalable: false } },
			narrow:		{ range: '-980', href: '{{ "/css/style-narrow.css | prepend: site.baseurl }}', containers: '95%' },
			narrower:	{ range: '-840', href: '{{ "/css/style-narrower.css | prepend: site.baseurl }}', containers: '95%!'},
			mobile:		{ range: '-736', href: '{{ "/css/style-mobile.css | prepend: site.baseurl }}', containers: '90%!', grid: { gutters: 20 } },
			mobilep:	{ range: '-480', href: '{{ "/css/style-mobilep.css | prepend: site.baseurl }}', containers: '100%' }
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
                var $feed    = $('#banner__right'),
                    $content = $('#banner__outside');

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

        // if( $('#background-slideshow').length > 0 ) {
        //     $('#background-slideshow').kenburnsy({
        //         fullscreen: true
        //     });
        // }
    });
})(jQuery);


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