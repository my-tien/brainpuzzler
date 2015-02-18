---

---

local jq = __js"$"
local setTimeout = __js"setTimeout"
local window = __js"window"


jq("body").addClass("is-loading")


jq(window).on("load", function()
    window.setTimeout(function()
        jq("body").removeClass("is-loading")
    end, 0)
end)


if jq("#menu_show").length >= 1 then
    print "hello"
    jq("#menu_show").click(function()
        jq("#menu_show").toggleClass("active")

        right = jq("#cover__right")
        outside = jq("#cover__outside")

        if not right.hasClass("hidden") then
            right.addClass("hidden")


            setTimeout(function()
                right.css("display", "none")
            end, 1400)

            outside.addClass("visible")

        else
            outside.removeClass("visible")
        right.css("display", "block")
        setTimeout(function()
            right.removeClass("hidden")

            end, 100)
        end

        return false

    end)
end

function steps_show(act)
    if act then
        active_part = act
    end

    jq(active_part .. " .anims").each(function(i, el)
        setTimeout(function()
            jq(el).addClass("visible")
        end, 100 + (i* 100))
    end)
end



if jq("#nav--sub").length > 0 then
    jq("#nav--sub li a").click(function()
        th = jq(__js"this")
        current_part = th.attr("href")

        if not th.hasClass("special") then
            th.parents("ul").find("li a").removeClass("special")
            th.addClass("special")
            jq(".part-content").stop(true, true).fadeOut()
            jq(current_part).stop(true, true).fadeIn()
        end

            steps_show(current_part)

        return false
    end)
end



jq("#gallery--video").poptrox();


{% if site.deploy == "true" %}
    if jq("#background-slideshow").length > 0 then
        jq("#background-slideshow").kenburnsy{ fullscreen=true }
    end
{% endif %}