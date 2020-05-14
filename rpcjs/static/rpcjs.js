var socket = io();

log = function(str) {
    console.info(str);
};

socket.on('disconnect', function() {
    socket.emit("disconnect");
});

// bind callback when the event is fired; forward it to the server
// so it can reply
bind_callback = function(event, id, attr, prop){
    return function(){
        var event_name = "bind_" + event + "_" + id;
        log("notifying " + event_name + " " + attr + " " + prop);

        data = null;
        if (attr !== null){
            data = document.getElementById(id).getAttribute(attr);
        }
        if (prop !== null){
            data = document.getElementById(id)[prop];
        }
        log('sending '+ data)
        socket.emit(event_name, data);
    };
};

// bind an element so we receive events when it is modified
// supported events: https://www.w3schools.com/jsref/dom_obj_event.asp
socket.on("bind", function(data) {
    log("binding " + data);

    var id = data["id"];
    var event = data["event"];
    var attr = data["attribute"];
    var prop = data["property"];

    var element = document.getElementById(id);
    var handler = bind_callback(event, id, attr, prop);
    element.addEventListener(event, handler);

    // set the initial value
    handler();
});


socket.on("set_attribute", function(data) {
    log("set_attribute " + data);

    var id = data["id"];
    var attribute = data["attribute"];
    var value = data["value"];

    var element = document.getElementById(id)
    element.setAttribute(attribute, value);
});

socket.on("set_property", function(data) {
    log("set_property " + data);

    var id = data["id"];
    var property = data["property"];
    var value = data["value"];

    var element = document.getElementById(id)
    element[property] = value;
});

function new_html_node(htmlString) {
  var div = document.createElement('div');
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

function new_html_nodes(htmlString) {
  var div = document.createElement('div');
  div.innerHTML = htmlString.trim();
  return div.childNodes;
}

socket.on("append_child", function(data) {
    log("append_child " + data);

    var id = data["id"];
    var value = new_html_node(data["node"]);

    var element = document.getElementById(id)
    element.appendChild(value);
});


socket.on("redirect", function(data) {
    log("redirect to " + data);

    var url = data["url"];
    window.location.href = url;
});


socket.on("get_size", function(data) {
    log("get_size " + data);

    var id = data["id"];
    var element = document.getElementById(id)

    var w = element.clientWidth;
    var h = element.clientHeight;

    socket.emit('get_size_' + id , {
        "width": w,
        "height": h
    });
});


// Update the vega chart data with new incoming data from the server
// In that case the server dictates when through a websocket
appendStreamData = function (id) {
    return function(chart) {
        // Register the event handler
        socket.on('stream_data_' + id, function(data){
            var values = data['new_values'];
            var name = data['name']

            var changeSet = vega
                .changeset()
                .insert(values);

            // log('receiving ' + name + ' ' + values);
            chart.view.change(name, changeSet).run();
        });
        log('stream handler attached');
    }
}

displayVega = function(vegaEmbed, elementId, spec) {
    var embedOpt = {
        "mode": "vega-lite"
    };

    function showError(el, error) {
        el.innerHTML = ('<div class="error" style="color:red;">' +
            '<p>JavaScript Error: ' + error.message + '</p>' +
            "<p>This usually means there's a typo in your chart specification. " +
            "See the javascript console for the full traceback.</p>" +
            '</div>');
        throw error;
    }
    const el = document.getElementById(elementId);

    vegaEmbed("#" + elementId, spec)
        .then(appendStreamData(elementId))
        .catch(error => showError(el, error));
};


socket.on("display_vega", function(data) {
    log("display_vega");

    var elementId = data['id'];
    var spec = data['spec'];

    displayVega(vegaEmbed, elementId, spec)
});


socket.on("connect", function() {
    socket.emit("handshake");
});

log("RPCjs setup is done");