let showHiddenMenuBtnId = "showHiddenMenuTable"
let hiddenMenuContainerId = "hiddenMenuContainer"
let idSeparator = "MenuTable"
function bindButtons() {
    $("button[id^='"+showHiddenMenuBtnId+"']").each(function (i, el) {
        $(this).on("click", function () {
            let id = $(this).attr('id').split(idSeparator)[1];
            let menuId = "#"+hiddenMenuContainerId + id
            $("div[id^='"+hiddenMenuContainerId+"']").each(function (i, el) {
                
                if (menuId != "#" + $(this).attr("id")) {
                    if ($(this).css('display') != 'none') {
                        $(this).toggle()
                    }
                }
            })
            let hiddenMenu = $(menuId).parent()
            let isVisible = isvisibleOnViewport(hiddenMenu[0])
            if (!isVisible) {
                $(menuId).css("bottom", "40px")
            } 
            $(menuId).toggle()
        });
    });
}

function isvisibleOnViewport(element) {
    var rect = element.getBoundingClientRect();
    var html = document.documentElement;
    return (
        (rect.top) >= 0 &&
        rect.left >= 0 &&
        (rect.bottom + 100) <= (window.innerHeight || html.clientHeight) &&
        rect.right <= (window.innerWidth || html.clientWidth)
    );
}

$(document).ready(function () {

    $(document).mouseup(function (e) {
        $("div[id^='"+hiddenMenuContainerId+"']").each(function (i, el) {
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0) {
                if ($(this).css('display') != 'none') {
                    $(this).toggle()
                }
            }
        })
    });

    let interval = setInterval(function () {
        let buttonsLength = $("button[id^='"+showHiddenMenuBtnId+"']").length
        if (buttonsLength > 0) {
            console.log("bindButtons")
            bindButtons()
            clearInterval(interval)
        }
    }, 500)
})