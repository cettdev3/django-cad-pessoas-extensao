let customTabsId = "servicoContratadoList"
let tabsLinkId = "servicoContratadoLink"
let prevBtn = "formMembrosExecucaoPrev"
let nextBtn ="formMembrosExecucaoNext"
let finishBtn = "finishCadastroServicoContratado"

function getActiveTab() {
    let activeTab = $("*[id^='"+customTabsId+"']").filter(function (i, el) {
        return $(el).hasClass("active") || $(el).hasClass("active-form-tab")
    })

    id = $(activeTab[0]).attr("id")

    if (id == undefined) return 0

    id = id.charAt(id.length - 1)
    return id
}

function functionGetTabsQuantity() {
    let tabs = $("*[id^='"+customTabsId+"']")
    tabs = $("*[id^='"+customTabsId+"']")
    let length = tabs.length
    return length
}

function showHideTabs(instructions) {
    instructions.show.forEach(function (elementId) {
            $("#" + elementId).show()
    })
    instructions.hide.forEach(function (elementId) {
        $("#" + elementId).hide()
    })
}

function processTabBtnClick(direction) {
    let activeTab = getActiveTab()
    let nextTab = parseInt(activeTab) + direction
    $("#"+tabsLinkId+nextTab).trigger("click")
    $("#"+customTabsId+nextTab).addClass("active-form-tab")
    $("#"+customTabsId+activeTab).removeClass("active-form-tab")
    setTabsbehavior()
}

function setTabsbehavior() {
    tabsControl = {
        first: {
            show: [nextBtn],
            hide: [prevBtn, finishBtn]
        },
        last: {
            show: [prevBtn, finishBtn],
            hide: [nextBtn]
        },
        middle: {
            show: [prevBtn, nextBtn],
            hide: [finishBtn]
        },
        only: {
            show: [finishBtn],
            hide: [prevBtn, nextBtn]
        }
    }

    activTabFn = getActiveTab()
    tabsQuantity = functionGetTabsQuantity()
    console.log("activTabFn: " + activTabFn)
    console.log("tabsQuantity: " + tabsQuantity)
    if (activTabFn == 1 && tabsQuantity > 1) {
        console.log("first tab")
        showHideTabs(tabsControl.first)
    } else if (tabsQuantity == 1) {
        console.log("only tab")
        showHideTabs(tabsControl.only)
    } else if (activTabFn == tabsQuantity && tabsQuantity > 1) {
        console.log("last tab")
        showHideTabs(tabsControl.last)
    } else if (tabsQuantity > 1) {
        console.log("middle tab")
        showHideTabs(tabsControl.middle)
    }
}

function setupTabNavigationEvent() {
    $(document.body).off("click", "#"+nextBtn);
    $(document.body).off("click", "#"+prevBtn);

    $(document.body).on("click", "#"+nextBtn, function () {
        console.log("click next")
        processTabBtnClick(1);
    });

    $(document.body).on("click", "#"+prevBtn, function () {
        processTabBtnClick(-1);
    });
}


function setModalBehaviour(callcback) {
    setTabsbehavior()
    callcback()
}

$(document).ready(function () {
    setTabsbehavior()
    setupTabNavigationEvent(); 
})