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


if jq("#menu_show").length > 0 then
    jq("#menu_show").click(function()
        right = jq("#cover__right")
        outside = jq("#cover__outside")

        jq("#menu_show").toggleClass("active")
        jq("#menu_show").toggleClass("forever")
        jq("#cover__right").addClass("bounceOutRight")

        if not right.hasClass("hidden") then
            right.addClass("hidden")

            setTimeout(function()
                right.css("display", "none")
            end, 1400)

            outside.css("display", "block")

        else
            -- outside.removeClass("visible")
            setTimeout(function()
                outside.css("display", "none")
            end, 1000)
            right.removeClass("hidden")
            right.removeClass("bounceOutRight")
            right.addClass("bounceInRight")
            right.css("display", "block")
        end
    end)
end


if jq("#nav--sub").length > 0 then
    jq("#nav--sub li a").click(function()
        th = jq(__js"this")
        current_part = th.attr("href")

        jq("#about").css("display", "none")
        jq("#contributors").css("display", "none")
        jq("#contact").css("display", "none")

        jq(current_part).css("display", "block")

        return false
    end)
end

jq("#gallery--video").poptrox();

if jq("#background-slideshow").length > 0 and jq(window).height() > 800 then
    jq("#background-slideshow").kenburnsy{ fullscreen=true }
end