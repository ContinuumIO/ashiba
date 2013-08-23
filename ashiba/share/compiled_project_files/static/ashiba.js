//Should probably namespace this
debug = false;

var ashiba = {
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
      if (element === null){
        throw "Error: Ashiba's handlers.py refers to an object named '" +
          element_name + "' which does not exist in the DOM."
      }
      Object.getOwnPropertyNames(domObj[element_name]).forEach(function(property){
      	if (debug) {
        	console.log("Element name: " + element_name + '\n'
            	      + "    Property: " + property + '\n'
                	  + "       Value: " + domObj[element_name][property] + '\n'
        	);
        }
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
            /* TODO: Put the following in a map if eval is a list */
            try{
              $(element).each(function(){eval(meta['eval']);});
            }catch(err){
              console.log("ERROR in _meta.eval on element "
                + element.id + ':\n>>> ' + err);
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

  'grabAttr' : function (o){
    var att = o.attributes;
    var out = {};
    for (i=0;i<att.length;i++){
      out[att[i].name] = att[i].value;
    }
    return out;
  },

  'eventHandlerFactory' : function (objName, eventName){
    return function(){
      console.log("Received event " + objName + ":" + eventName);
      d = ashiba.getDom();
      $.ajax({
        url: "event/" + objName + "/" + eventName,
        type: 'POST',
        data: d,
        dataType: 'json',
        contentType: "application/json"
      }).done(function(data){
        console.log("AJAX success, setting DOM elements.");
        //console.log("Response Data: " + JSON.stringify(data));
        ashiba.setDom(data);
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
    };
  }
}

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
});
