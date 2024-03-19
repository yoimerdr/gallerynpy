(function () {
  document.addEventListener("DOMContentLoaded", function () {
    function addColor(target, color) {
      $(target).css({
        color: color
      })
    }

    $("em.sig-param .default_value .pre").each(function () {
      var color = "var(--code-keyword)";
      try {
        switch (typeof eval(this.innerText)) {
          case "string":
            color = "var(--code-string)";
            break;
          case "number":
            color = "var(--code-number)";
            break;

        }
      } catch (e) {
      }

      addColor(this, color)
    })

    $("em.sig-param").each(function () {
      $(this).find(".n > .pre").each(function (index) {
        var color = "var(--code-class)";
        if (index === 0)
          color = "var(--code-params)"

        addColor(this, color)
      })

    })

    var element = $(".wy-side-nav-search")
    var version = element.find(".version")

    if (version) {
      var icon = element.find(".icon.icon-home")

      $("<small>")
        .text(version.text())
        .appendTo(icon)

      element = $("nav.wy-nav-top")

      element.find("a")
        .last()
        .remove()

      element.append(icon.clone())
    }

    version.remove()

    $("dt.sig.py").addClass("notranslate")

    function checkFabUpPosition() {
      var fabUp = $("#fab-up")
      window.scrollY < window.innerHeight ? fabUp.hide() : fabUp.show()
    }

    $("<button>")
      .attr("id", "fab-up")
      .attr("class", "fab-up")
      .append(
        $("<i>")
          .attr("class", "fa fa-arrow-up")
      )
      .click(function () {
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        })
      })
      .appendTo(document.body)

    $("i[data-toggle='wy-nav-top']")
      .first()
      .click(function () {
        $("#fab-up")
          .toggle()
        checkFabUpPosition()
      })

    checkFabUpPosition()
    document.addEventListener("scroll", checkFabUpPosition)
  })
})()