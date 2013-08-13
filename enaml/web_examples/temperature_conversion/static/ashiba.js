$(document).ready(function(){
  /* Nice-ify sliders */
  $('input[type="range"]').after(function(){
    return ('&nbsp;<output for="' + this.id +'">' +
                    this.value +'</output>');
  }).on('change', function(){
    $('output[for="'+ this.id +'"]').val(this.value);
  });

  /* Bless jQUI elements */
  var uiElements = ['tabs', 'dialog'];
  for (i=0;i<uiElements.length;i++){
    var e = uiElements[i];
    $('.jqui-' + e + ':not(.hide)')[e]();
  }

  /* Setup Websockets */
  if ("WebSocket" in window) {                                         
    ws = new WebSocket("ws://" + document.domain + ":12345/api");                
    ws.onmessage = function (msg) {                                  
      console.log("MESSAGE RECEIVED:\n"+msg.data);
      var deltas = JSON.parse(msg.data)['domDeltas'];
      ashiba.setDomDeltas(deltas);
    };                                                               
  } else {                                                             
    alert("WebSocket not supported");                                
  }

  /* Bind Events */
  $('[data-events]').each(function(){
    console.log("Object: " + this.id);
    var events;
    if (!!this.getAttribute('data-events')){
      events = this.getAttribute('data-events').split(/\s+/);
    } else {
      events = [];
    }
    for(i=0;i<events.length;i++){
      console.log("  Event: " + events[i]);
      $(this).on(events[i],
        ashiba.eventHandlerFactory(this, events[i])
      );
    }
  });
});

var ashiba = {
  'setDomDeltas' : function(deltas){
    function setDomDelta(obj){
      console.log('SETTING #' + obj.id)
      Object.getOwnPropertyNames(obj['data']).forEach(function(pName){
        $('#' + obj.id).prop(pName, obj['data'][pName]);
        console.log('#' + obj.id + '.' + pName + ' = ' + obj['data'][pName]);
      });
    }
    console.log("Setting deltas: " + JSON.stringify(deltas));
    deltas.forEach(setDomDelta);
  },

  'eventHandlerFactory' : function (me, eventName){
    var objName = me.id;
    return function(){
      var message = {
        'id'    : objName,
        'event' : eventName,
        'meta'  : {},
        'data'  : {}
      };

      var dataVisible;
      if (!!me.getAttribute('data-visible')) {
        dataVisible = me.getAttribute('data-visible').split(/\s+/);
      } else {
        dataVisible = [];
      }

      for(i=0;i<dataVisible.length;i++){
        var key = dataVisible[i];
        message['data'][key] = me[key];
      }
      
      console.log("Observed event #" + objName + ":" + eventName + '\n'
                + "  Message: " + JSON.stringify(message, undefined, 2));
      
      //ashiba.sendAJAX(message);
      ws.send(JSON.stringify(message));
    };
  },

  /* The following functions are depricated, used for the AJAX event version */

  'getDom' : function(){
    var dom = {}; 
    var inputs = $('input, select, [data-visible]');
    for(i=0;i<inputs.length;i++){
      var element = inputs[i];
      if(!!element.id){
        dom[element.id] = {};
        var meta = {'nodeName' :element.nodeName,
                    'innerHTML':element.innerHTML}
        if (element.className !== ''){
          meta['class'] = element.className.split(/\s+/);
        } else {
          meta['class'] = [];
        }
        dom[element.id]['_meta'] = meta;
        if (element.type === "checkbox"||
            element.type === "radio"){
          dom[element.id]['checked'] = element.checked;
        }else{
          dom[element.id]['value'] = element.value;
        }
      }

      if (element.hasAttribute('data-visible')){
        var dv = element.getAttribute('data-visible').split(/\s+/);
        dv.forEach(function(x){dom[element.id][x] = element[x];});
      }
    }

    return JSON.stringify(dom);
  },

  'setDom' : function (jsonResponse){
    var domObj = jsonResponse["dom_changes"];
    Object.getOwnPropertyNames(domObj).forEach(function(element_name){
      var element = document.getElementById(element_name);
      Object.getOwnPropertyNames(domObj[element_name]).forEach(function(property){
        console.log("Element name: " + element_name + '\n'
                  + "    Property: " + property + '\n'
                  + "       Value: " + domObj[element_name][property] + '\n'
        );
        if (property != '_meta'){
          element[property] = domObj[element_name][property];
        } else {
          var meta = domObj[element_name]['_meta'];
          if (meta.innerHTML !== undefined){  
            element.innerHTML = meta.innerHTML;
          }
          for (i=0;!!meta['class'] && i<meta['class'].length;i++){
            var className = meta['class'][i];
            if (className[0] == '-'){
              $(element).removeClass(className.slice(1));
            } else if (className[0] == '+'){
              $(element).addClass(className.slice(1));
            }
          }
          if (!!meta['style']){
            $(element).css(meta['style']);
          }
          if (!!meta['eval']){
            console.log(element.id + " EVAL " + meta['eval']);
            try{
              $(element).each(function(){eval(meta['eval']);});
            }catch(err){
              console.log("ERROR in _meta.eval on element " 
                + element.id + ':' + err);
            }
          }
        }
      });
      if (element !== null){
          var nn = element.nodeName.toLowerCase();
          if (!(nn == 'input' || nn == 'select' || nn == 'textarea')
              && !!element.onchange){
            element.onchange();
          }
      }
    });
  },

  'sendAJAX' : function(msg, url){
    $.ajax({
      url: url,
      type: 'POST',
      data: msg,
      dataType: 'json'
    }).done(function(data){
      console.log("AJAX success, setting DOM elements: "
          + JSON.stringify(data));
      //ashiba.setDom(data);
    }).fail(function(data){
      debugStr = data.responseText;
      if (debugStr.indexOf('Werkzeug Debugger') >= 0){
        document.body.innerHTML = debugStr;
        console.log("AJAX failure: " +
                    /.*\/\//.exec($('title').last().text()));
      } else {
        alert("AJAX failure: " + debugStr);
        console.log("AJAX failure: " + debugStr);
      }
    }); 
  }
}
