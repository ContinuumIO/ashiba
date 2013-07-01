/* Compiled with Ashiba v0.0 */

$(window).load(function(){
  $("#btn_convert").on("click",
    ashiba.eventHandlerFactory("btn_convert", "click")
  );
});