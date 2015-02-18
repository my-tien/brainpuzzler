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
})(jQuery);