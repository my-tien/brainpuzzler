---

---

(function($) {
    $(function() {
        skel.init({
            reset: 'full',
            containers: '960px',
            breakpoints: {

                large: {
                    media: "(min-width: 1201px)",
                    containers: "1200px"
                },
                medium: {
                    media: '(min-width: 769px) and (max-width: 1200px)',
                    containers: "960px"
                },
                small: {
                    media: '(max-width: 768px)',
                    containers: "95%"
                }
            }
        });
    });
})(jQuery);