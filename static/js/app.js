(function () {
  function formatCountdown(targetIso) {
    var target = new Date(targetIso);
    if (Number.isNaN(target.getTime())) return "";

    var now = Date.now();
    var diff = target.getTime() - now;
    if (diff <= 0) return "Lights out soon";

    var days = Math.floor(diff / 86400000);
    var hours = Math.floor((diff % 86400000) / 3600000);
    var minutes = Math.floor((diff % 3600000) / 60000);

    if (days > 0) return days + "d " + hours + "h to race";
    return hours + "h " + minutes + "m to race";
  }

  function tick() {
    document.querySelectorAll("[data-countdown]").forEach(function (el) {
      el.textContent = formatCountdown(el.getAttribute("data-countdown"));
    });
  }

  tick();
  setInterval(tick, 30000);
})();
