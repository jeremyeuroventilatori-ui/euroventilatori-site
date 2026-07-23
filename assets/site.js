/* JS commun des pages intérieures : thème, menu mobile, parallaxe légère.
   (index.html embarque en plus ses scripts propres : canvas hero, pupitre.) */
(function(){
"use strict";
var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
var root = document.documentElement;

var themeBtn = document.getElementById("themeBtn");
if (themeBtn) themeBtn.addEventListener("click", function(){
  var dark = root.getAttribute("data-theme") === "dark" ||
    (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
  root.setAttribute("data-theme", dark ? "light" : "dark");
});

var burger = document.getElementById("burger"), nav = document.getElementById("mainNav");
if (burger && nav){
  burger.addEventListener("click", function(){
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function(e){
    if (e.target.tagName === "A"){ nav.classList.remove("open"); burger.setAttribute("aria-expanded","false"); }
  });
}

var plxEls = [];
document.querySelectorAll("[data-plx]").forEach(function(el){
  plxEls.push({ el:el, d:parseFloat(el.getAttribute("data-plx"))||0, sec:null });
});
function plxFrame(){
  var vc = innerHeight/2;
  for (var i=0;i<plxEls.length;i++){
    var o = plxEls[i];
    if (!o.sec) o.sec = o.el.closest("section, footer") || o.el.parentElement;
    var r = o.sec.getBoundingClientRect();
    if (r.bottom < -200 || r.top > innerHeight + 200) continue;
    var y = (r.top + r.height/2 - vc) * o.d;
    o.el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
  }
}
if (!reduced && plxEls.length){
  var tick = false;
  addEventListener("scroll", function(){
    if (tick) return; tick = true;
    requestAnimationFrame(function(){ plxFrame(); tick = false; });
  }, {passive:true});
  plxFrame();
}
})();
